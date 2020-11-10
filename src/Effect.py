from .Action import *
import json

effect_dict = {}

def init_effect(file):
    if not bool(action_dict):
        raise AttributeError("Initialize action_dict first.")

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
                action_dict[action_str].mainEffect.append(k_sub)
                d[k_top][k_sub]['MainEffect'].append(action_dict[action_str])

            for action_str in v_sub['SideEffect']:
                action_dict[action_str].sideEffect.append(k_sub)
                d[k_top][k_sub]['SideEffect'].append(action_dict[action_str])
    
    return d

def strip_str(s):
    if 'High' in s:
        return s[4:]
    else:
        return s[3:]