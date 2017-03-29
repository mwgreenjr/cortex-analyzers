`Back to index <index.html>`_

CERTat Passive DNS
==================
This analyzer queries the CERT.at passive dns whois directory service using a wrapper-construct for the whois commandline client.

Accepted data types are: 

- ``domain`` 

Configuration
-------------
The passive dns analyzer accepts a limit parameter, that shortens (or lengthen) the output, default is 100:

.. code-block:: python

    CERTatPassiveDNS {
        limit="100"
    }


CERTatPassiveDNSAnalyzer
------------------------
.. automodule:: certat_passivedns
.. autoclass:: CERTatPassiveDNSAnalyzer
   :members:
   :private-members:


Whois_wrapper
-------------
.. automodule:: whois_wrapper
   :members:
   :private-members: