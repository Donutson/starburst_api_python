"""
Class to interact with a starburst instance
"""

import json
import pandas as pd
import requests
import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError, SQLAlchemyError

from starburst_api.classes.class_starburst_connection_info import (
    StarburstConnectionInfo,
)
from starburst_api.classes.class_starburst_domain_info import StarburstDomainInfo
from starburst_api.classes.class_data_product import DataProduct
from starburst_api.helpers.utils import (
    read_starburst_view_files,
    validate_query_path,
    map_view_config_fields,
    read_query_file,
    find_data_product,
    fetch_data_product,
    handle_fetch_data_product_response,
    fetch_data_product_tags,
    process_fetch_data_product_tags_response,
)
from starburst_api.helpers.variables import (
    APPLICATION_JSON_TEXT,
    STARBURST_SSL_VERIFICATION,
)


requests.packages.urllib3.disable_warnings()


class Starburst:
    """Provides methods to interact with Starburst."""

    def __init__(self, connection_info: StarburstConnectionInfo):
        """
        Initialize the Starburst client.

        Parameters:
            connection_info (StarburstConnectionInfo): to establish a connection with Starburst.
        """
        self.connection_info = connection_info

        password = urllib.parse.quote(self.connection_info.password)
        self.connection_string = (
            f"trino://{self.connection_info.user}:{password}@{self.connection_info.host}"
            + f":{self.connection_info.port}/{self.connection_info.catalog}/{self.connection_info.schema}"
        )

    def create_domain(self, domain: StarburstDomainInfo):
        """
        Create a domain in Starburst.

        Parameters:
            domain (StarburstDomain): The domain object to be created.
        """
        url = (
            f"https://{self.connection_info.host}:{self.connection_info.port}/"
            + "api/v1/dataProduct/domains"
        )
        headers = {
            "Accept": APPLICATION_JSON_TEXT,
            "Content-Type": APPLICATION_JSON_TEXT,
        }
        auth = (self.connection_info.user, self.connection_info.password)

        response = requests.post(
            url,
            headers=headers,
            auth=auth,
            json=domain.to_dict(),
            verify=STARBURST_SSL_VERIFICATION,
        )

        if response.status_code == 200:
            print(f"Domain {domain.name} created successfully")
        else:
            print(
                f"Failed to create domain {domain.name}. Status code: {response.status_code}"
            )
            print(response.text)

    def create_data_product(self, data_product: DataProduct):
        """
        Creates a data product on the server by sending a POST request to the API.

        This method constructs a URL to the data products endpoint and sends a POST request
        with the data product's information in JSON format. The method uses basic authentication
        and handles the server's response, printing success or failure messages based on the
        response status code received.

        Args:
            data_product (DataProduct): The DataProduct object to be created. The object should have
                                        methods for serializing itself to a dictionary.

        Returns:
            None: This method does not return anything but prints messages to indicate the status
                  of the request.
        """
        url = (
            f"https://{self.connection_info.host}:{self.connection_info.port}"
            + "/api/v1/dataProduct/products"
        )
        headers = {
            "Accept": APPLICATION_JSON_TEXT,
            "Content-Type": APPLICATION_JSON_TEXT,
        }
        auth = (self.connection_info.user, self.connection_info.password)

        response = requests.post(
            url,
            headers=headers,
            auth=auth,
            json=data_product.to_dict(),
            verify=STARBURST_SSL_VERIFICATION,
        )

        if response.status_code == 200:
            print(f"Data product {data_product.name} created successfully")
        else:
            print(
                f"Failed to create data product {data_product.name}."
                + "Status code: {response.status_code}"
            )
            print(response.text)

    def create_view_from_config(
        self, config: list = None, views_dir: str = None, strict: bool = False
    ):
        """
        Creates views from the provided configuration using a Starburst connection.

        Args:
            config (list): List of view configuration dictionaries.
            views_dir (str): Directory containing view configuration files.
            strict (bool, optional): If True, stops execution on the first error. Defaults to False.
        """

        def create_view_result_handler(res, view_name, view_type, strict):
            """
            Handle the result of the view creation.

            Args:
                res (int or other): Result of the view creation.
                view_name (str): Name of the view.
                view_type (str): Type of the view ("view" or "materialized_view").
                strict (bool): If True, stops execution on the first error.
            """
            if isinstance(res, int):
                print(f"Failed to create {view_type} {view_name}")
                if strict:
                    return
            else:
                print(f"{view_type.capitalize()} {view_name} was successfully created")

        if not config and not views_dir:
            print(
                "Please specify one of the following arguments 'config' or 'views_dir'"
            )
            return

        if views_dir:
            config = read_starburst_view_files(views_dir)

        mapped_fields = {
            "name": "view_name",
            "cron": "cron",
            "comment": "comment",
            "gracePeriod": "grace_period",
            "maxImportDuration": "max_import_duration",
            "incrementalColumn": "incremental_column",
            "partitionedBy": "partitioned_by",
        }

        for view_conf in config:
            if not validate_query_path(view_conf, strict):
                continue

            args = map_view_config_fields(view_conf, mapped_fields)
            query = read_query_file(view_conf["queryPath"])

            if view_conf.get("type") == "materialized_view":
                res = self.create_mv_view(query=query, **args)
                create_view_result_handler(
                    res, args.get("view_name"), "materialized view", strict
                )
            else:
                res = self.create_view(query=query, **args)
                create_view_result_handler(res, args.get("view_name"), "view", strict)

    def update_domain(self, domain: StarburstDomainInfo):
        """
        Update a domain's configuration in the Starburst Data Product system.

        This function sends a PUT request to the Starburst API to update the domain specified by `domain.id`.
        It handles different HTTP response status codes to provide appropriate feedback.

        Args:
            domain (StarburstDomainInfo): The domain information to update.

        Returns:
            int: The HTTP status code of the response.
        """
        url = (
            f"https://{self.connection_info.host}:{self.connection_info.port}/"
            + f"api/v1/dataProduct/domains/{domain.id}"
        )
        headers = {
            "Accept": APPLICATION_JSON_TEXT,
            "Content-Type": APPLICATION_JSON_TEXT,
        }
        auth = (self.connection_info.user, self.connection_info.password)

        response = requests.put(
            url,
            headers=headers,
            auth=auth,
            json=domain.to_dict(),
            verify=STARBURST_SSL_VERIFICATION,
        )

        if response.status_code == 200:
            print(f"Domain {domain.name} had been updated successfully")
        elif response.status_code == 400:
            print(f"Bad request when attempting to update domain {domain.name}")
        elif response.status_code == 403:
            print(f"Operation forbidden when attempting to update domain {domain.name}")
        elif response.status_code == 404:
            print(
                f"Operation not found  when attempting to update domain {domain.name}"
            )
        else:
            print(
                f"Failed to update domain {domain.name}. Status code: {response.status_code}"
            )
        print(response.text)
        return response.status_code

    def update_data_product(self, data_product: DataProduct):
        """
        Updates a specific data product on the server using a HTTP PUT request.

        This method sends a JSON representation of the DataProduct instance to the server
        to update the existing data product. The method constructs a URL targeting the
        specific data product by its ID and sends the updated data as JSON.

        Args:
            data_product (DataProduct): The data product instance to update. This object
                                        must have an 'id' attribute and a 'to_dict()' method
                                        that serializes its properties to a dictionary format.

        Returns:
            None: Int: Status code of the operation

        Side Effects:
            Prints messages to the console based on the HTTP status code returned by the
            server:

            - 200: Update successful.
            - 400: Bad request (e.g., malformed request body).
            - 403: Operation forbidden (e.g., insufficient permissions).
            - 404: Data product not found on the server.
            - 409: Conflict (e.g., concurrent modification conflict).
            - Other codes: Generic failure message with the status code.

        Example:
            >>> data_product = DataProduct(id="123", name="New Name", ...)
            >>> update_data_product(data_product)
            Data product has been updated successfully.

        Notes:

            - The data product instance must have a valid 'id' that exists on the server.
            - Ensure that the 'DataProduct' class has a 'to_dict' method which correctly

            serializes the data product's attributes to a dictionary.
        """
        url = (
            f"https://{self.connection_info.host}:{self.connection_info.port}/"
            + f"api/v1/dataProduct/products/{data_product.id}"
        )
        headers = {
            "Accept": APPLICATION_JSON_TEXT,
            "Content-Type": APPLICATION_JSON_TEXT,
        }
        auth = (self.connection_info.user, self.connection_info.password)

        response = requests.put(
            url,
            headers=headers,
            auth=auth,
            json=data_product.to_dict(),
            verify=STARBURST_SSL_VERIFICATION,
        )

        if response.status_code == 200:
            print(f"Data product {data_product.name} had been updated successfully")
        elif response.status_code == 400:
            print(f"Bad request when attempting to update domain {data_product.name}")
        elif response.status_code == 403:
            print(
                f"Operation forbidden when attempting to update domain {data_product.name}"
            )
        elif response.status_code == 404:
            print(
                f"Operation not found when attempting to update domain {data_product.name}"
            )
        elif response.status_code == 409:
            print(
                f"Conflict appeared when attempting to update domain {data_product.name}"
            )
        else:
            print(f"Failed to update data product. Status code: {response.status_code}")
        print(response.text)
        return response.status_code

    def get_domain_by_id(self, domain_id: str, as_class: bool = False):
        """
        Retrieve information about a domain by its ID.

        Args:
            domain_id (str): The ID of the domain to retrieve.
            as_class (bool, optional): If True, return the domain information as a
                                    StarburstDomainInfo object. If False, return
                                    the domain information as a dictionary.
                                    Default is False.

        Returns:
            StarburstDomainInfo or dict: The domain information. The format depends on
                                        the value of `as_class`:
                                        - If `as_class` is True: Returns a StarburstDomainInfo object.
                                        - If `as_class` is False: Returns a dictionary.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the HTTP request.

        Prints:
            str: Error messages if the operation is forbidden or not found.

        Examples:
            >>> get_domain_by_id("12345")
            {'name': 'Sales', 'description': 'Sales data domain', 'schemaLocation': 's3://sales-data'}

            >>> get_domain_by_id("12345", as_class=True)
            StarburstDomainInfo(name='Sales', description='Sales data domain', schema_location='s3://sales-data')
        """
        url = (
            f"https://{self.connection_info.host}:{self.connection_info.port}"
            + f"/api/v1/dataProduct/domains/{domain_id}"
        )
        headers = {
            "Accept": APPLICATION_JSON_TEXT,
            "Content-Type": APPLICATION_JSON_TEXT,
        }
        auth = (self.connection_info.user, self.connection_info.password)

        response = requests.get(
            url, headers=headers, auth=auth, verify=STARBURST_SSL_VERIFICATION
        )

        domain = response.json()

        if response.status_code == 200:
            if as_class:
                return StarburstDomainInfo(
                    id=domain["id"],
                    name=domain.get("name"),
                    description=domain.get("description"),
                    schema_location=domain.get("schemaLocation"),
                    assigned_data_products=domain.get("assignedDataProducts"),
                )
            return domain
        if response.status_code == 403:
            print(
                f"Operation forbidden when attempting to get domain {domain.get('name')}: {response}"
            )
        if response.status_code == 404:
            print(
                f"Operation not found when attempting to get domain {domain.get('name')}: {response}"
            )

        return None

    def get_domain_by_name(self, domain_name: str, as_class: bool = False):
        """
        Retrieves a domain by its name from the list of domains.

        This method searches through the list of domains obtained from `list_domains()` method.
        It compares each domain's 'name' attribute with the provided `domain_name`.
        If a match is found,it returns the domain.
        If no match is found, it prints a message and returns None.

        Args:
            domain_name (str): The name of the domain to search for.
            as_class (bool, optional): If True, return the domain information as a
                                    StarburstDomainInfo object. If False, return
                                    the domain information as a dictionary.
                                    Default is False.

        Returns:
            StarburstDomainInfo or dict: The domain information. The format depends on
                                        the value of `as_class`:
                                        - If `as_class` is True: Returns a StarburstDomainInfo object.
                                        - If `as_class` is False: Returns a dictionary.
        """
        domains_list = self.list_domains()

        for domain in domains_list:
            if domain["name"] == domain_name:
                if as_class:
                    return StarburstDomainInfo(
                        id=domain["id"],
                        name=domain["name"],
                        description=domain["description"],
                        schema_location=domain["schemaLocation"],
                        assigned_data_products=domain["assignedDataProducts"],
                    )
                return domain

        print(f"Domain {domain_name} not found")
        return None

    def get_data_product(
        self, domain_name: str, data_product_name: str, as_class: bool = False
    ):
        """
        Retrieve a specific data product by name from a specified domain.

        Args:
            domain_name (str): The name of the domain where the data product is located.
            data_product_name (str): The name of the data product to retrieve.
            as_class (bool, optional): If True, return the data product information as a DataProduct object.
                                    If False, return the data product information as a dictionary. Default is False.

        Returns:
            dict or DataProduct or None: If successful, returns the data product details as a dictionary or a
                                        DataProduct object, depending on the value of `as_class`. If the product
                                        is not found or another error occurs, prints an error message and returns None.

        Raises:
            KeyError: If the domain is not found, which could interrupt the retrieval of the domain ID.
        """
        domain = self.get_domain_by_name(domain_name)
        if not domain:
            print(f"Domain {domain_name} not found.")
            return None

        data_product = find_data_product(domain, data_product_name)

        if not data_product:
            print(
                f"Data product {data_product_name} not found on domain {domain_name}."
            )
            return None

        response = fetch_data_product(self.connection_info, data_product["id"])
        return handle_fetch_data_product_response(response, as_class)

    def get_data_product_details(self, domain_name: str, data_product_name: str):
        """
        Retrieves a specific data product details by name from a specified domain.

        This method constructs an API URL and sends a GET request to retrieve the data product
        identified by `data_product_name` within the domain specified by `domain_name`.
        The method formats the search criteria into the appropriate JSON structure
        and handles the response by either returning the JSON data of the product or
        by printing an error message if the product is not found or if an error occurs.

        Args:
            domain_name (str): The name of the domain where the data product is located.
            data_product_name (str): The name of the data product to retrieve.

        Returns:
            dict or int: If successful, returns the JSON response containing the data product details.
                         If the product is not found or another error occurs, prints an error message and
                         returns the HTTP status code.

        Raises:
            KeyError: If the domain is not found, which could interrupt the retrieval of the domain ID.
        """
        domain = self.get_domain_by_name(domain_name)

        if domain:
            url = f"https://{self.connection_info.host}:{self.connection_info.port}/api/v1/dataProduct/products"
            headers = {
                "Accept": APPLICATION_JSON_TEXT,
                "Content-Type": APPLICATION_JSON_TEXT,
            }
            auth = (self.connection_info.user, self.connection_info.password)
            search = {
                "dataDomainIds": [domain["id"]],
                "searchString": data_product_name,
            }
            data = {"searchOptions": json.dumps(search)}

            response = requests.get(
                url,
                headers=headers,
                auth=auth,
                params=data,
                verify=STARBURST_SSL_VERIFICATION,
            )

            if response.status_code == 200 and response.json():
                return response.json()[0]

            print(
                f"Data product {data_product_name} not found on domain {domain_name}."
                + f" Status code: {response.status_code}"
            )
            print(response.text)
            return response.status_code

        return None

    def get_data_product_tags(
        self, domain_name: str, data_product_name: str, as_class: bool = False
    ):
        """
        Retrieve tags for a specific data product within a domain.

        Args:
            domain_name (str): The name of the domain containing the data product.
            data_product_name (str): The name of the data product whose tags are to be retrieved.
            as_class (bool, optional): If True, return tags as a list of Tag objects.
                                        If False, return tags as a list of dictionaries.
                                        Default is False.

        Returns:
            list: A list of tags for the specified data product. The format of the tags
                depends on the value of `as_class`:
                - If `as_class` is True: Returns a list of Tag objects.
                - If `as_class` is False: Returns a list of dictionaries.

        Raises:
            ValueError: If the domain or data product is not found.
            requests.exceptions.RequestException: If an error occurs during the HTTP request.

        Prints:
            str: Error messages if the operation is forbidden or not found.
        """
        domain = self.get_domain_by_name(domain_name)
        if not domain:
            print(f"Domain {domain_name} not found.")
            return None

        data_product = find_data_product(domain, data_product_name)
        if not data_product:
            print(
                f"Data product {data_product_name} not found in domain {domain_name}."
            )
            return None

        response = fetch_data_product_tags(self.connection_info, data_product["id"])
        return process_fetch_data_product_tags_response(response, as_class)

    def list_domains(self):
        """
        Retrieve a list of domains from the server.

        Returns:
            dict or int: If the request is successful, returns a dictionary containing domain information.
                        If the request fails, returns the status code (int) of the response.

        Raises:
            (optional) Exception: Any additional exceptions that may occur during the execution of the method.
                                 For example, if there's an issue with the network or authentication.

        Note:
            This method sends a GET request to the server to retrieve the list of domains.
            The URL, headers, and authentication details are obtained from the connection information provided
            during the initialization of the class instance.
            If the request is successful (status code 200),
            the JSON response containing domain information is returned.
            If the request fails, the status code of the response is printed along
            with any error message received.
            It's important to note that the use of 'verify=False' in the request is
            for skipping SSL certificate verification.
            Depending on the server configuration and security requirements,
            this option may need to be adjusted.
        """
        url = f"https://{self.connection_info.host}:{self.connection_info.port}/api/v1/dataProduct/domains"
        headers = {
            "Accept": APPLICATION_JSON_TEXT,
            "Content-Type": APPLICATION_JSON_TEXT,
        }
        auth = (self.connection_info.user, self.connection_info.password)

        response = requests.get(
            url, headers=headers, auth=auth, verify=STARBURST_SSL_VERIFICATION
        )

        if response.status_code == 200:
            return response.json()

        print(response.text)
        return response.status_code

    def delete_domain_by_name(self, domain_name: str):
        """
        Delete a domain by its name.

        Args:
            domain_name (str): The name of the domain to be deleted.

        Returns:
            None

        Note:
            This method retrieves the list of domains using the `list_domains` method.
            It then iterates over the domains to find the one with a matching name.
            Once found, it constructs the URL for the DELETE request using the domain's ID.
            The DELETE request is sent to the server with the appropriate headers and authentication.
            If the request is successful (status code 204), a success message is printed.
            If the request fails due to insufficient permissions (status code 403),
            a relevant message is printed.
            If the request fails for any other reason,
            an error message along with the status code and response text is printed.
            If no domain with the specified name is found,
            a message indicating the absence of the domain is printed.
            It's important to note that the use of 'verify=False'
            in the request is for skipping SSL certificate verification.
            Depending on the server configuration and security requirements,
            this option may need to be adjusted.
        """
        domain = self.get_domain_by_name(domain_name)
        if domain:
            url = (
                f"https://{self.connection_info.host}:{self.connection_info.port}"
                + f"/api/v1/dataProduct/domains/{domain['id']}"
            )
            headers = {
                "Accept": APPLICATION_JSON_TEXT,
                "Content-Type": APPLICATION_JSON_TEXT,
            }
            auth = (self.connection_info.user, self.connection_info.password)

            response = requests.delete(
                url, headers=headers, auth=auth, verify=STARBURST_SSL_VERIFICATION
            )

            if response.status_code == 204:
                print(f"Domain {domain_name} had been successfully deleted")
            elif response.status_code == 403:
                print("Deletion forbidden")
            else:

                print(
                    f"Failed to delete domain {domain_name}. Status code: {response.status_code}"
                )
                print(response.text)

    def delete_data_product(
        self,
        domain_name: str,
        data_product_name: str,
        delete_product_ressources: str = "false",
    ):
        """
        Deletes a specified data product within a given domain.

        This method sends a request to delete a data product from the specified domain.
        It optionally skips deleting the underlying resources in Trino based on the `delete_product_resources`
        parameter. The function first retrieves the data product to ensure it exists. If found, it proceeds
        to send a deletion request.

        Args:
            domain_name (str): The domain in which the data product is located.
            data_product_name (str): The name of the data product to be deleted.
            delete_product_resources (str): A string, either 'true' or 'false', that specifies whether to
                                            skip deleting the Trino resources associated with the data product.
                                            'false' by default, which implies resources will also be deleted.

        Raises:
            ValueError: If the 'delete_product_resources' parameter is not 'true' or 'false'.
            Exception: If there are problems with the network, server, or other operational issues.

        Returns:
            None: This method prints the outcome of the delete operation, including success messages and any
                HTTP errors encountered, but does not return any values.

        Prints:
            str: Outputs the status of the operation to the console, indicating success, denial of permissions,
                or other errors encountered.
        """
        data_product = self.get_data_product(domain_name, data_product_name)
        if data_product:
            url = (
                f"https://{self.connection_info.host}:{self.connection_info.port}"
                + f"/api/v1/dataProduct/products/{data_product['id']}/workflows/delete"
            )
            headers = {
                "Accept": APPLICATION_JSON_TEXT,
                "Content-Type": APPLICATION_JSON_TEXT,
            }

            if delete_product_ressources not in ("false", "true"):
                raise ValueError(
                    "Arg delete_product_ressources must be 'false' or 'true'"
                )

            params = {"skipTrinoDelete": delete_product_ressources}
            auth = (self.connection_info.user, self.connection_info.password)

            response = requests.post(
                url,
                headers=headers,
                auth=auth,
                params=json.dumps(params),
                verify=STARBURST_SSL_VERIFICATION,
            )

            if response.status_code == 202:
                print(
                    f"Data product {data_product_name} of domain"
                    + f" {domain_name} had been successfully deleted"
                )
            elif response.status_code == 403:
                print(f"Deletion forbidden for data product {data_product_name}")
            else:

                print(
                    f"Failed to delete data product {data_product_name} of domain {domain_name}."
                    + f" Status code: {response.status_code}"
                )
            print(response.text)

    def publish_data_product(
        self, domain_name: str, data_product_name: str, force: str = "false"
    ):
        """
        Publishes a specified data product within a given domain.

        This method attempts to publish a data product by sending a POST request to the data product's publish API endpoint.
        The function first retrieves the data product using `get_data_product` to ensure it exists. If found, it proceeds
        to send a publish request with an optional 'force' parameter to override any existing data conflicts.

        Args:
            domain_name (str): The domain in which the data product is located.
            data_product_name (str): The name of the data product to be published.
            force (str): A string, either 'true' or 'false', that forces the publishing process to override conflicts.
                        Default is 'false'.

        Raises:
            ValueError: If the 'force' parameter is not 'true' or 'false'.
            Exception: If there are problems with the network, server, or other operational issues.

        Returns:
            None: This method prints the outcome of the publish operation, including success messages and any HTTP
                errors encountered, but does not return any values.

        Prints:
            str: Outputs the status of the operation to the console, indicating success or the type of error encountered.
        """
        data_product = self.get_data_product(domain_name, data_product_name)
        if data_product:
            url = (
                f"https://{self.connection_info.host}:{self.connection_info.port}"
                + f"/api/v1/dataProduct/products/{data_product['id']}/workflows/publish"
            )
            headers = {
                "Accept": APPLICATION_JSON_TEXT,
                "Content-Type": APPLICATION_JSON_TEXT,
            }

            if force not in ("false", "true"):
                raise ValueError("Arg force must be 'false' or 'true'")

            params = {"force": force}
            auth = (self.connection_info.user, self.connection_info.password)

            response = requests.post(
                url,
                headers=headers,
                auth=auth,
                params=json.dumps(params),
                verify=STARBURST_SSL_VERIFICATION,
            )

            if response.status_code == 202:
                print(
                    f"Data product {data_product_name} of domain"
                    + f" {domain_name} had been successfully publish"
                )
            elif response.status_code == 403:
                print(f"Publish forbidden for data product {data_product_name}")
            elif response.status_code == 404:
                print(
                    "Operation not found when attempting to publish data product {data_product_name}"
                )
            else:

                print(
                    f"Failed to publish data product {data_product_name} of domain {domain_name}."
                    + f" Status code: {response.status_code}"
                )
            print(response.text)

    def execute_query(
        self,
        query: str,
        to_pandas: bool = True,
        verify_ssl: bool = STARBURST_SSL_VERIFICATION,
    ):
        """
        Executes an SQL query on the Starburst (Trino) database and returns the results.

        Args:
            query (str): The SQL query to execute.
            to_pandas (bool): If True, returns the results as a pandas DataFrame,
                            otherwise returns a SQLAlchemy ResultProxy object.
            verify_ssl (bool): If True, SSL certificates will be verified. If False, SSL
                          certificates will not be verified. Default is True.

        Returns:
            pandas.DataFrame or sqlalchemy.engine.result.ResultProxy: The results of the SQL query,
                                                                    depending on the to_pandas argument.

        Description:
            This method constructs a connection string using the credentials and connection information
            stored in the object, creates an SQLAlchemy engine, and connects to execute the given SQL query.
            Depending on the value of the to_pandas argument, it either returns the raw results wrapped in a
            SQLAlchemy ResultProxy, which can be iterated over, or converts the results into a pandas DataFrame,
            which is useful for further data manipulation and analysis.
        """
        engine = create_engine(
            self.connection_string, connect_args={"verify": verify_ssl}
        )

        try:
            with engine.connect() as connection:
                result = connection.execute(query)

                if to_pandas:
                    # Convertir les résultats en DataFrame pandas
                    return pd.read_sql(query, connection)

            # Retourne les résultats bruts
            return result
        except DatabaseError as error_msg:
            print(f"Failed to connect to database: {error_msg}")
            return -1
        except SQLAlchemyError as error_msg:
            print(f"SQLAlchemy error occurred: {error_msg}")
            return -2

    def create_mv_view(self, query: str, view_name: str, cron: str, **options):
        """
        Creates a materialized view in the database with specified properties and scheduling.

        This method constructs and executes a SQL command to create a materialized view based on the given SQL query
        and scheduling parameters. It supports various options to customize the materialized view, such as
        incremental updates, partitioning, and a comment describing the view.

        Args:
            query (str): The SQL query that defines the materialized view's data.
            view_name (str): The name to assign to the materialized view.
            cron (str): A cron expression that defines the refresh schedule for the materialized view.
            **options (dict): Optional keyword arguments to further customize the materialized view:
                - comment (str): A comment to describe the materialized view. Defaults to an empty space.
                - grace_period (str): The grace period for late data handling, default is '10.00m'.
                - incremental_column (str): Column to use for incremental loading. If not provided, the view is not incremental.
                - max_import_duration (str): Maximum duration that the incremental import process is allowed to take, default is '1.00h'.
                - partitioned_by (list of str): A list of columns by which the view is to be partitioned. Provide as a string like 'col1, col2'.
                - run_as_invoker (bool or str): Whether to run the view refresh as the invoker's identity, default is 'false'.

        Returns:
            The result of the execute_query method, which may vary based on the underlying database and method implementation.
            Typically, this would be the raw result of the execution if `to_pandas` is False.

        Example:
            >>> create_mv_view(
                "SELECT * FROM minio.test.orders WHERE order_date >= CURRENT_DATE - INTERVAL '1' DAY",
                "daily_orders",
                "0 0 * * *",
                comment="Daily orders view",
                grace_period="15.00m",
                incremental_column="order_date",
                partitioned_by="order_date",
                run_as_invoker='true'
            )

        Note:
            The cron expression must be properly formatted according to the database's expected standards. Ensure that
            any optional parameters are provided in accordance with how they should be applied in the SQL command.
        """
        inc = "" if options.get("incremental_column") else "--"
        part = "" if options.get("partitioned_by") else "--"

        partitioned_by = options.get("partitioned_by", "").split(",")
        partitioned_by = [f"'{item.strip()}'" for item in partitioned_by]
        partitioned_by = ",".join(partitioned_by)

        mv_query = f"""
        CREATE MATERIALIZED VIEW {view_name}
        COMMENT '{options.get("comment", " ")}'
        WITH (
        cron = '{cron}',
        grace_period = '{options.get("grace_period",'10.00m')}',
        {inc}incremental_column = '{options.get("incremental_column")}',
        max_import_duration = '{options.get("grace_period",'1.00h')}',
        {part}partitioned_by = ARRAY[{partitioned_by}],
        run_as_invoker = {options.get("run_as_invoker",'false')}
        ) AS
        {query}
        """
        res = self.execute_query(mv_query, to_pandas=False)

        return res

    def create_view(self, query: str, view_name: str, **options):
        """
        Creates a SQL view with a specified name and query, including optional custom settings.

        This method constructs and executes a SQL command to create a view based on the given SQL query.
        It allows for the addition of an optional comment to describe the view, which can be included through keyword arguments.

        Args:
            query (str): The SQL query that defines the view's data. This query should be a valid SQL statement
                        that typically selects data from one or more tables.
            view_name (str): The name to assign to the view. This name must be unique within the database or schema
                            unless it is replacing an existing view.
            **options (dict): Optional keyword arguments to further customize the view:

                - comment (str): A comment to describe the view, providing context or documentation for
                                future reference. Default is an empty space if not specified.

        Returns:
            The result of the execute_query method, which might be a success message, error message, or any
            other data depending on the implementation of `execute_query`. The result will indicate whether
            the view creation was successful or if there were errors.

        Example:
            >>> create_view(
                "SELECT customer_id, sum(price) FROM sales GROUP BY customer_id",
                "minio.test.view_customer_sales",
                comment="Shows total sales by customer"
            )

        Note:
            The caller must ensure that the provided SQL query is syntactically correct and that the `view_name`
            does not conflict with existing names in the same namespace unless the intent is to replace an existing view.
            Optional parameters like 'comment' must be properly formatted as valid SQL comments.
        """
        mv_query = f"""
        CREATE VIEW {view_name}
        COMMENT '{options.get("comment", " ")}'
        AS
        {query}
        """
        res = self.execute_query(mv_query, to_pandas=False)

        return res
