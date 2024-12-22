Owner
=========================

.. autoclass:: classes.class_owner.Owner

Usage Example
-------------

Here’s how you can create an `Owner` object and handle potential exceptions:

.. code-block:: python

    from starburst_api.classes import Owner

    try:
        # Create an Owner instance
        owner = Owner(
            name="Alice Johnson",
            email="alice.johnson@example.com"
        )

        # Access attributes
        print(owner.name)  # Output: "Alice Johnson"
        print(owner.email)  # Output: "alice.johnson@example.com"

    except ValueError as e:
        print(f"Error creating owner: {e}")