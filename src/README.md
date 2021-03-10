# Descriptions on the Class Codes

**Note that some of the classes were not described and the description could be outdated!**

## `Rule.py`
The class `Rule` contains information on a trigger-actions rule.</br>
It is worth noting that there are **actions**, not action.

### Member Variables
- `InstantiatedTrigger trigger` (mandatory)

- `List(InstantiatedAction) actions` (mandatory)

### Methods
- Constructor `Rule(_trigger: InstantiatedTrigger, _actions: list)`

- Static `from_json(filename: str)`

    It reads a json file to load trigger-action rule.</br>
    The specification of json file should be written as follows:
    ```json
    {
        "trigger": {
            "type": "the name of NominalTrigger",
            "params": "required parameters for the trigger"
        },
        "actions": [
            {
                "type": "the name of NominalAction",
                "values": "required values for the action",
                "device": "running device of the action"
            }
        ]
    }
    ```

- `to_json(filename: str)`
    
    It stores the current data into a file with given filename.

- `merge(other: Rule)`

    It merges the given rule into `self`. Existing actions will not be merged to avoid duplicate invocations, and merged actions will be added on the last position.


## `RulesHistory.py`
The class `RulesHistory` contains two important information: (1) the information on the entire rules used for the **given session** and (2) the invocation history of trigger-action pairs.

### Member variables
- `Dictionary(InstantiatedTrigger: Rule) rules` (mandatory)

- `List([the following elements]) history` (mandatory)
    
    It is an ascending-order list of invocation history. The elements are as follows:
    
    - `int timeOffset` (mandatory)
    - `InstantiatedTrigger trigger` (mandatory)
    - `InstantiatedAction action` (mandatory)
    - `list mainEffect` (mandatory)
    - `list sideEffect` (mandatory)
    - `list device` (mandatory)

### Methods
- Constructor `RulesHistory(useTimeOffset=False, baseTimestamp=None)`

    It generates an empty `RulesHistory` object with the given arguments.

    If the `useTimeOffset` is set, the object will be aware of the time offsets while searching TAP rules. The `baseTimestamp` should be set if you are going to use the time offsets.

- Static `from_folder(foldername: str)`

    It reads the data inside the folder with given filename to load the rules and the history data.

- `to_folder(foldername: str)`

    It stores the history data and used rules into csv and json files, respectively.

- `record(rule: Rule, offset=None)`

    It records the given rule into history with the given offset. If the rule is not in the internal dictionary, it will be added / merged.

- `search(implicature: str, checkSideEffect=True, device=None, skipCount=0)`

    It searches the most recently used trigger-action pair with given implicature and device.

    If `checkSideEffect` is set, the search algorithm will check both `mainEffect` and `sideEffect`.

    If `device` hint is set, the search algorithm will also check the action has been performed by matching device.

    If `skipCount` is more than zero, the search algorithm will skip the found history for `skipCount` times. That is, if `skipCount = 1`, the second-most-recent trigger-action pair will be returned. This count will be particulary useful when the user rejected the most recently used pair.

    The return values are in `dict` format, specified as follows:
    ```python
    {
        'exceedThreshold': True if exceeded the time threshold,
        'sideEffect': True if the log found by sideEffect,
        'historyData': None if not found else the row data
    }
    ```