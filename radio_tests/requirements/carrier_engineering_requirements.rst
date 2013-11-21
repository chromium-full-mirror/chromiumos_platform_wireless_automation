
Carrier Engineering Requirements
=================================

Subsections:
-------------

Activate their cellular account & service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enable the cellular modem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Tested By:
    :class:`cellular_smoke.CellularSmoke`

:Description:
    * Turn the modem on, and verify it's up.
    * This downloads a small html file from a local webserver over the LTE link.

Disable the cellular modem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:Tested By:
    :class:`cellular_smoke.CellularSmoke`

:Description:
    * Turn the modem off, and ensure the disconnect message is received by the call box.

Connect to a CDMA/UMTS/LTE network
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:Tested By:
    :class:`cellular_smoke.CellularSmoke`

:Description:
        * Connect to a network.


Disconnect from the cellar network
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:Tested By:
    :class:`cellular_smoke.CellularSmoke`

:Description:
        * Disconnect from the cellular network.


Download data via the cellular connection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:Tested By:
        :class:`cellular_smoke.CellularSmoke`

:Description:
        * Download data over the cellular network.


Upload data via the cellular connection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:Tested By:
        :class:`cellular_smoke.CellularSmoke`

:Description:
        * Upload data over the cellular network.


Lock their SIM card via a PIN
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unlock their SIM card via a PIN
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unlock their SIM card via a PUK code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Determine their signal strength
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Determine their connection technology
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Determine their international roaming status
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enable roaming
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Disable roaming
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set their APN details ^ APN, username & password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update their PRL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Receive a notification when they are out of credit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Receive an SMS notification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Successfully maintain a connection during a 2G <^> 3G tower handover
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Navigate to their account management page via the "View Account" link
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Switch the modem firmware to connect to different CDMA carriers and UMTS networks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Reset the modem to the factory state.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:Tested By:
        :class:`cellular_smoke.CellularSmoke`

:Description:
            * Reset the modem.

