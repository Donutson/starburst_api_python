"""
UTILITIES FUNCTIONS
"""
import pandas as pd
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
        connect_args={"http_scheme": "https", "verify": False},
    )

    if not len(table_name.split(".")) == 3:
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
