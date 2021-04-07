from random import choice

from logger import get_logger
from ..utils.responseTools import addBreak, wrapSpeak, googleResponse

log = get_logger('miscHandlers')

def modifyFinishHandler(data):
    searchContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/search')
    ][0]['parameters']
    
    # logging for development purpose
    log.debug('Finished context: {}'.format(searchContext))

    fulfillmentText = [
        choice([
            'Great',
            'Got it',
            'Okay'
        ]),
        'Your modification has been applied to the mashup.',
    ]
    outputContexts = data['queryResult']['outputContexts']

    for c in outputContexts:
        c['lifespanCount'] = 0
    
    payload = googleResponse(
        ssml=wrapSpeak(addBreak(fulfillmentText[0], fulfillmentText[1])),
        text='. '.join(fulfillmentText)
    )
    payload['google']['expectUserResponse'] = False

    return {
        'fulfillmentText': '. '.join(fulfillmentText),
        'outputContexts': outputContexts,
        'payload': payload
    }