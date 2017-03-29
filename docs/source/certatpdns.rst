`Back to index <index.html>`_

CERT.AT Passive DNS
==================
This analyzer queries the CERT.AT passive dns whois directory service using a wrapper-construct for the whois commandline client.

Accepted data types are: 

- ``domain`` 

CERT.AT pDNS is not a public service. It is only available for national / governmental CERTs in good standing with CERT.AT. For access, you have to get in contact with CERT.AT.

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
