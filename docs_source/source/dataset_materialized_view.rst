Dataset Materialized View
=========================

.. autoclass:: classes.class_dataset_materialized_view.DatasetMaterializedView

Usage Example
-------------

Here’s an example of how to create and use a `DatasetMaterializedView` object:

.. code-block:: python
    
    from starburst_api.classes import DatasetMaterializedView, DatasetColumn, DefinitionProperties

    try:
        # Define some columns for the materialized view
        columns = [
            DatasetColumn(name="id", type="integer", description="Unique identifier."),
            DatasetColumn(name="name", type="string", description="Name of the item."),
            DatasetColumn(name="created_at", type="timestamp", description="Creation timestamp."),
        ]

        # Define definition properties
        definition_properties = DefinitionProperties(
            refresh_interval="2h", incremental_column="id"
        )

        # Create a DatasetMaterializedView instance
        materialized_view = DatasetMaterializedView(
            name="customer_materialized_view",
            description="A materialized view of customer data.",
            definition_query="SELECT id, name, created_at FROM customers",
            columns=columns,
            definition_properties=definition_properties,
            marked_for_deletion=False,
        )

        # Access attributes
        print(materialized_view.name)  # Output: "customer_materialized_view"
        print(materialized_view.definition_properties.refresh_interval)  # Output: "2h"

    except ValueError as e:
        print(f"Error creating DatasetMaterializedView: {e}")

    # Example with invalid input
    try:
        invalid_view = DatasetMaterializedView(
            name="CustomerMaterializedView",  # Invalid: contains uppercase letters
            definition_properties=DefinitionProperties(refresh_interval="10m")
        )
    except ValueError as e:
        print(f"Error: {e}")  # Output: Error message about invalid input