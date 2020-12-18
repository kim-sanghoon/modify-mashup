# To run this script, set dir to 'test/' and execute 'python3 testSearchRulesHistory.py'

# If you want to test with time threshold, enable this flag.
TIME_SENSITIVE = False

import sys
sys.path.append('..')

from src.Action import *
from src.Trigger import *
from src.Effect import *
from src.Rule import *
from src.RulesHistory import *

import json, random, time, os

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

    # (-1) if time sensitive, prepare enabling time
    try:
        os.remove('testSearchRulesHistory/timestamp.txt')
    except FileNotFoundError:
        pass # it's okay

    if TIME_SENSITIVE:
        with open('testSearchRulesHistory/timestamp.txt', 'w') as f:
            f.write(str(int(time.time()) - 1200))
    
    # (0) initialize test set
    rh = RulesHistory.from_folder('testSearchRulesHistory')

    if TIME_SENSITIVE:
        for row in rh.history:
            row[0] *= 100

    better_print(rh)

    # (1) search test with time check
    t0 = time.time()

    print(rh.search('HighNoise'))
    print(rh.search('HighNoise', checkSideEffect=False))
    print(rh.search('HighNoise', device='dish washer'))
    print(rh.search('HighNoise', skipCount=2))
    print(rh.search('HighNoise', skipCount=4))

    t1 = time.time()
    print(t1 - t0)