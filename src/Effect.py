from .Action import *
import json

def init_effect(file):
    if not bool(NominalAction.actionDict):
        raise AttributeError("Initialize NominalAction.actionDict first.")

    j = json.load(file)
    d = {}

    for k_top, v_top in j.items():
        d[k_top] = {}
        for k_sub, v_sub in v_top.items():
            d[k_top][k_sub] = {
                "MainEffect": [],
                "SideEffect": []
            }

            for action_str in v_sub['MainEffect']:
                NominalAction.actionDict[action_str].mainEffect.append(k_sub)
                d[k_top][k_sub]['MainEffect'].append(NominalAction.actionDict[action_str])

            for action_str in v_sub['SideEffect']:
                NominalAction.actionDict[action_str].sideEffect.append(k_sub)
                d[k_top][k_sub]['SideEffect'].append(NominalAction.actionDict[action_str])
    
    NominalAction.effectDict = d


def strip_str(s):
    if 'High' in s:
        return s[4:]
    else:
        return s[3:]