"""
StarburstDomain
"""


class StarburstDomainInfo:
    """Represents a domain in Starburst."""

    MAX_NAME_LENGTH = 255
    MAX_SCHEMA_LOCATION_LENGTH = 255

    def __init__(self, name: str, description: str, schema_location: str, **options):
        """
        Initialize the StarburstDomain object.

        Parameters:
        - name (str): The name of the domain.
        - description (str): The description of the domain.
        - schema_location (str): The location of the schema.
        - id (str): Domain UUID
        - assigned_data_products (list[StarburstDataProductInfo]):
            List of the data products that are assigned to this domain.
        - created_by (str): Name of the user who created this domain.
        - created_at (str): Timestamp of when this domain was created.
        - updated_at (str): Timestamp of when this domain was last updated.
            This is initialized to createdAt.
        - updated_by (str): Name of the user who last updated this domain.
            This is initialized to createdBy
        """
        if len(name) > self.MAX_NAME_LENGTH:
            raise ValueError(
                "Length of 'name' exceeds maximum allowed length of"
                + f"{self.MAX_NAME_LENGTH} characters"
            )
        self.name = name
        self.description = description
        if len(schema_location) > self.MAX_SCHEMA_LOCATION_LENGTH:
            raise ValueError(
                "Length of 'schema_location' exceeds maximum allowed length of"
                + f"{self.MAX_SCHEMA_LOCATION_LENGTH} characters"
            )
        self.schema_location = schema_location
        self.assigned_data_products = options.get("assigned_data_products", None)
        self.created_by = options.get("created_by", None)
        self.created_at = options.get("created_at", None)
        self.updated_at = options.get("updated_at", None)
        self.updated_by = options.get("updated_by", None)
        self.id = options.get("id", None)

    def __repr__(self):
        return (
            f"StarburstDomain(name={self.name}, "
            f"description={self.description}, "
            f"schema_location={self.schema_location})"
        )

    def to_dict(self) -> dict:
        "Convert the instance to a dictionnary"
        return {
            "name": self.name,
            "description": self.description,
            "schemaLocation": self.schema_location,
        }
