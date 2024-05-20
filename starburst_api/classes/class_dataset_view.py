"""
DatasetView class
"""
import re

from starburst_api.classes.class_dataset_column import DatasetColumn


class DatasetView:
    """
    Represents a view of a dataset.

    Attributes:
        name (str): The name of the dataset view.
            It must be a valid SQL name with lowercase letters.
        description (str): A description of the dataset view. (Optional)
        definition_query (str): The SQL query defining the dataset view. (Optional)
        columns (list of DatasetColumn): List of columns in the dataset view. (Optional)
        marked_for_deletion (bool): Indicates whether the dataset view is marked for deletion. (Optional)
    """

    def __init__(self, name: str, **options):
        """
        Initialize a DatasetView object.

        Args:
            name (str): The name of the dataset view. It must be a valid SQL name with lowercase letters.
            **options: Additional options to specify description, definition_query, columns, and marked_for_deletion.
        Raises:
            ValueError: If the provided name violates the specified constraint
                        or if columns is not a list of DatasetColumn objects.
        """
        # Check if name is a valid SQL name with lowercase letters
        if not re.match(r"^[a-z][a-z0-9_]*$", name):
            raise ValueError("Name must be a valid SQL name with lowercase letters.")

        self.name = name
        self.description = options.get("description")
        self.definition_query = options.get("definition_query")
        self.marked_for_deletion = options.get("marked_for_deletion", "false")

        columns = options.get("columns", [])
        if not all(isinstance(column, DatasetColumn) for column in columns):
            raise ValueError("Columns must be a list of DatasetColumn objects.")
        self.columns = columns

    def to_dict(self):
        "Convert the instance to a dictionnary"
        return {
            "name": self.name,
            "description": self.description,
            "definitionQuery": self.definition_query,
            "markedForDeletion": self.marked_for_deletion,
            "columns": [column.to_dict() for column in self.columns],
        }
