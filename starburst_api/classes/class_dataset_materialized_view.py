"""
DatasetView class
"""
from starburst_api.classes.class_dataset_view import DatasetView
from starburst_api.classes.class_definition_properties import DefinitionProperties


class DatasetMaterializedView(DatasetView):
    """
    Represents a materialized view of a dataset.

    Attributes:
        definition_properties (DefinitionProperties): The definition properties for the materialized view.
    """

    def __init__(self, name: str, **options):
        """
        Initialize a DatasetMaterializedView object.

        Args:
            name (str): The name of the dataset materialized view.
            **options: Additional options to specify description, definition_query, columns,
                       marked_for_deletion, and definition_properties.
        Raises:
            ValueError: If the provided name violates the specified constraint
                        or if columns is not a list of DatasetColumn objects
                        or if the definition_properties are not valid.
        """
        super().__init__(name, **options)

        definition_properties = options.get("definition_properties")
        if definition_properties:
            if not isinstance(definition_properties, DefinitionProperties):
                raise ValueError(
                    "Definition properties must be an instance of DefinitionProperties."
                )

            if self.columns and definition_properties.incremental_column:
                # Vérifie si incremental_column est égal à l'un des noms des colonnes
                column_names = [column.name for column in self.columns]
                if definition_properties.incremental_column not in column_names:
                    raise ValueError(
                        "incremental_column must be equal to the name of one of the DatasetColumn objects."
                    )

        self.definition_properties = definition_properties

    def to_dict(self) -> dict:
        "Convert the instance to a dictionnary"
        return {
            "name": self.name,
            "description": self.description,
            "definitionQuery": self.definition_query,
            "markedForDeletion": self.marked_for_deletion,
            "columns": [column.to_dict() for column in self.columns],
            "definitionProperties": self.definition_properties.to_dict(),
        }
