import requests

from logger import get_logger
from .encodeTools import decodeObj

def parseFollowupContext(data):
    strip_session = lambda x: x['name'].replace(data['session'] + '/contexts/', '')
    contexts = {strip_session(c): c for c in data['queryResult']['outputContexts']}
    
    implicature = contexts['implicature-followup']['parameters']['implicatureType']
    device = '' if 'parameters' not in contexts['implicature'] else contexts['implicature']['parameters']['devices']
    if device == '':
        device = None
    
    return (implicature, device)


def requestSearch(implicature, **kwargs):
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


def requestModify(modifyType, implicature, **kwargs):
    """
    @param modifyType: the type of modification, expected one of ['replace', 
      'append', 'remove']
    @param implicature: the core information to search for the IoT action.
    @kwargs checkSideEffect: default True, set False if you do not want 
      to consider any side effects.
    @kwargs device: default None, set if the user uttered device hints
    @kwargs skipCount: default 0, increase by 1 if the user reject the
      previous search result.
    """
    assert modifyType in ['replace', 'append', 'remove']

    jsonForm = {
        'modifyType': modifyType,
        'implicature': implicature,
        **kwargs
    }
    response = requests.post('http://localhost:445/modify', json=jsonForm)
    response = response.json()

    if response['status'] == 'error':
        log = get_logger()
        log.error('Mashup module returned error - ' + response['what'])
        raise RuntimeError(response['what'])
    
    return decodeObj(response['searchResult'])


def requestTypeCheck(intent, implicature, **kwargs):
    """
    @param intent: the Dialogflow action information
    @param implicature: the core information to search for the IoT action.
    @kwargs checkSideEffect: default True, set False if you do not want 
      to consider any side effects.
    @kwargs device: default None, set if the user uttered device hints
    @kwargs skipCount: default 0, increase by 1 if the user reject the
      previous search result.
    """
    jsonForm = {
        'intent': intent,
        'implicature': implicature,
        **kwargs
    }
    response = requests.post('http://localhost:445/type', json=jsonForm)
    response = response.json()

    if response['status'] == 'error':
        log = get_logger()
        log.error('Mashup module returned error - ' + response['what'])
        raise RuntimeError(response['what'])
    
    return response


def requestParam(implicature, **kwargs):
    """
    @param implicature: the core information to search for the IoT action.
    @kwargs checkSideEffect: default True, set False if you do not want 
      to consider any side effects.
    @kwargs device: default None, set if the user uttered device hints
    @kwargs skipCount: default 0, increase by 1 if the user reject the
      previous search result.
    """
    jsonForm = {
        'implicature': implicature,
        **kwargs
    }
    response = requests.post('http://localhost:445/param', json=jsonForm)
    response = response.json()

    if response['status'] == 'error':
        log = get_logger()
        log.error('Mashup module returned error - ' + response['what'])
        raise RuntimeError(response['what'])
    
    return response