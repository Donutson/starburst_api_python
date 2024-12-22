"""
DataProduct class
"""


class DataProduct:
    """
    Represents a data product.

    Attributes:
        name (str): The name of the data product in lower_underscore_camel_case format.
        catalog_name (str): The name of the catalog.
        data_domain_id (str): The ID of the data domain.
        summary (str): Summary description for this data product.
        description (str): Description of the data product. (Optional)
        views (list of DatasetView): List of dataset views. (Optional)
        materialized_views (list of DatasetMaterializedView): List of materialized dataset views. (Optional)
        owners (list of Owner): List of owners of the data product. (Optional)
        relevant_links (list of RelevantLink): List of relevant links related to the data product. (Optional)
    """

    def __init__(
        self, name: str, catalog_name: str, data_domain_id: str, summary: str, **options
    ):
        """
        Initialize a DataProduct object.

        Args:
            name (str): The name of the data product in lower_underscore_camel_case format.
            catalog_name (str): The name of the catalog.
            data_domain_id (str): The ID of the data domain.
            summary (str): Summary description for this data product.
            **options: Additional options to specify id, description, views, materialized_views, owners,
            and relevant_links.
            
        Raises:
            ValueError: If any of the attributes violate the specified constraints.
        """
        # Check required attributes
        self._validate_string(name, "name", min_length=1, max_length=40)
        self._validate_string(
            catalog_name, "catalog_name", min_length=1, max_length=255
        )
        self._validate_uuid(data_domain_id, "data_domain_id")
        self._validate_string(summary, "summary", max_length=150)

        # Initialize attributes
        self.name = name
        self.catalog_name = catalog_name
        self.data_domain_id = data_domain_id
        self.summary = summary

        # Optional attributes
        self.id = options.get("id")
        self.description = options.get("description")
        self.views = options.get("views", [])
        self.materialized_views = options.get("materialized_views", [])
        self.owners = options.get("owners", [])
        self.relevant_links = options.get("relevant_links", [])

    def _validate_string(
        self,
        value: str,
        attribute_name: str,
        min_length: int = None,
        max_length: int = None,
    ):
        """Validate string attributes."""
        if value is not None:
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

    def _validate_uuid(self, value: str, attribute_name: str):
        """Validate UUID attributes."""
        if value is not None and not isinstance(value, str):
            raise ValueError(f"{attribute_name} must be a string (UUID).")
            # Add additional UUID validation logic if needed

    def to_dict(self) -> dict:
        "Convert the instance to a dictionnary"
        return {
            "name": self.name,
            "catalogName": self.catalog_name,
            "dataDomainId": self.data_domain_id,
            "summary": self.summary,
            "description": self.description,
            "views": [view.to_dict() for view in self.views],
            "materializedViews": [
                materializedView.to_dict()
                for materializedView in self.materialized_views
            ],
            "owners": [owner.to_dict() for owner in self.owners],
            "relevantLinks": [
                relevantLink.to_dict() for relevantLink in self.relevant_links
            ],
        }
