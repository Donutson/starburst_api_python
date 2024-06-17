"""
Tag class
"""


class Tag:
    """
    Represents an owner.

    Attributes:
        id (str): The uuid of the tag.
        value (str): The value of the tag.
    """

    def __init__(self, id: str, value: str):
        """
        Initialize a Tag object.

        Args:
            id (str): The uuid of the tag.
            value (str): The value of the tag.
        Raises:
            ValueError: If any of the attributes violate the specified constraints.
        """
        self._validate_uuid(id, "id")
        self._validate_string(value, "value", max_length=255)

        self.id = id
        self.value = value

    def __str__(self) -> str:
        return self.value

    def _validate_uuid(self, value: str, attribute_name: str):
        """Validate UUID attributes."""
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(f"{attribute_name} must be a string (UUID).")
            # Add additional UUID validation logic if needed

    def _validate_string(self, value: str, attribute_name: str, min_length=None, max_length=None):
        """Validate string attributes."""
        if not isinstance(value, str):
            raise ValueError(f"{attribute_name} must be a string.")
        if min_length is not None and len(value) < min_length:
            raise ValueError(
                f"{attribute_name} must be at least {min_length} characters long."
            )
        if max_length is not None and len(value) > max_length:
            raise ValueError(
                f"{attribute_name} must be at most {max_length} characters long."
            )

    def to_dict(self) -> dict:
        "Convert the instance to a dictionnary"
        return {"id": self.id, "value": self.value}
