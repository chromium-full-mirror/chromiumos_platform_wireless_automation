
Rf Performance Requirements:
============================


Basic module verification:
---------------------------

Provisioning the modem should work
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Modem should connect to Verizon live network
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Does the link work
:class:`cellular_smoke.CellularSmoke`


Interaction of RF module with rest of the chromebook:
------------------------------------------------------

desense (does chromebook generated nose block any channels)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ACLR should be passing in corner cases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(does the lowest voltage cause a PA linearity decrease)

Total Radiated Power should pass (is there an antenna impedance mismatch)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Basic Stability:
-----------------
Max download test (short time period, best case environment, call box)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stability at max download (many days)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Does Shill and ModemManager track states
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


