`Back to index <index.html>`_

Example Analyzer
================
Writing a new Analyzer
----------------------
*This is not complete, right now.*

The MinimalPythonAnalyzer can be used as skeleton when writing a new one. In addition to the anlyzer itself, the configuration file, Example.json, needs some changes:

.. code-block:: python
	:linenos:

	{
	    "name": "Example",
	    "author": "Nils Kuhnert, CERT-Bund",
        "url": "https://github.com/BSI-CERT-Bund/cortex-analyzers",
	    "version": "0.1",
	    "baseConfig": "Example",
	    "config": {},
	    "description": "This is an example analyzer. It returns nothing.",
	    "dataTypeList": ["ip", "domain"],
	    "command": "Example/example_analyzer.py"
	}

If my new module is named Yara, and is callable over console using the file yara.py, the configuration would look like this:

.. code-block:: python
	:linenos:

	{
	    "name": "Yara",
	    "author": "Nils Kuhnert, CERT-Bund",
        "url": "https://github.com/BSI-CERT-Bund/cortex-analyzers",
	    "version": "0.1",
	    "baseConfig": "Yara",
	    "config": {},
	    "description": "This is my brand new yara analyzer.",
	    "dataTypeList": ["ip", "domain"],
	    "command": "Yara/yara.py"
	}


Example Analyzer
----------------
.. automodule:: example_analyzer
.. autoclass:: MinimalPythonAnalyzer
   :members:
   :private-members: