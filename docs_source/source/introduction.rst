Starburst API Python
====================

The goal of this package is to create data products on Starburst using Python. This package leverages the `Starburst REST API <https://docs.starburst.io/latest/api/index.html>`_ to interact with your Starburst Enterprise instance.
You can find the package source code on `GitHub <https://github.com/Donutson/starburst_api_python>`_.

Prerequisites
-------------

To use this package, you need the following:

1. A Starburst Enterprise instance.
2. Python >= 3.7.*
3. Required Python libraries:

   - `trino`
   - `pandas`
   - `sqlalchemy`
   - `sqlalchemy-trino`

Installation
------------

Install the package using the following command:

.. code-block:: shell

    pip install git+https://github.com/Donutson/starburst_api_python.git

Package Overview
----------------

Classes
~~~~~~~

**StarburstConnectionInfo**

Defines a connection to a Starburst instance.

.. code-block:: python

    connection_info = StarburstConnectionInfo(
        host="127.0.0.1",
        user="starburst",
        password="starburst_pass",
        port="30443",
    )

**StarburstDomainInfo**

Defines a domain in Starburst.

.. code-block:: python

    domain = StarburstDomainInfo(
        name="test_api_python",
        description="Creating a domain via Python",
        schema
    )