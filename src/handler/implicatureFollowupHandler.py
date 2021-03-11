import requests

from logger import get_logger
from ..utils.encodeTools import decodeObj
from ..utils.responseTools import wrapSpeak, addBreak

def __request_search(implicature, **kwargs):
    """
    @param implicature: the core information to search for the IoT action.
    @kwargs checkSideEffect: default True, set False if you do not want 
      to consider any side effects.
    @kwargs device: default None, set if the user uttered device hints
    @kwargs skipCount: default 0, increase by 1 if the user reject the
      previous search result.
    """
    jsonForm = {'implicature': implicature, **kwargs}
    response = requests.post('http://localhost:445/search', json=jsonForm)
    response = response.json()

    if response['status'] == 'error':
        log = get_logger()
        log.error('Mashup module returned error - ' + response['what'])
        raise RuntimeError(response['what'])
    
    return decodeObj(response['searchResult'])
    

def implicatureFollowupYesHandler(data):
    strip_session = lambda x: x['name'].replace(data['session'] + '/contexts/', '')
    contexts = {strip_session(c): c for c in data['queryResult']['outputContexts']}
    
    implicature = contexts['implicature-followup']['parameters']['implicatureType']
    device = '' if 'parameters' in contexts['implicature'] else contexts['implicature']['parameter']['devices']
    if device == '':
        device = None

    result = __request_search(implicature, device=device)
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
        action.type.language['past'],
        '' if not result['sideEffect'] else ' potentially',
        implicatureResponse[implicature.lower()]
    )
    subResponse = 'Would you like to check which trigger activated it, or change it to what you need?'
    
    return {
        'fulfillmentText': mainResponse + ' ' + subResponse,
        'payload': {
            'google': {
                'expectUserResponse': True,
                'richResponse': {
                    'items': [
                        {
                            'simpleResponse': {
                                'ssml': wrapSpeak(addBreak(mainResponse, subResponse, breakTime='2000ms')),
                                'displayText': mainResponse + ' \n' + subResponse
                            }
                        }
                    ]
                }
            }
        }
    }

def implicatureFollowupNoHandler(data):
    # We assume that the implicature detection failed.
    fulfillmentText = "It seems I was wrong. Could you tell me what you need?"

    return {
        'fulfillmentText': fulfillmentText
    }