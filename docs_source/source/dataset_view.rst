Dataset View
=========================

.. autoclass:: classes.class_dataset_view.DatasetView

Usage Example
-------------

Here’s an example of how to create and use a `DatasetView` object:

.. code-block:: python
    
        from starburst_api.classes import DatasetView, DatasetColumn
    
        try:
            # Define some columns for the dataset view
            columns = [
                DatasetColumn(name="id", type="integer", description="Unique identifier."),
                DatasetColumn(name="name", type="string", description="Name of the item."),
                DatasetColumn(name="created_at", type="timestamp", description="Creation timestamp."),
            ]
    
            # Create a DatasetView instance
            view = DatasetView(
                name="customer_view",
                description="A view of customer data.",
                definition_query="SELECT id, name, created_at FROM customers",
                columns=columns,
                marked_for_deletion=False,
            )
    
            # Access attributes
            print(view.name)         # Output: "customer_view"
            print(view.description)  # Output: "A view of customer data."
            print(view.columns[0].name)  # Output: "id"
    
        except ValueError as e:
            print(f"Error creating DatasetView: {e}")
    
        # Example with invalid input
        try:
            invalid_view = DatasetView(
                name="CustomerView",  # Invalid: contains uppercase letters
                columns=["invalid_column"]  # Invalid: not a list of DatasetColumn objects
            )
        except ValueError as e:
            print(f"Error: {e}")  # Output: Error message about invalid input
