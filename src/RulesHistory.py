from .Trigger import *
from .Action import *
from .Effect import strip_str, inverse_str
from .Rule import *
from logger import get_logger

import csv, os, re, time

class RulesHistory:
    def __init__(self, useTimeOffset=False, baseTimestamp=None):
        # assert all the required elements are loaded.
        assert len(NominalTrigger.triggerDict) > 0
        assert len(NominalAction.actionDict) > 0
        assert len(NominalAction.effectDict) > 0

        self.rules = {}
        self.history = []
        self.useTimeOffset = useTimeOffset
        self.log = get_logger()

        if useTimeOffset:
            assert baseTimestamp is not None
            self.baseTimestamp = baseTimestamp
    
    def __eq__(self, other):
        isEqual = (self.rules == other.rules and self.history == other.history)
        isEqual = isEqual and (self.useTimeOffset == other.useTimeOffset)
        if self.useTimeOffset:
            isEqual = isEqual and (self.baseTimestamp == other.baseTimestamp)

        return isEqual
    
    def __ne__(self, other):
        return not(self == other)
    
    @staticmethod
    def from_folder(foldername: str):
        useTimeOffset, baseTimestamp = False, None
        if os.path.exists(foldername + '/timestamp.txt'):
            useTimeOffset = True
            with open(foldername + '/timestamp.txt', 'r') as timestampFile:
                baseTimestamp = int(timestampFile.read().rstrip())
        
        rh = RulesHistory(useTimeOffset=useTimeOffset, baseTimestamp=baseTimestamp)

        ruleFilenameList = [r for r in os.listdir(foldername) if re.search(r'^rule', r)]
        for ruleFilename in ruleFilenameList:
            rule = Rule.from_json(foldername + '/' + ruleFilename)
            rh.rules[rule.trigger] = rule

        # repr(Instantiated*) to Instantiated* dictionary for faster searching
        triggerReprDict = {}
        actionReprDict = {}

        for rule in rh.rules.values():
            triggerReprDict[repr(rule.trigger)] = rule.trigger
            for action in rule.actions:
                actionReprDict[repr(action)] = action

        # now, start loading history data
        with open(foldername + '/history.csv', 'r') as historyFile:
            csvReader = csv.reader(historyFile)
            next(csvReader)

            for row in csvReader:
                trigger = triggerReprDict[row[1]]
                action = actionReprDict[row[2]]

                rh.history.append([
                    int(row[0]),
                    trigger,
                    action,
                    action.type.mainEffect,
                    action.type.sideEffect,
                    action.device
                ])
        
        return rh

    def to_folder(self, foldername: str):
        os.makedirs(foldername, exist_ok=True)

        if self.useTimeOffset:
            with open(foldername + '/timestamp.txt', 'w') as timestampFile:
                timestampFile.write(str(self.baseTimestamp))
        
        i = 0
        for rule in self.rules.values():
            rule.to_json(foldername + '/rule-{}.json'.format(i))
            i += 1

        with open(foldername + '/history.csv', 'w') as historyFile:
            csvWriter = csv.writer(historyFile)
            csvWriter.writerow(('timeOffset', 'trigger', 'action'))

            for row in self.history:
                csvWriter.writerow(row[0:3])
        
        self.log.debug('RulesHistory object is saved to ./{}/'.format(foldername))

    def record(self, rule: Rule, offset=None):
        if self.useTimeOffset:
            assert offset is not None
        else:
            offset = 1 if len(self.history) == 0 else self.history[-1][0] + 1
        
        # if the rule is not on the dictionary, it is inserted.
        if rule.trigger not in self.rules:
            self.rules[rule.trigger] = rule
        
        # if a different rule with the same trigger, merge it with the existing one.
        if rule.trigger in self.rules and self.rules[rule.trigger] != rule:
            self.rules[rule.trigger].merge(rule)
        
        for action in rule.actions:
            self.history.append([
                offset,
                rule.trigger,
                action,
                action.type.mainEffect,
                action.type.sideEffect,
                action.device
            ])
            offset += 1

    def search(self, implicature: str, checkSideEffect=True, device=None, skipCount=0):
        ret = {
            'exceedThreshold': False,
            'sideEffect': False,
            'historyData': None
        }

        if self.useTimeOffset:
            # if the offset value of a history log is less than the threshold,
            # the log is more than {time-threshold} old.
            implicatureThreshold = {
                'AirQuality': 4800,
                'Brightness': 300,
                'Humidity': 4800,
                'Noise': 600,
                'Security': 10800,
                'Temperature': 7200
            }
            thresholdOffset = int(time.time()) - self.baseTimestamp - implicatureThreshold[strip_str(implicature)]
        
        for row in reversed(self.history):
            if self.useTimeOffset and row[0] < thresholdOffset:
                ret['exceedThreshold'] = True # exceeded the time threshold
            
            if implicature in row[3] or inverse_str(implicature) in row[3]:                
                if device is not None and device != row[5]:
                    continue

                if skipCount > 0:
                    skipCount -= 1
                    continue

                # handle if both implicature and inverse implicature exist on row[3]
                # check the description on search() on README.md for further details
                if implicature in row[3] and inverse_str(implicature) in row[3]:
                    low = implicature if implicature.startswith('Low') else inverse_str(implicature)
                    high = inverse_str(low)

                    row[3] = list(row[3]) # shallow copy the items

                    normValues = []
                    for k, v in row[2].values.items():
                        minval, maxval = row[2].type.valuesRange[k]
                        normValues.append((v - minval) / (maxval - minval))
                    
                    if sum(normValues) / len(normValues) < 0.5:
                        row[3].remove(high)
                    else:
                        row[3].remove(low)

                ret['historyData'] = row
                return ret # success with mainEffect
            
            if checkSideEffect and implicature in row[4]:
                if device is not None and device != row[5]:
                    continue

                if skipCount > 0:
                    skipCount -= 1
                    continue

                ret['sideEffect'] = True
                ret['historyData'] = row
                return ret # success with sideEffect
        
        return ret # search failed
