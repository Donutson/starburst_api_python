"""
Owner class
"""


class Owner:
    """
    Represents an owner.

    Attributes:
        name (str): The name of the owner.
        email (str): The email of the owner.
    """

    def __init__(self, name: str, email: str):
        """
        Initialize an Owner object.

        Args:
            name (str): The name of the owner.
            email (str): The email of the owner.
        Raises:
            ValueError: If any of the attributes violate the specified constraints.
        """
        self._validate_string(name, "name", min_length=1, max_length=40)
        self._validate_string(email, "email", min_length=1, max_length=255)

        self.name = name
        self.email = email

    def __str__(self) -> str:
        return f"({self.name}: {self.email})"

    def _validate_string(
        self, value: str, attribute_name: str, min_length=None, max_length=None
    ):
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
        return {"name": self.name, "email": self.email}
