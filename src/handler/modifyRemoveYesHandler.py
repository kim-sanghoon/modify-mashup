from random import choice

from logger import get_logger
from ..utils.searchTools import requestModify
from ..utils.responseTools import addBreak, wrapSpeak, googleResponse

log = get_logger('removeHandler')

def modifyRemoveYesHandler(data):
    searchContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/search')
    ][0]['parameters']
    
    # logging for development purpose
    log.debug('Remove context: {}'.format(searchContext))

    result = requestModify(
        'remove',
        searchContext['implicatureType'], 
        device=None if searchContext['device'] == "" else searchContext['device'],
        skipCount=searchContext['count']
    )

    mainResponse = [
        choice([
            'The rule has been successfully removed',
            'Successfully removed'
        ]),
        'You can find out other rules that may have affected you'
    ]

    return {
        'fulfillmentText': mainResponse[0] + '. ' + mainResponse[1] + '.',
        'payload': googleResponse(
            ssml=wrapSpeak(addBreak(mainResponse[0], mainResponse[1])),
            text=mainResponse[0] + '. ' + mainResponse[1] + '.'
        )
    }
