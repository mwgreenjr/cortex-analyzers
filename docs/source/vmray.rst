`Back to index <index.html>`_

VMRay
=====
This analyzer handles ``file`` and ``hash`` inputs for searching in/uploading to VMRay. Unfortunately, VMRay just retuns
an error when uploading an already available sample. According to the devs, they will provide a new API in the future.
At the moment, you either accept the "error"message or just force reanalyzation of the sample.

Configuration
-------------
For configuring the VMRay analyzer, the cortex configuration file should include the following values:

.. code-block:: python

    VMRay {
    	url="https://vmray.instance.de"
    	key="APIKEY"
    	certpath="/path/to/verification/cert.pem"
    	disablereanalyze="false"
    }

VMRayAnalyzer
-------------
.. automodule:: vmray
.. autoclass:: VMRayAnalyzer
   :members:
   :private-members:

VMRayClient
-----------
.. automodule:: vmrayclient
.. autoclass:: VMRayClient
   :members:
   :private-members:

.. autoclass:: VMRayClientError
   :members:
   :private-members:

.. autoclass:: UnknownHashTypeError
   :members:
   :private-members:

.. autoclass:: BadResponseError
   :members:
   :private-members:

.. autoclass:: SampleFileNotFoundError
   :members:
   :private-members:


