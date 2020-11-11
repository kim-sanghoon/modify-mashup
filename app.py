#!/usr/bin/env python3

from flask import Flask, request, jsonify
from datetime import datetime

import sys, json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    data   = request.get_json()
    intent = data['queryResult']['intent']['displayName']

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
        # 'intent' : function
    }

    handler = switch[intent]
    ret = handler()

    sys.stdout.flush()
    return jsonify(ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=443,
            ssl_context=('server.crt', 'server.key'))