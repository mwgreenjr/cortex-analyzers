`Back to index <index.html>`_

FireHOL Blocklists
==================
This analyzer compares an ip-address with the fireHOL blocklists that can be found on
`iplists.firehol.org <https://iplists.firehol.org/>`_ also. It returns all matched lists. The lists have to be
downloaded and extracted to a directory in advance to use this analyzer.

Accepted inputs are:

- ``ip``

Configuration
-------------
For configuring the FireHOL IP Blocklists analyzer, the cortex configuration file should include the following values:

.. code-block:: python

    FireholBlocklists {
        blocklistspath="/tmp/fireholblocklists" # Path to blocklists cloned from github
        ignoredays="365" # Ignore lists older than x days - NOT IMPEMENTED YET
    }

FireholBlocklistsAnalyzer
-------------------------
.. automodule:: firehol_blocklists
.. autoclass:: FireholBlocklistsAnalyzer
   :members:
   :private-members:
