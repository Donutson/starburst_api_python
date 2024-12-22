Relevant Tag
=========================

.. autoclass:: classes.class_tag.Tag

Usage Example
-------------

Here’s an example of how to create and use a `Tag` object:

.. code-block:: python

    from my_module import Tag

    try:
        # Create a Tag instance
        tag = Tag(
            id="123e4567-e89b-12d3-a456-426614174000",
            value="Important"
        )

        # Access attributes
        print(tag.id)  # Output: "123e4567-e89b-12d3-a456-426614174000"
        print(tag.value)  # Output: "Important"

    except ValueError as e:
        print(f"Error creating tag: {e}")