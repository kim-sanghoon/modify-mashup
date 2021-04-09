# Descriptions on the Data

There are four main files in this folder: `action.json`, `effects.json`, `intents.json`, and `trigger.json`.<br />
I briefly describe how each file is organized.

## `action.json`
This file contains properties of each nominal action.

### JSON Specification
An action specified in the file is shown as follows:
```json
{

    "IncreaseVolumeAction": {
        "inverseOf": "DecreaseVolumeAction",
        "type": "number",
        "values": ["volume"],
        "valuesRange": {
            "volume": [10, 100]
        },
        "language": {
            "past": "the volume was increased to {volume} percent",
            "gerund": "increasing the volume to {volume} percent",
            "increase": "increasing the volume to {volume} percent",
            "infinitive": "increase the volume to {volume} percent"
        },
        "device": ["audio", "tv"]
    },

}
```
- Property `inverseOf` (mandatory)
    
    This property indicates the inversive action of the action. For example, the inversive action of `EnableLightingSystemAction` is set to `DisableLightingSystemAction`. Using this property, users can invalidate the effect caused by actions.

    If there is no inversive action for an action, the property shall indicate itself. Please refer `SetLightingAction` for an example.

- Property `type` (mandatory)

    This property indicates the type of the action. There are only two types for the actions: `bool` and `number`. 
    
    Boolean actions generally have their `inverseOf` counterpart while numeric actions do not. However, there are some expections such as `IncreaseVolumeAction` as shown above.

- List `values` (mandatory)

    This list contains parameters required to operate the action.

- Dict `valuesRange` (optional)

    This dictionary contains the expected range of each values listed in `values`. The keys of the dict shall be an element of `values`, and the values shall be a list of two elements: the minimum and the maximum.

    This dictionary is intended to generate an `InstantiatedAction` object without a user input. Thus, the minimum and the maximum defined in this dict does not represent that a user input should be inside the range.

    This dictionary is mandatory only if there are one or more elements in `values` (that is, it is optional if the type is `bool`).

- Dict `language` (mandatory)

    This dictionary contains the natural language representation of the action.
    
    Currently, there are three mandatory elements and two optional elements in this dictionary.
    
    - `past` (mandatory)
    
    - `gerund` (mandatory)

    - `infinitive` (mandatory)

    - `increase` (optional, only shown in numeric-type actions)

    - `decrease` (optional, only shown in numeric-type actions)

- List `device` (mandatory)

    This list contains the related IoT devices to the action. An element of the list shall be an entity of `devices` Dialogflow entities.

### Test Code
```python
from src.Action import *
import json

if __name__ == "__main__":
    action_f = open('./data/action.json')
    action_j = json.load(action_f)
    
    for k, v in action_j.items():
        NominalAction(name=k, json_info=v)

    print(NominalAction.actionDict)
```

## `effects.json`
There are six abstract environmental variables in this file: `AirQuality`, `Brightness`, `Humidity`, `Noise`, `Security`, and `Temperature`. Each variable is divided into two levels: Low and High.

An environmental variable specified in the file is shown as follows:

```json
{

    "AirQuality": {
        "HighAirQuality": {
            "MainEffect": [
                "EnableAirPurifierSystemAction"
            ],
            "SideEffect": [
                "OpenWindowFrameAction",
                "CloseWindowFrameAction"
            ]
        },
        "LowAirQuality": {
            "MainEffect": [
                "DisableAirPurifierSystemAction"
            ],
            "SideEffect": [
                "OpenWindowFrameAction",
                "CloseWindowFrameAction"
            ]
        }
    },

}
```

For each level of a variable, there are two categories of actions classification: `MainEffect` and `SideEffect`.<br />
The invocation of an action defined in `MainEffect` will cause the environment variable low or high. For example, `EnableAirPurifierSystemAction` is defined in `MainEffect` of `HighAirQuality` level. It represents that turning the air purifier on will make the air quality high.<br />
There is no guarantee, but the invocation of an action defined in `SideEffect` also could affect the environment variable. For example, `OpenWindowFrameAction` is defined in `SideEffect` of `HighAirQuality` level. That is, opening the windows could potentially make the air quality high. 

### Test Code
Notice that `action.json` should be properly loaded in advance to test `effect.json`.
```python
from src.Action import *
from src.Effect import *
import json

if __name__ == "__main__":
    action_f = open('./data/action.json')
    action_j = json.load(action_f)
    
    for k, v in action_j.items():
        NominalAction(name=k, json_info=v)
    
    effect_f = open('./data/effects.json')

    init_effect(effect_f)
    print(NominalAction.effectDict)
```

## `intents.json`
This file contains mappings between Google Dialogflow intents (more precisely, actions) and corresponding EUPont trigger / action classes.
As [the recommended naming convention of Dialogflow](https://cloud.google.com/dialogflow/cx/docs/concept/best-practices) is to segment intent names with punctuation.

### JSON Specification
Examples of the mappings are shown as follows:
```json
{
    "modify.open-unlock": [
        "OpenWindowFrameAction",
        "DisableSecuritySystemAction",
        "WindowFrameOpenedTrigger",
        "SecuritySystemDisabledTrigger"
    ],
    "modify.receive.call": [
        "ReceivedIncomingCallTrigger"
    ],
}
```

All the intents that are only mapped with triggers have only one mapping in the list, while the others have multiple mappings.

## `trigger.json`
This file contains properties of each nominal trigger.

### JSON Specification
A trigger specified in the file is shown as follows:
```json
{

    "EveryYearTrigger": {
        "params": {
            "month": {
                "type": "string",
                "followup": "Which month do you want to trigger in?"
            },
            "day": {
                "type": "number",
                "followup": "Which day do you want to trigger at?"
            }
        },
        "paramsRange": {
            "month": [
                "January", "February", "March", "April", 
                "May", "June", "July", "August", 
                "September", "October", "November", "December"
            ],
            "day": [1, 28]
        },
        "language": {
            "present": "the date is {month} {day}",
            "past": "the date was {month} {day}",
            "short": "on {month} {day}"
        }
    },

}
```
- Dict `params` (mandatory)

    This dictionary contains parameters required to invoke the trigger. The key of the dictionary shall the name of parameters, and the value shall be the dictionary containing the following properties.
    
    - Property `type` (mandatory) : It indicates the type of the parameter. The `type` should be exactly one of the followings: `number`, `string`, or `time`.

    - Property `followup` (mandatory) : It is used to ask the parameter value when the user did not provided the required parameter.

    If there is no parameter required for the trigger, `params` should be an empty dictionary.

- Dict `paramsRange` (mandatory)

    This dictionary contains example values for each parameter. The key of the dictionary shall be the name of parameters, and the value shall be the list containing information on the parameter value.
    
    - If the type of the parameter is `string`, the value list should contain some examples of the parameter value.

    - If the type is `number` or `time`, the value list should contain the recommended minimum and the maximum of the parameter value.

    This dictionary is intended to generate an `InstantiatedTrigger` object without a user input. Thus, the values defined in this dict does not represent that a user input should be inside the range.

    If there is no parameter required for the trigger, `paramsRange` should be an empty dictionary.

- Dict `language` (mandatory)

    This dictionary contains the natural language representation of the trigger.
    
    Currently, there are two mandatory elements and one optional element in this dictionary.
    
    - `present` (mandatory)
    
    - `past` (mandatory)

    - `short` (optional)

### Notes

- `ConnectionToNetworkTrigger`

    There could be parameters to specify which network to be triggered at, but I assume that there is only one home network for the simplicity.

- `ReceivedBreakingNewsTrigger`

    I found that this category has so many different types of trigger individuals, and triggers related to weather forecast (such as `triggerweathercurrentconditionchangesto`) are also in this category. To solely focus on the smart-home-related stuffs, I regarded this type as some weather forecast trigger.

### Test Code
```python
from src.Trigger import *
import json

if __name__ == "__main__":
    trigger_f = open('./data/trigger.json')
    trigger_j = json.load(trigger_f)

    for k, v in trigger_j.items():
        NominalTrigger(name=k, json_info=v)
    
    print(NominalTrigger.triggerDict)
    
    for k, v in NominalTrigger.triggerDict.items():
        iActions = [InstantiatedTrigger(v, _random=True) for _ in range(5)]
        print(iActions)
```
