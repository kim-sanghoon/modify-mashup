#!/usr/bin/env python3

from flask import Flask, request, jsonify
from datetime import datetime

import requests, sys, json

from logger import get_logger

# Define intent handlers here
from src.handler.dfImplicatureHandler import dfImplicatureHandler
from src.handler.implicatureFollowupHandler import implicatureFollowupYesHandler, implicatureFollowupNoHandler
from src.handler.implicaturePinpointDetailHandler import implicaturePinpointDetailHandler
from src.handler.implicaturePinpointRejectHandler import implicaturePinpointRejectHandler

app = Flask(__name__)
log = get_logger()

@app.route('/', methods=['POST'])
def main():
    data   = request.get_json()
    intent = data['queryResult']['intent']['displayName']
    action = data['queryResult']['action']

    #################
    # Debug purpose #
    #################

    time = datetime.now()
    timestamp = int(time.timestamp())

    with open('log/dialogflow/{}.json'.format(timestamp), 'w+') as f:
        json.dump(data, f)
    
    log.debug('User intent : {}'.format(str(intent)))
    log.debug('Raw user input: {}'.format(str(intent)))
    log.debug('Input data has been saved as - {}.json'.format(timestamp))

    [h.flush() for h in log.handlers]

    ###################
    # Invoke handlers #
    ###################

    switch = {
        # 'action' : function
        
        # Initial stage -- user implicature handler
        'implicature.airquality.high': dfImplicatureHandler,
        'implicature.airquality.low': dfImplicatureHandler,
        'implicature.brightness.high': dfImplicatureHandler,
        'implicature.brightness.low': dfImplicatureHandler,
        'implicature.humidity.high': dfImplicatureHandler,
        'implicature.humidity.low': dfImplicatureHandler,
        'implicature.noise.high': dfImplicatureHandler,
        'implicature.noise.low': dfImplicatureHandler,
        'implicature.security.high': dfImplicatureHandler,
        'implicature.security.low': dfImplicatureHandler,
        'implicature.temperature.high': dfImplicatureHandler,
        'implicature.temperature.low': dfImplicatureHandler,

        # Second stage -- implicature followup handler
        'implicature.followup.yes': implicatureFollowupYesHandler,
        'implicature.followup.no': implicatureFollowupNoHandler,

        # Third stage -- pinpoint branch handler
        'implicature.pinpoint.detail': implicaturePinpointDetailHandler,
        'implicature.pinpoint.modify.explicit': None,
        'implicature.pinpoint.reject': implicaturePinpointRejectHandler
    }

    handler = switch[action]
    ret = handler(data)

    [h.flush() for h in log.handlers]
    return jsonify(ret)

if __name__ == "__main__":
    # Check if the mashup module has been initialized
    try:
        mashupModuleCheck = requests.get(
            url='http://localhost:445/check'
        )

        mashupModuleCheck = mashupModuleCheck.json()
        if mashupModuleCheck['status'] != 'ok':
            raise ConnectionError('Mashup module has not been initialized.')
    except Exception as e:
        log.error(str(e))
        log.error('  -> error occurred while checking mashup module, exiting...')

        exit(-1)

    # Start the back-end
    app.run(host='0.0.0.0',
            port=443,
            ssl_context=('server.crt', 'server.key'))