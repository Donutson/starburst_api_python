Client Starburst
=========================

.. autoclass:: classes.class_starburst.Starburst
    :members:

.. code-block:: python

    # Assuming StarburstConnectionInfo, StarburstDomainInfo, DataProduct, etc. are already defined

    # Step 1: Set up connection information
    connection_info = StarburstConnectionInfo(
        user="username", 
        password="password", 
        host="your-starburst-host", 
        port=8080, 
        catalog="your_catalog", 
        schema="your_schema"
    )

    # Initialize Starburst client
    starburst = Starburst(connection_info)

    # Step 2: Create a domain
    domain = StarburstDomainInfo(name="Sales", description="Sales data", schema_location="s3://sales-data")
    starburst.create_domain(domain)

    # Step 3: Create a data product
    data_product = DataProduct(id="123", name="Sales Data", description="Sales data product", domain="Sales")
    starburst.create_data_product(data_product)

    # Step 4: Create views from config
    views_config = [
        {"name": "customer_sales_view", "query": "SELECT customer_id, SUM(price) FROM sales GROUP BY customer_id"}
    ]
    starburst.create_view_from_config(config=views_config, views_dir="views_directory", strict=True)

    # Step 5: Update a domain
    domain_update = StarburstDomainInfo(id="123", name="Sales", description="Updated description", schema_location="s3://new-sales-data")
    starburst.update_domain(domain_update)

    # Step 6: Update a data product
    data_product_update = DataProduct(id="123", name="Updated Sales Data", description="Updated sales product", domain="Sales")
    starburst.update_data_product(data_product_update)

    # Step 7: Get a domain by ID
    domain_info = starburst.get_domain_by_id("12345", as_class=True)
    print(domain_info)

    # Step 8: Get a domain by name
    domain_by_name = starburst.get_domain_by_name("Sales", as_class=False)
    print(domain_by_name)

    # Step 9: Get a data product by domain and name
    data_product_info = starburst.get_data_product("Sales", "Sales Data", as_class=True)
    print(data_product_info)

    # Step 10: Get data product details
    data_product_details = starburst.get_data_product_details("Sales", "Sales Data")
    print(data_product_details)

    # Step 11: Get data product tags
    data_product_tags = starburst.get_data_product_tags("Sales", "Sales Data", as_class=True)
    print(data_product_tags)

    # Step 12: List all domains
    domains = starburst.list_domains()
    print(domains)

    # Step 13: Delete a domain by name
    starburst.delete_domain_by_name("Sales")

    # Step 14: Delete a data product
    starburst.delete_data_product("Sales", "Sales Data", delete_product_ressources="true")

    # Step 15: Publish a data product
    starburst.publish_data_product("Sales", "Sales Data", force="false")

    # Step 16: Execute an SQL query
    query = "SELECT * FROM sales.orders WHERE order_date >= CURRENT_DATE - INTERVAL '1' DAY"
    result = starburst.execute_query(query)
    print(result)

    # Step 17: Create a materialized view
    mv_query = "SELECT * FROM sales.orders WHERE order_date >= CURRENT_DATE - INTERVAL '1' DAY"
    starburst.create_mv_view(query=mv_query, view_name="daily_orders", cron="0 0 * * *", comment="Daily orders view")

    # Step 18: Create a regular view
    view_query = "SELECT customer_id, SUM(price) FROM sales.orders GROUP BY customer_id"
    starburst.create_view(query=view_query, view_name="customer_order_summary", comment="View summarizing customer orders")
