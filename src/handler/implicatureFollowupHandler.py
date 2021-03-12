import requests

from ..utils.responseTools import wrapSpeak, addBreak, googleResponse
from ..utils.searchTools import requestSearch, parseFollowupContext

def implicatureFollowupYesHandler(data):
    implicature, device = parseFollowupContext(data)
    result = requestSearch(implicature, device=device)

    # if nothing found
    if result['historyData'] is None:
        fulfillmentText = [
            "Sorry, but I couldn't find any actions about it.",
            "Could you start over by saying the problem again?"
        ]
        return {
            'fulfillmentText': ' '.join(fulfillmentText),
            'payload': googleResponse(
                ssml=wrapSpeak(addBreak(fulfillmentText[0], fulfillmentText[1])),
                text=' \n'.join(fulfillmentText)
            )
        }
    
    # otherwise
    _, trigger, action, *_ = result['historyData']

    implicatureResponse = {
        "lowairquality": "the air quality's bad",
        "lowbrightness": "it's too dark",
        "lowhumidity": "it's dry",
        "lownoise": "it's too quiet",
        "lowsecurity": "it's not secure",
        "lowtemperature": "it's cold",
        "highairquality": "the air quality's too high",
        "highbrightness": "it's too bright",
        "highhumidity": "it's humid",
        "highnoise": "it's noisy",
        "highsecurity": "it's too secure",
        "hightemperature": "it's hot"
    }

    mainResponse = 'I found {} recently, and it may{} cause you feel that {}.'.format(
        action.type.language['past'].format(**action.values),
        '' if not result['sideEffect'] else ' potentially',
        implicatureResponse[implicature.lower()]
    )
    subResponse = [
        'Would you like to check which trigger activated it', 
        'otherwise', 
        'change or adjust it?'
    ]
    
    return {
        'fulfillmentText': mainResponse + ' ' + ' '.join(subResponse),
        'outputContexts': [
            {
                'name': '{}/contexts/search'.format(data['session']),
                'lifespanCount': 3,
                'parameters': {
                    'implicatureType': implicature,
                    'count': 0,
                    'device': device
                }
            }
        ],
        'payload': googleResponse(
            ssml=wrapSpeak(
                addBreak(mainResponse, addBreak(
                    addBreak(subResponse[0], subResponse[1], strength='weak', comma=True),
                    subResponse[2], strength='weak', comma=True
                ))),
            text=mainResponse + ' ' + ' '.join(subResponse)
        )
    }

def implicatureFollowupNoHandler(data):
    # We assume that the implicature detection failed.
    fulfillmentText = "It seems I was wrong. Could you tell me what you need?"
    outputContexts = data['queryResult']['outputContexts']
    
    for c in outputContexts:
        c['lifespanCount'] = 0

    return {
        'fulfillmentText': fulfillmentText,
        'outputContexts': outputContexts
    }