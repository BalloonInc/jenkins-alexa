"""
Alexa skill for Jenkins, to be ran in AWS lambda.

(c) 2018 Balloon Inc. VOF
Wouter Devriendt
"""
import os
import jenkins
from jenkins import JenkinsSettings
import alexahelpers as ah

settings = JenkinsSettings()

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
    speech_output = "Jenkins, out, have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return ah.build_response({}, ah.build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def startJob(intent, session):
    jenkins.startJob("BalloonInc-web", settings)
    session_attributes = {}
    speech_output = "Starting a job is not yet implemented"

    should_end_session = True
    reprompt_text = "Which job should I start?"
    return ah.build_response(session_attributes, ah.build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def abortJob(intent, session):
    session_attributes = {}
    speech_output = "Aborting a job is not yet implemented"
    reprompt_text = "Which job should I abort?"
    should_end_session = True
    return ah.build_response(session_attributes, ah.build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def getJobStatus(intent, session):
    session_attributes = {}
    speech_output = "Getting a job status is not yet implemented"
    reprompt_text = "Which job should I get the status for?"
    should_end_session = True
    return ah.build_response(session_attributes, ah.build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

    newSettings = jenkins.readSettingsFromEnvironment()
    settings.jenkins_url = newSettings.jenkins_url
    settings.username = newSettings.username
    settings.auth_token = newSettings.auth_token

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
