`Back to index <index.html>`_

Virusshare.com
==============
This analyzer enables searching for md5 hashes in Virusshare.com hash list. It does not download samples for you nor
links directly to the sample - the author of virusshare prohibits the automatic download/site scraping and I respect
that. It provides a button to start the virusshare search, though, but you need an account for that. You can request an
invitation to the platform through contacting the admin via mail, directly.

Configuration
-------------
In order to check md5-hashes against the hash lists, a directory containing the lists must be provided in cortex config:

.. code-block:: none

   Virusshare {
      path="/path/to/download/directory"
   }

Download the newest hash lists
------------------------------
Usage
^^^^^
In order to download the newest available hash lists from virusshare.com, you can run the ``download_hashes.py`` script.

.. code-block:: none

   ./download_hashes.py /path/to/your/download/directory

It takes a lot of time to download. The files are names 000.md5 - xxx.md5 and already available files are skipped.

Documentation
^^^^^^^^^^^^^
.. automodule:: download_hashes
   :members:
   :private-members:

Virusshare Analyzer
-------------------
.. automodule:: virusshare
.. autoclass:: VirusshareAnalyzer
   :members:
   :private-members:
