#!/usr/bin/env python3

from flask import Flask, request, jsonify
from datetime import datetime

import sys, json

# Define intent handlers here
from src.handler.dfImplicatureHandler import dfImplicatureHandler
from src.handler.implicatureFollowupHandler import implicatureFollowupHandler

app = Flask(__name__)

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

    print('[info] Current time   : ', str(time.isoformat()))
    print('[info] User intent    : ', str(intent))
    print('[info] Raw user input : ', str(data['queryResult']['queryText']))

    with open('log/dialogflow/{}.json'.format(timestamp), 'w+') as f:
        json.dump(data, f)
    print('[info] Input data has been saved as - {}.json'.format(timestamp))

    sys.stdout.flush()

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
        'implicature.followup.yes': implicatureFollowupHandler,
        'implicature.followup.no': implicatureFollowupHandler
    }

    handler = switch[action]
    ret = handler(data)

    sys.stdout.flush()
    return jsonify(ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=443,
            ssl_context=('server.crt', 'server.key'))