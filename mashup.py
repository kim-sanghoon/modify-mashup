import argparse, json, pickle

from flask import Flask, request, jsonify
from datetime import datetime

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
setNumber, modifyHistory = None, []
intentDict = {}

ok = lambda d={}: (jsonify({'status': 'ok', **d}), 200)
error = lambda d={}: (jsonify({'status': 'error', **d}), 400)

def saveModificationHistory():
    global modifyHistory

    if modifyHistory:
        time = datetime.now()
        timestamp = int(time.timestamp())

        with open('log/modification/{}-{}.json'.format(timestamp, setNumber), 'wb') as f:
            pickle.dump(modifyHistory, f)
        
        log.debug('Saved current modification history of set #{}.'.format(setNumber))

    modifyHistory = []


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


@app.route('/type', methods=['POST'])
def type():
    req = request.get_json()

    if req is None or 'implicature' not in req:
        log.debug('No implicature data found.')
        return error({
            'what': 'Expected implicature information, received none.'
        })
    
    if 'intent' not in req:
        log.debug('No intent data found.')
        return error({
            'what': 'Expected intent information, received none.'
        })
    
    copyReq = dict(req)
    del copyReq['intent']
    
    searchResult = rulesHistory.search(**copyReq)
    log.debug('Search result - {}'.format(searchResult))

    _, trigger, action, *_ = searchResult['historyData']

    intentData = []
    for nominalName in intentDict[req['intent']]:
        if nominalName in NominalAction.actionDict:
            intentData.append(NominalAction.actionDict[nominalName])
        
        if nominalName in NominalTrigger.triggerDict:
            intentData.append(NominalTrigger.triggerDict[nominalName])

    return ok({
        'trigger': trigger.type.name in intentDict[req['intent']],
        'action': action.type.name in intentDict[req['intent']],
        'intentData': encodeObj(intentData)
    })


@app.route('/modify', methods=['POST'])
def modify():
    req = request.get_json()

    if req is None:
        return error({
            'what': 'No data given.'
        })

    if 'modifyType' not in req or 'implicature' not in req:
        errMsg = 'Expected modifyType and implicature info.'
        log.debug(errMsg)
        return error({'what': errMsg})

    # assert information on the new component is present
    # if the modification type is either replace or append
    if req['modifyType'] in ['replace', 'append'] and 'modifyData' not in req:
        errMsg = 'Expected modifyData info.'
        log.debug(errMsg)
        return error({'what': errMsg})
    
    copyReq = dict(req)
    del copyReq['modifyType']
    if 'modifyData' in req:
        del copyReq['modifyData']
    
    searchResult = rulesHistory.search(**copyReq)
    log.debug('Search result - {}'.format(searchResult))

    if searchResult['historyData'] is None:
        errMsg = 'Expected valid history data, found nothing.'
        log.debug(errMsg)
        return error({'what': errMsg})

    modifyHistory.append([req, searchResult])

    return ok({
        'modifyType': req['modifyType'], 
        'searchResult': encodeObj(searchResult)
    })


@app.route('/undo', methods=['POST'])
def undo():
    global modifyHistory

    if modifyHistory:
        modifyHistory.pop()
    
    return ok({'length': len(modifyHistory)})


@app.route('/<setId>', methods=['GET'])
def changeHistory(setId):
    if not setId.isnumeric() or int(setId) not in [1, 2, 3, 4, 5]:
        return error({
            'what': 'Unexpected number : {}'.format(setId)
        })
    
    saveModificationHistory()
    rulesHistory = RulesHistory.from_folder('data/experiments/' + setId)
    log.debug('Changed the mashup set to #{}'.format(setId))
    setNumber = setId

    return ok({'setId': setId})


@app.route('/', methods=['GET'])
def main():
    global modifyHistory

    listStr = ''
    for item in rulesHistory.history:
        itemStr = str(item[1:3]).replace('<', '').replace('>', '')
        listStr += '<li style="margin: 0.5em 0;">{}</li>\r\n'.format(itemStr)

    modifyListStr = ''
    for item in modifyHistory:
        itemStr = str(item).replace('<', '').replace('>', '')
        modifyListStr += '<li style="margin: 0.5em 0;">{}</li>\r\n'.format(itemStr)
    
    template = '<h3>History Data</h3>\r\n<ol>{}</ol>\r\n<h3>Modifications</h3>\r\n<ol>{}</ol>'
    return template.format(listStr, modifyListStr)


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
    
    with open('data/intents.json') as f:
        intentDict = json.load(f)

    # Load RulesHistory mashup set
    rulesHistory = RulesHistory.from_folder('data/experiments/' + args.number)

    log.debug('Starting the mashup module with mashup set #{}'.format(args.number))
    setNumber, modifyHistory = int(args.number), []
    app.run(host='0.0.0.0', port=445)
