"""
RelevantLink class
"""


class RelevantLink:
    """
    Represents a relevant link.

    Attributes:
        label (str): The label of the relevant link.
        url (str): The URL of the relevant link.
    """

    MAX_LENGTH = 255

    def __init__(self, label: str, url: str):
        """
        Initialize a RelevantLink object.

        Args:
            label (str): The label of the relevant link.
            url (str): The URL of the relevant link.
        Raises:
            ValueError: If label or url exceeds the maximum length.
        """
        if len(label) > self.MAX_LENGTH:
            raise ValueError(
                f"Label must be at most {self.MAX_LENGTH} characters long."
            )
        if len(url) > self.MAX_LENGTH:
            raise ValueError(f"URL must be at most {self.MAX_LENGTH} characters long.")

        self.label = label
        self.url = url

    def to_dict(self) -> dict:
        "Convert the instance to a dictionnary"
        return {"label": self.label, "url": self.url}
