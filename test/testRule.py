# To run this script, set dir to 'test/' and execute 'python3 testRule.py'

import sys
sys.path.append('..')

from src.Action import *
from src.Trigger import *
from src.Rule import *

import json, random

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
    
    random_trigger = lambda : InstantiatedTrigger(random.choice(list(NominalTrigger.triggerDict.values())), _random=True)
    random_action = lambda : InstantiatedAction(random.choice(list(NominalAction.actionDict.values())), _random=True)

    # for i in range(5):
    #     print('  ---- ITERATION {} ----  '.format(i))
    #     testRule = Rule(random_trigger(), [random_action() for _ in range(random.randint(1, 5))])
    #     print(testRule) # is it properly generated?

    #     testRule.to_json('test-rule-{}.json'.format(i)) # is it properly saved?

    #     reloadRule = Rule.from_json('test-rule-{}.json'.format(i))
    #     print(reloadRule) # is it properly loaded?
    
    # (12/15) test for merge() method
    for i in range(5):
        print('  ---- ITERATION {} ----  '.format(i))

        sameTrigger = random_trigger()

        thisRule = Rule(sameTrigger, [random_action() for _ in range(random.randint(1, 5))])
        thatRule = Rule(sameTrigger, [random_action() for _ in range(random.randint(1, 5))])

        print(thisRule)
        print(thatRule)
        thisRule.merge(thatRule)
        print(thisRule)
        thisRule.merge(thatRule) # nothing happens
        print(thisRule)
    
# After running the script, don't forget to delete 'test-rule-*.json' files :)
