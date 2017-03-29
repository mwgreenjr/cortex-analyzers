`Back to index <index.html>`_

CIRCL Passive SSL
=================
Using username and password provided by CIRCL, their passive SSL service can be queried for:

- ``ip``
- ``hash`` or ``certificate_hash`` (self defined data type)

Configuration
-------------
For configuring the Circl.lu Passive SSL analyzer, the cortex configuration file should include the following values:

.. code-block:: python

    CIRCLPassiveSSL {
        user=""
        password=""
    }


CIRCLPassiveSSLAnalyzer
-----------------------
.. automodule:: circl_passivessl
.. autoclass:: CIRCLPassiveSSLAnalyzer
   :members:
   :private-members:

