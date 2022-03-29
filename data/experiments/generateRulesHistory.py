import sys
BASE_PATH = '/home/seiker/modify-mashup' # replace the base path
sys.path.append(BASE_PATH)

from src.Action import *
from src.Trigger import *
from src.Effect import *
from src.Rule import *
from src.RulesHistory import *

import json

def better_print(rh: RulesHistory):
    print('  ---- RULES ----  ')
    for k, v in rh.rules.items():
        print(k, ":", v)
    
    print('\n  ---- HISTORY ----  ')
    for row in rh.history:
        print(row)
    
    print('---------------')

if __name__ == "__main__":
    # init actions
    action_f = open(BASE_PATH + '/data/action.json')
    action_j = json.load(action_f)
    
    for k, v in action_j.items():
        NominalAction(name=k, json_info=v)

    # init triggers
    trigger_f = open(BASE_PATH + '/data/trigger.json')
    trigger_j = json.load(trigger_f)

    for k, v in trigger_j.items():
        NominalTrigger(name=k, json_info=v)
    
    # init effects
    effect_f = open(BASE_PATH + '/data/effects.json')
    init_effect(effect_f)
    
    rulesHistory = RulesHistory(useTimeOffset=False, baseTimestamp=None)

    for i in range(10):
        rule = Rule.from_json('./rule-{}.json'.format(i))
        rulesHistory.record(rule)
    
    rulesHistory.to_folder('generated')
