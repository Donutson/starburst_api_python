Relevant Link
=========================

.. autoclass:: classes.class_starburst_relevant_link.RelevantLink

Usage Example
-------------

Here’s how to create and use a `RelevantLink` object:

.. code-block:: python
    
    from starburst_api.classes import RelevantLink

    try:
        # Create a RelevantLink instance
        link = RelevantLink(
            label="Starburst Documentation",
            url="https://docs.starburst.io/latest/"
        )

        # Access attributes
        print(link.label)  # Output: "Starburst Documentation"
        print(link.url)  # Output: "https://docs.starburst.io/latest/"

    except ValueError as e:
        print(f"Error creating relevant link: {e}")
