`Back to index <index.html>`_

Google Safebrowsing
===================
The Google Safebrowsing analyzer is able to query for urls. You need to register a Google account and activate the
specific API in the console as mentioned `here <https://developers.google.com/safe-browsing/v4/get-started>`_.

Lists are chosen using the following values:

- ``threatTypes``
   - malware
   - social engineering
   - unwanted software
   - potentially harmful application
- ``platformTypes``
   - any platform
   - all platforms
   - windows
   - linux
   - osx
   - android
   - ios

Configuration
-------------
For configuring the Google Safebrowsing analyzer, the cortex configuration file should include the following values:

.. code-block:: python

    GoogleSafebrowsing {
		key="MySuperSecretApiKey"
    }

SafebrowsingAnalyzer
--------------------
.. automodule:: safebrowsing_analyzer
.. autoclass:: SafebrowsingAnalyzer
   :members:
   :private-members:

SafebrowsingClient
------------------
.. automodule:: safebrowsing
.. autoclass:: SafebrowsingClient
   :members:
   :private-members:

.. autoclass:: SearchTypeNotSupportedError
   :members:
   :private-members:

