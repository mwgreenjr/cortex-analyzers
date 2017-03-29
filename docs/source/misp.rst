`Back to index <index.html>`_

MISP
====
The MISP analyzer is able to query for all available data types. Separated in MISP instances, the analyzer returns all
fitting events including a link to that event, the tags, related events and clusters.

Configuration
-------------
For configuring the MISP analyzer, the cortex configuration file should include the following values:

.. code-block:: python

    MISP {
		url=["https://misp.instance-1.local", "https://misp.instance-2.com"]
		key=["Apikeyno1", "Apikeyno2" ]
		certpath=["/path/to/self/signed/cert/for/verification.pem", ""]
		name=["Instance 1 (private)", "Instance 2 (public)"]
    }

MISPAnalyzer
------------
.. automodule:: misp
.. autoclass:: MISPAnalyzer
   :members:
   :private-members:

MISPClient
----------
.. automodule:: mispclient
.. autoclass:: MISPClient
   :members:
   :private-members:

.. autoclass:: EmptySearchtermError
   :members:
   :private-members:

