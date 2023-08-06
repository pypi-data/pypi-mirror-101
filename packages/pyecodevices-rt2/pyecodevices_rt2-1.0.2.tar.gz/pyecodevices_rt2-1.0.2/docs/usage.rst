=====
Usage
=====

To use pyecodevices-rt2 in a project::

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
