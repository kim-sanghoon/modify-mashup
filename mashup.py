import argparse

from flask import Flask, request, jsonify

from src.Action import *
from src.Trigger import *
from src.Effect import *
from src.Rule import *
from src.RulesHistory import *
from src.utils.encodeTools import encodeObj
from logger import get_logger


app = Flask(__name__)
log = get_logger(name='mashup')
rulesHistory = None

ok = lambda d={}: (jsonify({'status': 'ok', **d}), 200)
error = lambda d={}: (jsonify({'status': 'error', **d}), 400)


@app.route('/check', methods=['GET'])
def check():
    if rulesHistory is not None:
        log.debug('Received health check, sent okay.')
        return ok()
    else:
        log.debug('Received health check, sent error.')
        return error()


@app.route('/search', methods=['POST'])
def search():
    req = request.get_json()

    if req is None or 'implicature' not in req:
        log.debug('No implicature data found.')
        return error({
            'what': 'Expected implicature information, received none.'
        })
    
    searchResult = rulesHistory.search(**req)
    log.debug('Search result - {}'.format(searchResult))
    return ok({'searchResult': encodeObj(searchResult)})


if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description='Mashup management module')
    argParser.add_argument('--number', required=True,
        help='Specify the number of mashup set. (1 - 5)'
    )
    args = argParser.parse_args()

    if int(args.number) not in [1, 2, 3, 4, 5]:
        raise RuntimeError('Unexpected number: {}'.format(args.number))

    # Load actions, triggers, and effects
    with open('data/action.json') as f:
        j = json.load(f)

        for k, v in j.items():
            NominalAction(name=k, json_info=v)
    
    with open('data/trigger.json') as f:
        j = json.load(f)

        for k, v in j.items():
            NominalTrigger(name=k, json_info=v)

    with open('data/effects.json') as f:
        init_effect(f)

    # Load RulesHistory mashup set
    rulesHistory = RulesHistory.from_folder('data/experiments/' + args.number)

    log.debug('Starting the mashup module with mashup set #{}'.format(args.number))
    app.run(host='0.0.0.0', port=445)