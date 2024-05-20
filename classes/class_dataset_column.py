"""
DatasetColumn class
"""


class DatasetColumn:
    """
    Represents a column in a dataset.

    Attributes:
        name (str): The name of the column.
        type (str): The type of data stored in the column.
        description (str): A description of the column.
    """

    def __init__(self, name: str, type: str, description: str):
        """
        Initialize a DatasetColumn object.

        Args:
            name (str): The name of the column.
                It must be a string with maximum length of 255 characters.
            type (str): The type of data stored in the column.
                It must be a string with maximum length of 255 characters.
            description (str): A description of the column.
                It must be a string with maximum length of 255 characters.
        Raises:
            ValueError: If any of the provided arguments violate the specified constraints.
        """
        if not isinstance(name, str) or len(name) > 255:
            raise ValueError(
                "Name must be a string with maximum length of 255 characters."
            )
        if not isinstance(type, str) or len(type) > 255:
            raise ValueError(
                "Type must be a string with maximum length of 255 characters."
            )
        if not isinstance(description, str) or len(description) > 255:
            raise ValueError(
                "Description must be a string with maximum length of 255 characters."
            )

        self.name = name
        self.type = type
        self.description = description

    def to_dict(self):
        "Convert the instance to a dictionnary"
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
        }
