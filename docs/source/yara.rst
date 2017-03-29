`Back to index <index.html>`_

Yara
====
The yara analyzer checks pattern in file against yara rules.

Yara can be queried for:

- ``file``

Configuration
-------------
For configuring the Yara analyzer, the cortex configuration file should include the following values:

.. code-block:: python

    Yara {
        rules=["/path/to/rule/directory/a", "/path/to/directory/b", "/path/to/my/rule.yar"]
    }


**If the value is a directory, the analyzer checks for an index.yar or .yas (precompiled yara rule)**. You can create
an index file containing several ``include`` directives. An example for that can be found in the
popular `yara-rules Repository <https://github.com/Yara-Rules/rules>`_.

YaraAnalyzer
------------
.. automodule:: yara_analyzer
.. autoclass:: YaraAnalyzer
   :members:
   :private-members:

