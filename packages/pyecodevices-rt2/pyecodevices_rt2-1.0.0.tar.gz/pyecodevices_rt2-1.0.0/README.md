# pyecodevices_rt2 - Python [GCE Ecodevices RT2](http://gce-electronics.com/fr/home/1345-suivi-consommation-ecodevices-rt2-3760309690049.html)

Get information from [GCE Ecodevices RT2](http://gce-electronics.com/fr/home/1345-suivi-consommation-ecodevices-rt2-3760309690049.html)
This work is originally developed for use with [Home Assistant](https://www.home-assistant.io/) and the *custom component* [ecodevices_rt2](https://github.com/pcourbin/ecodevices_rt2).
This work is based on the work of [Aohzan](https://github.com/Aohzan/pyecodevices).

## Parameters

- `host`: ip or hostname
- `port`: (default: 80)
- `apikey`: if authentication enabled on Ecodevices RT2
- `timeout`: (default: 3)

## Properties

- `host`: return the host
- `apikey`: return the apikey
- `apiurl`: return the default apiurl

## Methods

- `ping`: return true if the Ecodevices answer
- `get`: return json or part of json from the API and parameters according to [Ecodevices RT2 API](https://gce.ovh/wiki/index.php?title=API_EDRT) (or [PDF](https://forum.gce-electronics.com/uploads/default/original/2X/1/1471f212a720581eb3a04c5ea632bb961783b9a0.pdf)) 

## Example

```python
from pyecodevices_rt2 import EcoDevicesRT2

ecodevices = EcoDevicesRT2('192.168.0.20','80',"mysuperapikey")

print("# ping")
print(ecodevices.ping())
print("# Default API call")
print(ecodevices.apiurl)

# Indexes
print("# All Indexes")
print(ecodevices.get('Index','All'))
print("# Only Index 'Index_TI1'")
print(ecodevices.get('Index','All','Index_TI1'))

# Powers
print("# Actual power on 'POSTE5'")
print(ecodevices.get('Get','P','INSTANT_POSTE5'))

# EnOcean
print("# All Enocean")
print(ecodevices.get('Get','XENO'))
print("# Set Enocean1 and get status")
print(ecodevices.get('SetEnoPC','1','status'))
print("# Clear Enocean2 and get status")
print(ecodevices.get('ClearEnoPC','2','status'))

# Heaters / FP Modules
print("# Current state of all zones")
print(ecodevices.get('Get','FP'))
print("# Current state of First Zone of First FP module")
print(ecodevices.get('Get','FP', 'FP1 Zone 1'))
print("# Force First Zone of First FP module to be on 'Confort' mode and get status")
print(ecodevices.get('SetFP01','0', 'status'))
```
