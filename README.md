
Config for use with signalk-node-server

```
    {                                                                           
      "id": "victron_1",                                                        
      "pipeElements": [{                                                        
        "type": "providers/execute",                                            
        "options": {                                                            
          "command": "python /home/sbender/vedirect/vedirect_signalk.py"        
        }                                                                       
      }, {                                                                      
        "type": "providers/liner"                                                                                                                 
      }, {                                                                      
        "type": "providers/from_json"                                           
      }]                                                                        
    },                                                                          
```

Sample signalk full tree

```
    "chargers": {
      "victron": {
        "batteryVoltage": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.979Z", 
          "value": 13.530000000000001
        }, 
        "current": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.987Z", 
          "value": 0
        }, 
        "daySequenceNumber": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.993Z", 
          "value": 6
        }, 
        "error": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.985Z", 
          "value": "No error"
        }, 
        "firmwareVersion": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.986Z", 
          "value": 1.19
        }, 
        "load": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.982Z", 
          "value": "OFF"
        }, 
        "loadCurrent": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.988Z", 
          "value": 0
        }, 
        "maximumPowerToday": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.987Z", 
          "value": 64
        }, 
        "mode": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.980Z", 
          "value": "not charging"
        }, 
        "panelPower": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.981Z", 
          "value": 0
        }, 
        "panelVoltage": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.984Z", 
          "value": 1
        }, 
        "productId": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.989Z", 
          "value": "0xA043"
        }, 
        "serialNumber": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.994Z", 
          "value": "HQ1546SXL7S"
        }, 
        "yieldToday": {
          "$source": "victron_1.XX", 
          "value": 0.14
        }, 
        "yieldTotal": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.983Z", 
          "value": 0.76
        }, 
        "yieldYesterday": {
          "$source": "victron_1.XX", 
          "timestamp": "2017-02-10T03:43:31.992Z", 
          "value": 0.25
        }
      }
    }
  }, 
```

Using the vedirect class.

```
$ sudo python vedirect.py 
{'LOAD': 'ON', 'H19': '0', 'VPV': '0', 'ERR': '0', 'FW': '112', 'I': '0', 'H21': '0', 'PID': '0xA042', 'H20': '0', 'H23': '0', 'H22': '0', 'SER#': 'HQ1411?????', 'V': '12740', 'CS': '0', 'PPV': '0'}

{'LOAD': 'ON', 'H19': '0', 'VPV': '0', 'ERR': '0', 'FW': '112', 'I': '0', 'H21': '0', 'PID': '0xA042', 'H20': '0', 'H23': '0', 'H22': '0', 'SER#': 'HQ1411?????', 'V': '12740', 'CS': '0', 'PPV': '0'}

{'LOAD': 'ON', 'H19': '0', 'VPV': '0', 'ERR': '0', 'FW': '112', 'I': '0', 'H21': '0', 'PID': '0xA042', 'H20': '0', 'H23': '0', 'H22': '0', 'SER#': 'HQ1411?????', 'V': '12740', 'CS': '0', 'PPV': '0'}
```

Using the vedirectsim simulator.

Create a pair of virtual serial ports which transfer data between each other.

```
$ socat -d -d PTY,raw,echo=0,link=/tmp/vmodem0 PTY,raw,echo=0,link=/tmp/vmodem1
```

Connect vedirect.py to /tmp/vmodem1 and vedirectsim.py to /tmp/vmodem0
