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
from src.handler.implicaturePinpointPreviousHandler import implicaturePinpointPreviousHandler
from src.handler.modifyRemoveYesHandler import modifyRemoveYesHandler
from src.handler.modifyUndoYesHandler import modifyUndoYesHandler
from src.handler.modifyFinishHandler import modifyFinishHandler
from src.handler.modifyTriggerOnlyHandler import modifyTriggerOnlyHandler
from src.handler.modifyFollowupYesHandler import modifyFollowupYesHandler
from src.handler.modifyFollowupAddChangeHandler import modifyFollowupAddChangeHandler
from src.handler.modifyDevicesParameterHandler import modifyDevicesParameterHandler
from src.handler.modifyFollowupAllDevicesHandler import modifyFollowupAllDevicesHandler
from src.handler.modifyFollowupTriggerActionHandler import modifyFollowupTriggerActionHandler
from src.handler.modifyNumericParameterHandler import modifyNumericParameterHandler

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
        'implicature.pinpoint.reject': implicaturePinpointRejectHandler,
        'implicature.pinpoint.previous': implicaturePinpointPreviousHandler,

        #####################
        # Modification step #
        #####################

        # misc handlers
        'modify.remove.yes': modifyRemoveYesHandler,
        'modify.undo.yes': modifyUndoYesHandler,
        'modify.finish': modifyFinishHandler,
        'modify.followup.yes': modifyFollowupYesHandler,
        'modify.followup.add-change': modifyFollowupAddChangeHandler,
        'modify.followup.all-devices': modifyFollowupAllDevicesHandler,
        'modify.followup.trigger-action': modifyFollowupTriggerActionHandler,

        # trigger-only handlers
        'modify.receive.call': modifyTriggerOnlyHandler,
        'modify.receive.message': modifyTriggerOnlyHandler,
        'modify.send.message': modifyTriggerOnlyHandler,
        'modify.connect': modifyTriggerOnlyHandler,
        'modify.disconnect': modifyTriggerOnlyHandler,
        'modify.date': modifyTriggerOnlyHandler,
        'modify.time': modifyTriggerOnlyHandler,
        'modify.weather': modifyTriggerOnlyHandler,
        'modify.sleep': modifyTriggerOnlyHandler,
        'modify.wakeup': modifyTriggerOnlyHandler,
        'modify.detect.raindrop': modifyTriggerOnlyHandler,
        'modify.undetect.raindrop': modifyTriggerOnlyHandler,
        'modify.detect.presence': modifyTriggerOnlyHandler,
        'modify.undetect.presence': modifyTriggerOnlyHandler,
        'modify.enter': modifyTriggerOnlyHandler,
        'modify.exit': modifyTriggerOnlyHandler,
        'modify.tap': modifyTriggerOnlyHandler,

        # trigger-action handlers
        #  - modifyDevicesParameterHandler is a pre-handler that deals with
        #    whether the required parameter (devices) is present or not.
        'modify.enable': modifyDevicesParameterHandler,
        'modify.disable': modifyDevicesParameterHandler,
        'modify.close-lock': modifyDevicesParameterHandler,
        'modify.open-unlock': modifyDevicesParameterHandler,

        # parameter-change handlers
        'modify.decrease': modifyNumericParameterHandler,
        'modify.decrease.brightness': modifyNumericParameterHandler,
        'modify.decrease.humidity': modifyNumericParameterHandler,
        'modify.decrease.temperature': modifyNumericParameterHandler,
        'modify.decrease.volume': modifyNumericParameterHandler,
        'modify.increase': modifyNumericParameterHandler,
        'modify.increase.brightness': modifyNumericParameterHandler,
        'modify.increase.humidity': modifyNumericParameterHandler,
        'modify.increase.temperature': modifyNumericParameterHandler,
        'modify.increase.volume': modifyNumericParameterHandler,
        'modify.set': modifyNumericParameterHandler,
        'modify.set.brightness': modifyNumericParameterHandler,
        'modify.set.humidity': modifyNumericParameterHandler,
        'modify.set.temperature': modifyNumericParameterHandler,
        'modify.set.volume': modifyNumericParameterHandler
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