# To run this script, set dir to 'test/' and execute 'python3 testFileIORulesHistory.py'

import sys
sys.path.append('..')

from src.Action import *
from src.Trigger import *
from src.Effect import *
from src.Rule import *
from src.RulesHistory import *

import json, random

def random_trigger():
    return InstantiatedTrigger(random.choice(list(NominalTrigger.triggerDict.values())), _random=True)

def random_action():
    return InstantiatedAction(random.choice(list(NominalAction.actionDict.values())), _random=True)

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
    action_f = open('../data/action.json')
    action_j = json.load(action_f)
    
    for k, v in action_j.items():
        NominalAction(name=k, json_info=v)

    # init triggers
    trigger_f = open('../data/trigger.json')
    trigger_j = json.load(trigger_f)

    for k, v in trigger_j.items():
        NominalTrigger(name=k, json_info=v)
    
    # init effects
    effect_f = open('../data/effects.json')
    init_effect(effect_f)
    
    # (0) initialize an object
    rulesHistory = RulesHistory(useTimeOffset=False, baseTimestamp=None)

    for i in range(5):
        print('  ---- ITERATION {} ----  '.format(i))
        testRule = Rule(random_trigger(), [random_action() for _ in range(random.randint(1, 5))])
        print(testRule)

        # (1) record a rule
        rulesHistory.record(testRule)
    
    better_print(rulesHistory)

    # (2) save a ruleshistory
    rulesHistory.to_folder('testRulesHistory')

    # (3) load the ruleshistory
    anotherRH = RulesHistory.from_folder('testRulesHistory')

    better_print(anotherRH)

    print('equal' if rulesHistory == anotherRH else 'not equal')

