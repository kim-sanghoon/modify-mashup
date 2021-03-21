from random import choice

from logger import get_logger
from ..utils.searchTools import requestSearch
from ..utils.responseTools import addBreak, wrapSpeak, googleResponse

log = get_logger('rejectHandler')


def implicaturePinpointPreviousHandler(data):
    searchContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/search')
    ][0]['parameters']
    
    # logging for development purpose
    log.debug('Rejection context: {}'.format(searchContext))

    result = requestSearch(
        searchContext['implicatureType'], 
        device=None if searchContext['device'] == "" else searchContext['device'],
        skipCount=searchContext['count'] - 1  # decrease the skipCount by 1
    )

    _, trigger, action, *_ = result['historyData']

    mainResponse = '{}, {}'.format(
        choice([
            'Going back to the previous result',
            'Going back to the previous one',
            'Back to the previous result',
            'Switched back to the previous one'
        ]),
        action.type.language['past'].format(**action.values)
    )

    subResponse = [
        'Would you like to check the details', 
        'or change it?'
    ]

    # decrease the skipCount by 1
    outputContexts = data['queryResult']['outputContexts']
    for c in outputContexts:
        if c['name'].endswith('/search'):
            c['parameters']['count'] -= 1

    return {
        'fulfillmentText': mainResponse + '. ' + ', '.join(subResponse),
        'outputContexts': outputContexts,
        'payload': googleResponse(
            ssml=wrapSpeak(
                addBreak(
                    mainResponse, 
                    addBreak(subResponse[0], subResponse[1], strength='weak', comma=True)
                )),
            text=mainResponse + '. ' + ', '.join(subResponse)
        )
    }