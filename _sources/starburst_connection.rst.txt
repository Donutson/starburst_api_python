Starburst Connection Info
=========================

.. autoclass:: classes.class_starburst_connection_info.StarburstConnectionInfo

Usage Example
-------------

Here’s how you can create an instance of `StarburstConnectionInfo` :

.. code-block:: python

    from starburst_api.classes import StarburstConnectionInfo

    # Create an instance of StarburstConnectionInfo
    connection_info = StarburstConnectionInfo(
        host="starburst.example.com",
        user="my_user",
        password="my_password",
        port="8080",  # Custom port
        catalog="my_catalog",  # Custom catalog
        schema="my_schema"  # Custom schema
    )

    # Access connection information
    print(connection_info.host)  # "starburst.example.com"
    print(connection_info.user)  # "my_user"
    print(connection_info.port)  # "8080"
    print(connection_info.catalog)  # "my_catalog"
    print(connection_info.schema)  # "my_schema"