`Back to index <index.html>`_

Cortexutils3
============
Cortexutils3 was created to cut python 2.7 dependencies. The provided ``cortexutils.analyzer`` package used
``ioc-parser`` that has ``pdfminer`` as a requirement - not available for python 3.
Ignoring that the artifacts-part of the results is missing, ``cortexutils3`` does the nearly same job as its python 2.7
counterpart. The only changes are:

- On error it returns the input, too, but removes attributes like ``password``, ``key``, ``api_key``
- By default, ``summary(self, raw: dict) -> dict`` just returns the raw dictionary
   - This should be overwritten by your analyzer anyway, it helps for quick analyzer tests
- **[NEW]** The Analyzer class imports the new `Extractor <#extractor>`_ class to detect ioc's in the report
   - Only strings that contain the **isolated** ioc are found - this is not a fulltext search right now

Analyzer
--------
.. automodule:: analyzer
.. autoclass:: Analyzer
   :members:
   :private-members:

Extractor
---------
.. automodule:: extractor
.. autoclass:: Extractor
   :members:
   :private-members:

