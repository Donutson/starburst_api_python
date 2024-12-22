Data Product
=========================

.. autoclass:: classes.class_data_product.DataProduct

Usage Example
-------------

Here’s an example of how to create and use a `DataProduct` object:

.. code-block:: python

    from starburst_api.classes import DataProduct, DatasetView, DatasetMaterializedView, Owner, RelevantLink

    # Create dataset views
    views = [
        DatasetView(name="customer_view", description="Customer data view"),
        DatasetView(name="orders_view", description="Orders data view")
    ]

    # Create materialized dataset views
    materialized_views = [
        DatasetMaterializedView(name="customer_materialized_view"),
        DatasetMaterializedView(name="orders_materialized_view")
    ]

    # Define owners
    owners = [
        Owner(name="John Doe", email="john.doe@example.com"),
        Owner(name="Jane Smith", email="jane.smith@example.com")
    ]

    # Define relevant links
    links = [
        RelevantLink(label="Dashboard", url="http://dashboard.example.com"),
        RelevantLink(label="Documentation", url="http://docs.example.com")
    ]

    # Create a DataProduct instance
    data_product = DataProduct(
        name="customer_data_product",
        catalog_name="customer_catalog",
        data_domain_id="123e4567-e89b-12d3-a456-426614174000",
        summary="This data product contains customer-related datasets.",
        description="Detailed description of the customer data product.",
        views=views,
        materialized_views=materialized_views,
        owners=owners,
        relevant_links=links
    )

    # Access attributes
    print(data_product.name)  # Output: "customer_data_product"
    print(data_product.owners[0].name)  # Output: "John Doe"
    print(data_product.relevant_links[1].url)  # Output: "http://docs.example.com"