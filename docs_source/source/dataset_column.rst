Dataset Column
=========================

.. autoclass:: classes.class_dataset_column.DatasetColumn

Usage Example
-------------

Here’s an example of how to create and use a `DatasetColumn` object:

.. code-block:: python

    from starburst_api.classes import DatasetColumn

    try:
        # Create a DatasetColumn instance
        column = DatasetColumn(
            name="CustomerID",
            type="string",
            description="The unique identifier for a customer."
        )

        # Access attributes
        print(column.name)         # Output: "CustomerID"
        print(column.type)         # Output: "string"
        print(column.description)  # Output: "The unique identifier for a customer."

    except ValueError as e:
        print(f"Error creating DatasetColumn: {e}")

    # Example with invalid input
    try:
        invalid_column = DatasetColumn(
            name="A" * 300,  # Invalid: exceeds 255 characters
            type="integer",
            description="This will fail."
        )
    except ValueError as e:
        print(f"Error: {e}")  # Output: "Name must be a string with maximum length of 255 characters."