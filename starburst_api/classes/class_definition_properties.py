"""
DefinitionProperties class
"""
import re


class DefinitionProperties:
    """
    Represents the definition properties for a materialized view.

    Attributes:
        refresh_interval (str): The refresh interval for the materialized view.
        incremental_column (str): The incremental column for the materialized view.
    """

    VALID_INTERVAL_FORMAT = re.compile(r"^[1-9]\d*[mhdw]$")

    def __init__(self, refresh_interval: str, incremental_column: str = None):
        """
        Initialize a DefinitionProperties object.

        Args:
            refresh_interval (str, optional): The refresh interval for the materialized view.
            incremental_column (str, optional): The incremental column for the materialized view.
        Raises:
            ValueError: If both refresh_interval and incremental_column are None,
                        or if refresh_interval is not in the specified format
                        or if refresh_interval is less than "60m".
        """
        if not self.VALID_INTERVAL_FORMAT.match(refresh_interval):
            raise ValueError(
                "Invalid format for refresh_interval. Valid formats: '60m', '4h', '2d', '1w'"
            )
        if (refresh_interval[-1] == "m") and (int(refresh_interval[:-1]) < 60):
            raise ValueError("refresh_interval must be at least '60m'")

        self.refresh_interval = refresh_interval
        self.incremental_column = incremental_column

    def to_dict(self) -> dict:
        "Convert the instance to a dictionnary"
        return {
            "refresh_interval": self.refresh_interval,
            "incremental_column": self.incremental_column,
        }
