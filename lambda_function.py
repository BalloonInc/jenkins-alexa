"""
Alexa skill for Jenkins, to be ran in AWS lambda.

(c) 2018 Balloon Inc. VOF
Wouter Devriendt
"""
import os
import time

import jenkins
from jenkins import Jenkins
import alexahelpers as ah
import humantime

jenkins = Jenkins()

# --------------- Functions that control the skill's behavior ------------------


def getWelcomeResponse():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Jenkins is listening. " \
                    "You can ask me to start a job, get status info or abort a job."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Do you want to start a job, get status info or abort a job?"
    should_end_session = False
    return ah.build_response(session_attributes, ah.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def endSession():
    card_title = "Session Ended"
    speech_output = "Jenkins out, have a nice day! "
    should_end_session = True
    return ah.build_response({}, ah.build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def startJob(intent, session):
    session_attributes = {}
    should_end_session = False
    rawJobName = getRawJobNameFromIntent(intent)
    if rawJobName:
        print("raw job name found")
        jobName = jenkins.searchJobByName(rawJobName)
        if not jobName:
            print("didn't understand the jobname")
            speech_output = "I didn't find the job: " + rawJobName + ". Which job should I start?"
        else:
            print("all good, found the job, starting it now.")
            r = jenkins.startJob(jobName)
            eta = jenkins.getJobStatus(jobName).json()["estimatedDuration"]

            speech_output = "The job is queued for running, and will take approximately " + humantime.format(eta // 1000)
            should_end_session = True
    else:
        print("no job name given")
        return ah.build_response(session_attributes, ah.build_speechlet_directive())

    reprompt_text = "Again: Which job should I start?"

    return ah.build_response(session_attributes, ah.build_speechlet_response(
        "Start job", speech_output, reprompt_text, should_end_session))


def abortJob(intent, session):
    session_attributes = {}
    should_end_session = False
    rawJobName = getRawJobNameFromIntent(intent)
    if rawJobName and intent['confirmationStatus'] != 'NONE':
        print("raw job name found")
        jobName = jenkins.searchJobByName(rawJobName)
        if not jobName:
            print("didn't understand the jobname")
            speech_output = "I didn't find the job: " + rawJobName + ". Which job should I abort?"
        else:
            print("all good, found the job, aborting it now.")
            r = jenkins.abortJob(jobName)
            speech_output = "I requested for " + jobName + " to be aborted."
            should_end_session = True
    else:
        print("no job name given")
        return ah.build_response(session_attributes, ah.build_speechlet_directive())

    reprompt_text = "Again, which job should I abort?"
    return ah.build_response(session_attributes, ah.build_speechlet_response(
        "Abort job", speech_output, reprompt_text, should_end_session))


def getJobStatus(intent, session):
    session_attributes = {}
    should_end_session = False
    rawJobName = getRawJobNameFromIntent(intent)
    if rawJobName:
        print("raw job name found")
        jobName = jenkins.searchJobByName(rawJobName)
        if not jobName:
            print("didn't understand the jobname")
            speech_output = "I didn't find the job: " + rawJobName + ". Which job should I get the status for?"
        else:
            print("all good, found the job, getting status now.")
            r = jenkins.getJobStatus(jobName)
            speech_output = getSpeechOutputForStatus(r)
            should_end_session = True
    else:
        print("no job name given")
        return ah.build_response(session_attributes, ah.build_speechlet_directive())

    reprompt_text = "Again, which job should I get the status for?"
    return ah.build_response(session_attributes, ah.build_speechlet_response(
        "Get status", speech_output, reprompt_text, should_end_session))

def getSpeechOutputForStatus(response):
    if response.status_code > 299 or response.status_code < 200:
        return "I cannot get a status at the moment. Try again in a little while."
    else:
        res = response.json()
        if res["building"]:
            eta = res["estimatedDuration"]//1000 - (round(time.time()) - res["timestamp"]//1000)
            if eta > 10:
                return "The build is ongoing, expect it to run for another" + \
                    humantime.format(eta)
            else:
                return "The build is still ongoing, but should be done any minute now."

        else:
            if res["result"] == "SUCCESS":
                return "The build finished succesfully in " + \
                    humantime.format(res["duration"]//1000)
            elif res["result"] == "ABORTED":
                return "The build was aborted after " + \
                    humantime.format(res["duration"]//1000)
            elif res["result"] == "FAILED":
                return "The build failed after " + \
                    humantime.format(res["duration"]//1000)
            else:
                return "The build is " + res["result"]


def getRawJobNameFromIntent(intent):
    if 'slots' not in intent:
        return None
    if 'jobname' not in intent['slots']:
        return None
    if 'value' not in intent['slots']['jobname']:
        return None
    return intent['slots']['jobname']['value']

# --------------- Events ------------------


def on_session_started(session_started_request, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

    jenkins.readSettingsFromEnvironment()


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return getWelcomeResponse()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print(intent_request)
    print(intent_request['intent'])
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId']+", intentName=" + intent_request['intent']['name'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "StartJobIntent":
        return startJob(intent, session)
    elif intent_name == "JobStatusIntent":
        return getJobStatus(intent, session)
    elif intent_name == "CancelJobIntent":
        return abortJob(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return getWelcomeResponse()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return endSession()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.ceb79513-96ca-4d59-a036-c51d91a2c53e"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
