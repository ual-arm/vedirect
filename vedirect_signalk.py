#!/usr/bin/python

from vedirect import vedirect
import json

key_base = 'electrical.chargers.victron.'

error_codes = {
    0: 'No error',
    2: 'Battery voltage too high',
    17: 'Charger temperature too high',
    18: 'Charger over current',
    19: 'Charger current reversed',
    20: 'Bulk time limit exceeded',
    21: 'Current sensor issue (sensor bias/sensor broken)',
    26: 'Terminals overheated',
    33: 'Input voltage too high (solar panel)',
    34: 'Input current too high (solar panel)',
    38: 'Input shutdown (due to excessive battery voltage)',
    116: 'Factory calibration data lost',
    117: 'Invalid/incompatible firmware',
    119: 'User settings invalid'
    }

def conv_error(code):
    return error_codes[int(code)]

device_state_map= {
    0: 'not charging',
    2: 'fault',
    3: 'charging bulk',
    4: 'charging absorption',
    5: 'charging float'
    }

def conv_mode(code):
    return device_state_map[int(code)]
    
values = {
    'LOAD': { 'key': 'load' },
    'H19': { 'key': 'yieldTotal', 'mx': 0.01 },
    'VPV': { 'key': 'panelVoltage', 'mx': 0.001 },
    'ERR': { 'key': 'error', 'f': conv_error },
    'FW': { 'key': 'firmwareVersion', 'mx': 0.01 },
    'I': { 'key': 'current', 'mx': 0.001 },
    'H21': { 'key': 'maximumPowerToday', 'f': int }, #W
    'IL': { 'key': 'loadCurrent', 'mx': 0.001}, 
    'PID': { 'key': 'productId' },
    'H20': { 'key': 'yieldToday', 'mx': 0.01 }, #kWh
    'H23': { 'key': 'maximumPowerYesterday', 'f': int }, #W
    'H22': { 'key': 'yieldYesterday', 'mx': 0.01 }, #kWh
    'HSDS': { 'key': 'daySequenceNumber', 'f': int },
    'SER#': { 'key': 'serialNumber' },
    'V': { 'key': 'batteryVoltage', 'mx': 0.001 },
    'CS': { 'key': 'mode', 'f': conv_mode} ,
    'PPV': { 'key': 'panelPower', 'f': int }
    }

def print_data_callback(data):
    updates = []
    for k in data.keys():
        if not values.has_key(k):
            continue
        
        info = values[k]
        key = key_base + info['key'] 
        value = data[k]
        if info.has_key('mx'):
            value = float(value) * info['mx']
        elif info.has_key('f'):
            func = info['f']
            value = func(value)

        updates.append({"path": key, "value": value})

        if k == 'CS':
            updates.append({'path': key_base + 'modeValue',
                            'value': int(data[k])})
        
    delta = {
        "updates": [
            {
                "source": {
                    "label": "victron_1"
                },
                "values": updates
            }
        ]
    }
    print json.dumps(delta)

if __name__ == '__main__':
    ve = vedirect('/dev/ve-direct')
    ve.read_data_callback(print_data_callback)

