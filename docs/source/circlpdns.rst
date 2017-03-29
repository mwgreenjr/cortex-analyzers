`Back to index <index.html>`_

CIRCL Passive DNS
=================
Using username and password provided by CIRCL, their passive DNS service can be queried for:

- ``domain``
- ``url`` (gets cut to domain)

Configuration
-------------
For configuring the Circl.lu Passive DNS analyzer, the cortex configuration file should include the following values:

.. code-block:: python

    CIRCLPassiveDNS {
        user=""
        password=""
    }


CIRCLPassiveDNSAnalyzer
-----------------------
.. automodule:: circl_passivedns
.. autoclass:: CIRCLPassiveDNSAnalyzer
   :members:
   :private-members:

