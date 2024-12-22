"""
StarburstConnectionInfo
"""


class StarburstConnectionInfo:
    """Contains information required to establish a connection with Starburst."""

    def __init__(self, host: str, user: str, password: str, **options):
        """
        Initialize the StarburstConnectionInfo object.

        Parameters:
            host (str): The hostname or IP address of the Starburst server.
            user (str): The username for authentication.
            password (str): The password for authentication.
            port (int): The port number for the connection. Default is 30443.
            catalog (str): The default catalog to use. Default is None.
            schema (str): The default schema to use. Default is None.
        """
        self.host = host
        self.user = user
        self.password = password
        self.port = options.get("port", "30443")
        self.catalog = options.get("catalog", None)
        self.schema = options.get("schema", None)

    def __repr__(self):
        return (
            f"StarburstConnectionInfo(host={self.host}, "
            f"user={self.user}, "
            f"port={self.port}, "
            f"catalog={self.catalog}, "
            f"schema={self.schema})"
        )
