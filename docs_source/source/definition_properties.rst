Definition Properties
=========================

.. autoclass:: classes.class_definition_properties.DefinitionProperties

Usage Example
-------------

Here’s how to create and use a `DefinitionProperties` object:

.. code-block:: python
    
    from starburst_api.classes import DefinitionProperties

    try:
        # Create a DefinitionProperties instance
        props = DefinitionProperties(
            refresh_interval="4h",
            incremental_column="updated_at"
        )

        # Access attributes
        print(props.refresh_interval)  # Output: "4h"
        print(props.incremental_column)  # Output: "updated_at"

    except ValueError as e:
        print(f"Error creating DefinitionProperties: {e}")

    # Example with invalid input
    try:
        invalid_props = DefinitionProperties(
            refresh_interval="30m"  # Invalid: less than 60m
        )
    except ValueError as e:
        print(f"Error: {e}")  # Output: "refresh_interval must be at least '60m'"