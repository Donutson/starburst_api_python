Starburst Domain Info
=========================

.. autoclass:: classes.class_starburst_domain_info.StarburstDomainInfo

Usage Example
-------------

Here’s how you can create an instance of `StarburstConnectionInfo` and use it to establish a connection:

Usage Example
-------------

Here’s an example of how to use the `StarburstDomainInfo` class:

.. code-block:: python
    
    from my_module import StarburstDomainInfo

    # Create an instance of StarburstDomainInfo
    domain_info = StarburstDomainInfo(
        name="CustomerData",
        description="Domain for customer-related data.",
        schema_location="s3://starburst/schemas/customer_data",
        owner="data_engineering",  # Custom metadata passed via options
        tags=["production", "analytics"]  # Additional metadata
    )

    # Access domain information
    print(domain_info.name)  # Output: "CustomerData"
    print(domain_info.description)  # Output: "Domain for customer-related data."
    print(domain_info.schema_location)  # Output: "s3://starburst/schemas/customer_data"

    # Access optional metadata
    print(domain_info.owner)  # Output: "data_engineering"
    print(domain_info.tags)  # Output: ["production", "analytics"]