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
