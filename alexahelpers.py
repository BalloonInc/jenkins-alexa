"""
Alexa skill helpers

(c) 2018 Balloon Inc. VOF
Wouter Devriendt
"""

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "Jenkins - " + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_speechlet_directive():
    return {
      "outputSpeech" : None,
      "card" : None,
      "directives" : [ {
        "type" : "Dialog.Delegate"
      } ],
      "reprompt" : None,
      "shouldEndSession" : False
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
