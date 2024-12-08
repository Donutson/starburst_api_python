"""
UTILITIES FUNCTIONS
"""
import os
import json
import pandas as pd
import requests
from sqlalchemy import create_engine
from urllib.parse import quote

from starburst_api.classes.class_dataset_column import DatasetColumn
from starburst_api.classes.class_starburst_connection_info import (
    StarburstConnectionInfo,
)
from starburst_api.classes.class_data_product import DataProduct
from starburst_api.classes.class_dataset_view import DatasetView
from starburst_api.classes.class_dataset_materialized_view import (
    DatasetMaterializedView,
)
from starburst_api.classes.class_dataset_column import DatasetColumn
from starburst_api.classes.class_owner import Owner
from starburst_api.classes.class_relevant_link import RelevantLink
from starburst_api.classes.class_definition_properties import DefinitionProperties
from starburst_api.classes.class_tag import Tag
from starburst_api.helpers.variables import (
    APPLICATION_JSON_TEXT,
    STARBURST_SSL_VERIFICATION,
)


def read_excel_to_dataset_colums(
    file_path: str, sheet_name: str = "schema"
) -> DatasetColumn:
    """
    Read an Excel file with 'name', 'type', and 'description' fields
    and create a list of dataset columns.

    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str): The name of the sheet in the Excel file.

    Returns:
        List of DatasetColumn: A list of DatasetColumn objects.
    """
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Create an empty list to store DatasetColumn objects
    columns = []

    # Iterate over rows in the DataFrame
    for _, row in df.iterrows():
        # Extract values for name, type, and description from the DataFrame
        name = row.get("name")
        type_col = row.get("type")
        description = row.get("description")

        # Create a DatasetColumn object and add it to the columns list
        column = DatasetColumn(name=name, type=type_col, description=description)
        columns.append(column)

    return columns


def create_excel_schema_from_starburst_table(
    connection_info: StarburstConnectionInfo, table_name: str, output_file: str
):
    """
    Connects to a Starburst (Trino) database, retrieves the schema of a specified table using the DESCRIBE command,
    and writes it to an Excel file.

    Args:
        connection_info (StarburstConnectionInfo): A StarburstConnectionInfo to create the connection url
        table_name (str): The name of the table for which the schema is to be retrieved.
        output_file (str): The path where the Excel file will be saved.

    """
    # Create a database engine
    engine = create_engine(
        f"trino://{connection_info.user}:{quote(connection_info.password)}"
        + f"@{connection_info.host}:{connection_info.port}?sslVerification=None",
        connect_args={"http_scheme": "https", "verify": STARBURST_SSL_VERIFICATION},
    )

    if len(table_name.split(".")) != 3:
        raise ValueError("Le nom de la table doit être absolu: catalog.schema.table")

    # SQL command to describe the table structure
    query = f"DESCRIBE {table_name}"

    # Execute the query and store results in a DataFrame
    df = pd.read_sql(query, engine)

    # Rename columns and add empty description column
    df.rename(
        columns={"Column": "name", "Type": "type", "Comment": "description"},
        inplace=True,
    )
    df = df[["name", "type", "description"]]

    # Create a Pandas Excel writer using openpyxl as the engine
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        # Write DataFrame to an Excel file on the sheet 'schema'
        df.to_excel(writer, sheet_name="schema", index=False)

    print(f"Schema for table '{table_name}' has been written to '{output_file}'.")


def data_product_json_to_class(data_product: dict) -> DataProduct:
    """
    Convert a dictionary representation of a data product to a DataProduct object.

    Args:
        data_product (dict): A dictionary containing details about the data product.
                             The dictionary must have the following keys:
                             - "name" (str): The name of the data product.
                             - "catalogName" (str): The catalog name of the data product.
                             - "dataDomainId" (str): The data domain ID of the data product.
                             - "description" (str): A description of the data product.
                             - "summary" (str): A summary of the data product.
                             - "owners" (list): A list of dictionaries, each representing an owner.
                             - "views" (list): A list of dictionaries, each representing a dataset view.
                             - "materializedViews" (list): A list of dictionaries, each representing a dataset materialized view.
                             - "relevantLinks" (list): A list of dictionaries, each representing a relevant link.

    Returns:
        DataProduct: An instance of DataProduct initialized with the values from the input dictionary.

    Raises:
        KeyError: If any of the required keys are missing from the input dictionary.
        TypeError: If the input is not a dictionary or if any of the lists are not properly formatted.
    """
    return DataProduct(
        id=data_product.get("id"),
        name=data_product.get("name"),
        catalog_name=data_product.get("catalogName"),
        data_domain_id=data_product.get("dataDomainId"),
        description=data_product.get("description"),
        summary=data_product.get("summary"),
        owners=[
            data_product_owner_json_to_class(owner)
            for owner in data_product.get("owners")
        ],
        views=[dataset_view_json_to_class(view) for view in data_product.get("views")],
        materialized_views=[
            dataset_materialized_view_json_to_class(view)
            for view in data_product.get("materializedViews")
        ],
        relevant_links=[
            data_product_relevant_link_json_to_class(link)
            for link in data_product.get("relevantLinks")
        ],
    )


def data_product_owner_json_to_class(owner: dict) -> Owner:
    """
    Convert a dictionary representation of a data product owner to an Owner object.

    Args:
        owner (dict): A dictionary containing details about the data product owner.
                      The dictionary must have the following keys:
                      - "name" (str): The name of the owner.
                      - "email" (str): The email address of the owner.

    Returns:
        Owner: An instance of Owner initialized with the values from the input dictionary.

    Raises:
        KeyError: If any of the required keys are missing from the input dictionary.
        TypeError: If the input is not a dictionary.
    """
    return Owner(name=owner.get("name"), email=owner.get("email"))


def data_product_relevant_link_json_to_class(link: dict) -> RelevantLink:
    """
    Convert a dictionary representation of a relevant link to a RelevantLink object.

    Args:
        link (dict): A dictionary containing details about the relevant link.
                     The dictionary must have the following keys:
                     - "label" (str): The label of the link.
                     - "url" (str): The URL of the link.

    Returns:
        RelevantLink: An instance of RelevantLink initialized with the values from the input dictionary.

    Raises:
        KeyError: If any of the required keys are missing from the input dictionary.
        TypeError: If the input is not a dictionary.
    """
    return RelevantLink(label=link.get("label"), url=link.get("url"))


def dataset_view_json_to_class(view: dict) -> DatasetView:
    """
    Convert a dictionary representation of a dataset view to a DatasetView object.

    Args:
        view (dict): A dictionary containing details about the dataset view.
                     The dictionary must have the following keys:
                     - "name" (str): The name of the dataset view.
                     - "description" (str): A description of the dataset view.
                     - "definitionQuery" (str): The SQL query defining the view.
                     - "columns" (list): A list of dictionaries, each representing a column.

    Returns:
        DatasetView: An instance of DatasetView initialized with the values from the input dictionary.

    Raises:
        KeyError: If any of the required keys are missing from the input dictionary.
        TypeError: If the input is not a dictionary or if columns is not a list.
    """
    return DatasetView(
        name=view.get("name"),
        description=view.get("description"),
        definition_query=view.get("definitionQuery"),
        columns=[dataset_column_json_to_class(column) for column in view["columns"]],
    )


def dataset_materialized_view_json_to_class(view: dict) -> DatasetMaterializedView:
    """
    Convert a dictionary representation of a dataset materialized view to a DatasetMaterializedView object.

    Args:
        view (dict): A dictionary containing details about the dataset materialized view.
                     The dictionary must have the following keys:
                     - "name" (str): The name of the dataset materialized view.
                     - "description" (str): A description of the dataset materialized view.
                     - "definitionQuery" (str): The SQL query defining the materialized view.
                     - "columns" (list): A list of dictionaries, each representing a column.
                     - "definitionProperties" (dict): A dictionary containing additional properties of the view.
                        It should contain:
                        - "refresh_interval" (int): The interval at which the view is refreshed.
                        - "incremental_column" (optional, str): The column used for incremental updates.

    Returns:
        DatasetMaterializedView: An instance of DatasetMaterializedView initialized with the values from the input dictionary.

    Raises:
        KeyError: If any of the required keys are missing from the input dictionary.
        TypeError: If the input is not a dictionary or if columns is not a list.
    """
    if view.get("definitionProperties").get("incremental_column"):
        definition_property = DefinitionProperties(
            refresh_interval=view.get("definitionProperties").get("refresh_interval"),
            incremental_column=view.get("definitionProperties").get(
                "incremental_column"
            ),
        )
    else:
        definition_property = DefinitionProperties(
            refresh_interval=view.get("definitionProperties").get("refresh_interval"),
        )

    return DatasetMaterializedView(
        name=view.get("name"),
        description=view.get("description"),
        definition_query=view.get("definitionQuery"),
        definition_properties=definition_property,
        columns=[dataset_column_json_to_class(column) for column in view["columns"]],
    )


def dataset_column_json_to_class(column: dict) -> DatasetColumn:
    """
    Convert a dictionary representation of a dataset column to a DatasetColumn object.

    Args:
        column (dict): A dictionary containing details about the dataset column.
                       The dictionary must have the following keys:
                       - "name" (str): The name of the dataset column.
                       - "description" (str): A description of the dataset column.
                       - "type" (str): The data type of the dataset column.

    Returns:
        DatasetColumn: An instance of DatasetColumn initialized with the values from the input dictionary.

    Raises:
        KeyError: If any of the required keys ("name", "description", "type") are missing from the input dictionary.
        TypeError: If the input is not a dictionary.
    """
    return DatasetColumn(
        name=column.get("name"),
        description=column.get("description"),
        type=column.get("type"),
    )


def load_starburst_view_file_content(file):
    """
    Load the content of the file.

    This function attempts to load the file content as JSON. If the content is not valid JSON,
    it reads the file line by line and constructs a dictionary from the text format.

    Args:
        file (file object): The file object to be read.

    Returns:
        dict: The content of the file as a dictionary.
    """

    try:
        return json.load(file)
    except json.JSONDecodeError:
        file.seek(0)
        return dict(line.strip().split(":", 1) for line in file.readlines())


def validate_starburst_view_file_fields(data, required_fields, valid_fields):
    """
    Validate the presence of required and valid fields.

    This function checks whether all required fields are present in the data and ensures no
    invalid fields are present.

    Args:
        data (dict): The data dictionary to be validated.

    Returns:
        tuple: A tuple containing a boolean indicating validity and a message.
    """
    if not required_fields.issubset(data):
        return False, "Missing required fields"
    if not all(field in valid_fields for field in data):
        return False, "Invalid fields present"
    return True, ""


def validate_starburst_view_file_types(data):
    """
    Validate the types and values of specific fields.

    This function ensures that the "executionOrder" field is an integer, the "type" field has a valid value,
    the "cron" field is present if the type is "materialized_view", and the "partitionedBy" field is a string if present.

    Args:
        data (dict): The data dictionary to be validated.

    Returns:
        tuple: A tuple containing a boolean indicating validity and a message.
    """
    if not isinstance(data["executionOrder"], int):
        return False, "executionOrder must be an integer"
    if data["type"] not in {"view", "materialized_view"}:
        return False, "Invalid type, must be view or materialized_view"
    if data["type"] == "materialized_view" and "cron" not in data:
        return False, "cron is required for materialized_view"
    if "partitionedBy" in data and not isinstance(data["partitionedBy"], str):
        return False, "partitionedBy must be a string"
    return True, ""


def is_valid_starburst_view_file(file) -> bool:
    """
    Checks if the file content is valid.

    The function verifies if the content of a given file (in JSON or text format) adheres to specific schema requirements.

    Args:
        file (file object): The file object to be validated.

    Returns:
        bool: True if the file content is valid, False otherwise.

    The required fields are:
    - name
    - type
    - queryPath
    - executionOrder

    Additionally, the following optional fields are allowed:
    - comment
    - cron
    - gracePeriod
    - incrementalColumn
    - partitionedBy
    - maxImportDuration

    Validation checks include:
    - Presence of all required fields.
    - Correct type for the "executionOrder" field (integer).
    - Valid value for the "type" field (either "view" or "materialized_view").
    - Presence of the "cron" field if the type is "materialized_view".
    - Correct type for the "partitionedBy" field (string, if present).
    - No extra fields outside the allowed ones.
    """

    required_fields = {"name", "type", "queryPath", "executionOrder"}
    optional_fields = {
        "comment",
        "cron",
        "gracePeriod",
        "incrementalColumn",
        "partitionedBy",
        "maxImportDuration",
    }
    valid_fields = required_fields | optional_fields

    data = load_starburst_view_file_content(file)
    is_valid, message = validate_starburst_view_file_fields(
        data=data, required_fields=required_fields, valid_fields=valid_fields
    )
    if not is_valid:
        print(message)
        return False

    is_valid, message = validate_starburst_view_file_types(data=data)
    if not is_valid:
        print(message)
        return False

    return True


def read_starburst_view_files(directory: str) -> list:
    """
    Reads all .view files in a directory and returns a list of valid dictionaries.

    The function iterates through all files with the .view extension in the specified directory,
    validates each file using the is_valid function, and returns a list of valid file contents as dictionaries.

    Args:
        directory (str): The directory path to read .view files from.

    Returns:
        list: A list of valid file content dictionaries, sorted by the executionOrder field.

    Each valid file is expected to contain:
    - name (str)
    - type (str): Either "view" or "materialized_view"
    - queryPath (str): Path to the SQL query file
    - executionOrder (int)

    Additionally, the following optional fields are allowed:
    - comment (str)
    - cron (str)
    - gracePeriod (str)
    - incrementalColumn (str)
    - partitionedBy (str)
    - maxImportDuration (str)
    """

    def load_and_validate_starburst_view_file(file_path):
        with open(file_path, "r") as file:
            if is_valid_starburst_view_file(file):
                file.seek(0)  # Reset file pointer for loading data
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    file.seek(0)
                    return dict(line.strip().split(":", 1) for line in file.readlines())
        return None

    valid_files = [
        load_and_validate_starburst_view_file(os.path.join(directory, filename))
        for filename in os.listdir(directory)
        if filename.endswith(".view")
    ]

    # Filter out any invalid files (None entries)
    valid_files = [file for file in valid_files if file is not None]

    # Convert executionOrder to int if it's in string format
    for file in valid_files:
        if isinstance(file["executionOrder"], str):
            file["executionOrder"] = int(file["executionOrder"])

    # Sort the list by executionOrder
    valid_files.sort(key=lambda file: file["executionOrder"])

    return valid_files


def validate_query_path(view_conf, strict):
    """
    Validate if the query path exists.

    Args:
        view_conf (dict): View configuration dictionary.
        strict (bool): If True, stops execution on the first error.

    Returns:
        bool: True if the query path exists, False otherwise.
    """
    if not os.path.exists(view_conf.get("queryPath")):
        print(f"{view_conf.get('queryPath')} not found")
        if strict:
            return False
    return True


def map_view_config_fields(view_conf, mapped_fields):
    """
    Map view configuration fields to the required arguments.

    Args:
        view_conf (dict): View configuration dictionary.
        mapped_fields (dict): Dictionary mapping view configuration fields to required argument names.

    Returns:
        dict: Mapped arguments dictionary.
    """
    return {mapped_fields.get(key, key): value for key, value in view_conf.items()}


def read_query_file(query_path):
    """
    Read the SQL query file content.

    Args:
        query_path (str): Path to the SQL query file.

    Returns:
        str: Content of the SQL query file.
    """
    with open(query_path, "r") as file:
        return file.read()


def find_data_product(domain, data_product_name):
    """
    Find the data product by name within the domain.

    Args:
        domain (dict): The domain dictionary containing data products.
        data_product_name (str): The name of the data product to find.

    Returns:
        dict or None: The data product dictionary if found, otherwise None.
    """
    for product in domain.get("assignedDataProducts", []):
        if product["name"] == data_product_name:
            return product
    return None


def fetch_data_product(connection_info, data_product_id):
    """
    Fetch the data product details using a GET request.

    Args:
        connection_info (ConnectionInfo): The connection information for authentication.
        data_product_id (str): The ID of the data product to fetch.

    Returns:
        Response: The HTTP response object.
    """
    url = (
        f"https://{connection_info.host}:{connection_info.port}"
        + f"/api/v1/dataProduct/products/{data_product_id}"
    )
    headers = {
        "Accept": APPLICATION_JSON_TEXT,
        "Content-Type": APPLICATION_JSON_TEXT,
    }
    auth = (connection_info.user, connection_info.password)

    return requests.get(
        url, headers=headers, auth=auth, verify=STARBURST_SSL_VERIFICATION
    )


def handle_fetch_data_product_response(response, as_class):
    """
    Handle the HTTP response for the data product retrieval.

    Args:
        response (Response): The HTTP response object.
        as_class (bool): If True, convert the JSON response to a DataProduct object.

    Returns:
        dict or DataProduct or None: The data product details as a dictionary or DataProduct object,
                                     depending on the value of `as_class`. Returns None if an error occurs.
    """
    if response.status_code == 200:
        if as_class:
            return data_product_json_to_class(response.json())
        return response.json()
    elif response.status_code == 403:
        print(f"Operation forbidden: {response}")
    elif response.status_code == 404:
        print(f"Data product not found: {response}")

    return None


def fetch_data_product_tags(connection_info, data_product_id):
    """
    Fetch the tags for a data product using a GET request.

    Args:
        connection_info (ConnectionInfo): The connection information for authentication.
        data_product_id (str): The ID of the data product to fetch tags for.

    Returns:
        Response: The HTTP response object.
    """
    url = (
        f"https://{connection_info.host}:{connection_info.port}"
        + f"/api/v1/dataProduct/tags/products/{data_product_id}"
    )
    headers = {
        "Accept": APPLICATION_JSON_TEXT,
        "Content-Type": APPLICATION_JSON_TEXT,
    }
    auth = (connection_info.user, connection_info.password)

    return requests.get(
        url, headers=headers, auth=auth, verify=STARBURST_SSL_VERIFICATION
    )


def process_fetch_data_product_tags_response(response, as_class):
    """
    Process the HTTP response for data product tags.

    Args:
        response (Response): The HTTP response object.
        as_class (bool): If True, convert the JSON response to a list of Tag objects.

    Returns:
        list: A list of tags, either as Tag objects or dictionaries.
    """
    if response.status_code == 200:
        json_tags = response.json()
        if as_class:
            return [Tag(id=tag.get("id"), value=tag.get("value")) for tag in json_tags]
        return json_tags

    handle_fetch_data_product_error(response)
    return None


def handle_fetch_data_product_error(response):
    """
    Print an error message based on the HTTP response status code.

    Args:
        response (Response): The HTTP response object.
    """
    error_message = {
        403: "Operation forbidden.",
        404: "Tags for the data product not found.",
    }.get(response.status_code, "An error occurred.")

    print(f"{error_message} Response: {response}")
