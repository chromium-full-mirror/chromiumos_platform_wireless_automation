QA Tests
=========

1.7.22 SMS message when disconnected from mobile network 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.23 SMS message over mobile network 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:Tested By:
    * network_ModemManagerSMS
    * network_ModemManagerSMSSignal

1.7.24 SMS message exceeding maximum characters 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.25 SMS message less than maximum characters 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


1.7.39 Auto-connect to Cellular Network (CDMA/GSM)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:Tested By:
    * network_3GAssociation

1.7.43 Cellular works after re-imaging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


1.7.44 Default APN values are used for cellular network [tcm:11560504] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


1.7.46 GSM PIN: Locked PIN handling [tcm:6813313] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:Tested By:
    * network_SIMLocking

1.7.47 GSM PIN: PIN Change (Reboot) [tcm:6854026] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:
    *  network_SIMLocking

1.7.48 GSM PIN: PUK Handling [tcm:16112346] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:
    *  network_SIMLocking

1.7.49 GSM: APN Settings [tcm:9286234] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.50 GSM: PIN Disable [tcm:6844293] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:
    *  network_SIMLocking

1.7.51 GSM: PIN Enable [tcm:6824322] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:
    *  network_SIMLocking

1.7.52 GSM: Reboot [tcm:6818290] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:
    *  network_3GRebootStress

1.7.53 GSM: Suspend Resume [tcm:6811013] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:

    *  network_MobileSuspendResume

1.7.55 Long SMS messages [tcm:16132144] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.56 modem factory-reset works [tcm:16207140] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.57 Modem with no SIM inserted [tcm:16094118] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.58 modem_set_carrier works in crosh on gobi modems [tcm:11561426] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:

    *  network_SwitchCarrier

1.7.60 Prioritize WiFi over WiMAX [tcm:18437096] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.65 Roaming option must be enabled for roaming to work [tcm:11549638] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.66 SIM with no plan associated with it [tcm:16093265] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.67 Suspend: Disconnect from Cellular network when device suspends/sleeps tcm:3705005
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:

    * network_MobileSuspendResume

1.7.69 Transition: Device prefers ethernet over cellular [tcm:3652006] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.70 Transition: Device prefers wifi over cellular [tcm:3640007] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.71 Transition: Disable cellular shall gracefully disconnect from 3G network. [tcm:3723003] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:

    *  network_3GDisableWhileConnecting

1.7.72 Transition: Disconnecting from Ethernet LAN automatically connects to selected Cellular network.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.7.72 Transition: Disconnecting from Ethernet LAN automatically connects to selected Cellular network.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:


1.7.73 User can Connect and Disconnect from Mobile network [tcm:4680201] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:
   *  network_3GDisableGobiWhileConnecting,
   *  network_3GDormancyDance
   *  network_3GModemControl
   *  network_3GSmokeTest
   *  network_ChromeCellularSmokeTest

1.7.75 User can successfully download large files [tcm:12152365] 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

