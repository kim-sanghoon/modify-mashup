# To run this script, set dir to 'test/' and execute 'python3 testTimedRule.py'
# This test is only for "time"-related triggers.

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
    
    timeTrigger = InstantiatedTrigger(
        _type=NominalTrigger.triggerDict['EveryDayTrigger'],
        _random=True
    )
    random_action = lambda : InstantiatedAction(random.choice(list(NominalAction.actionDict.values())), _random=True)

    testRule = Rule(timeTrigger, [random_action() for _ in range(random.randint(1, 5))])
    print(testRule) # is it properly generated?

    testRule.to_json('test-timed-rule.json') # is it properly saved?

    reloadRule = Rule.from_json('test-timed-rule.json')
    print(reloadRule) # is it properly loaded?

    # check the time data is actually a Time object
    print(type(reloadRule.trigger.params['time']))
    
# After running the script, don't forget to delete 'test-rule-*.json' files :)
