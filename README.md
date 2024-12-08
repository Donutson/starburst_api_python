# STARBURST API PYTHON
L'objectif de ce package est de créer des data product sous starburst à partir de python, ce package fait usage de [l'api rest](https://docs.starburst.io/latest/api/index.html) de starburst pour pouvoir interagit avec votre instance de Starburst Enterprise

## Prérequis
Pour faire usage de ce package il faut avoir les éléments suivants
1. Une instance de starburst Entreprise
2. Python >= 3.7
3. trino
4. pandas
5. sqlalchemy
6. sqlalchemy-trino

## Installation

```shell
pip install git+https://github.com/Donutson/starburst_api_python.git
```

## Présentation du package

### classes/class_starburst_connection_info.py

Cette classe permet de définir un objet de connexion à une instance de starburst
```python
connection_info = StarburstConnectionInfo(
    host="127.0.0.1",
    user="starburst",
    password="starburst_pass",
    port="30443",
)
```

### classes/class_starburst_domain_info.py

Cette classe permet de définir un domain starburst
```python
domain = StarburstDomainInfo(
        name="test_api_python",
        description="creation de domain via python",
        schema_location="s3://starburst/Test_api_python/"
    )
```

### classes/class_relevant_link.py

Cette classe permet de définir un lien pour ajouter à son data product sous starburst
```python
link = RelevantLink(
        label="google",
        url="www.google.com",
    )
```

### classes/class_owner.py

Cette classe permet de définir un owner pour ajouter à son data product sous starburst
```python
owner = Owner(
        name="Jhon Doe",
        email="jhon@gmail.com",
    )
```

### classes/class_definition_properties.py

Cette classe permet de définir les propriétés d'un dataset de type materialized views d'un data product sous starburst
```python
property = DefinitionProperties(
        refresh_interval="1w",
        incremental_column="date_load",
    )
```

### classes/class_dataset_column.py

Cette classe permet de définir une colonne d'un dataset d'un data product sous starburst
```python
column = DatasetColumn(
        name="date_load",
        type="Date",
        description="Date de chargement des données",
    )
```

### classes/class_dataset_view.py

Cette classe permet de définir un dataset de type view d'un data product sous starburst
```python
dataset = DatasetView(
         name = "api_python_dataset",
         description = "dataset create from python api",
         definition_query = "select * from postgres.payment.client",
         columns = [
            DatasetColumn(
            name="date_load",
            type="Date",
            description="Date de chargement des données",
            ),
            DatasetColumn(
            name="name",
            type="Varchar",
            description="Nom du client",
            ),
            DatasetColumn(
            name="amount",
            type="Date",
            description="Montant payé",
            ),
          ]
         )
```

### classes/class_dataset_materialized_view.py

Cette classe permet de définir un dataset de type materialized view d'un data product sous starburst
```python
dataset =  DatasetMaterializedView(
         name = "api_python_dataset",
         description = "dataset create from python api",
         definition_query = "select * from postgres.payment.client",
         definition_properties = DefinitionProperties(
                                  refresh_interval="1w",
                                  incremental_column="date_load",
                              )
         columns = [
            DatasetColumn(
            name="date_load",
            type="Date",
            description="Date de chargement des données",
            ),
            DatasetColumn(
            name="name",
            type="Varchar",
            description="Nom du client",
            ),
            DatasetColumn(
            name="amount",
            type="Date",
            description="Montant payé",
            ),
          ]
         )
```

### classes/class_data_product.py

Cette classe permet de définir un data product sous starburst
```python
data_product = DataProduct(
         name = "api_python_product",
         catalog_name = "minio",
         data_domain_id = starburst_client.get_domain_by_name(domain.name)["id"],
         summary = "Data product create via api python",
         owners = [Owner(
                 name = "Nelson",
                 email = "nelson@gmail.com"
             )
         ],
         views = [DatasetView(
                     name = "api_python_dataset",
                     description = "dataset create from python api",
                     definition_query = "select * from postgres.payment.client",
                     columns = [...]
                     )]
     )
```

### classes/class_data_product.py

Cette classe nous permet d'interagir avec starburst pour créer, mettre à jour et supprimer des data products et des domains. On peut également exécuter des requêtes vers starburst et créer des vues [matérialisées], on ne mettra pas d'exemple de code et vous invitons à suire l'exemple d'utilisation plus bas.

### helpers/utils.py [read_excel_to_dataset_colums]
Cette fonction permet de lire un fichier excel définissant les champs d'un dataset et nous fournir une liste de DatasetColumn correspondant

### helpers/utils.py [create_excel_schema_from_starburst_table]
Cette fonction prend en entrée le nom d'une table et nous crée un fichier excel contenant le schéma de cette table (nom des champs, type des champs et description des champs si disponible)

## Exemple d'usage

```python
from starburst_api.classes.class_starburst_connection_info import StarburstConnectionInfo
from starburst_api.classes.class_data_product import DataProduct
from starburst_api.classes.class_owner import Owner
from starburst_api.classes.class_dataset_view import DatasetView
from starburst_api.classes.class_starburst_domain_info import StarburstDomainInfo
from starburst_api.classes.class_starburst import Starburst
from starburst_api.helpers.utils import read_excel_to_dataset_colums
from starburst_api.helpers.utils import create_excel_schema_from_starburst_table

# Création des instances de StarburstConnectionInfo et StarburstDomain
connection_info = StarburstConnectionInfo(
    host="127.0.0.1",
    user="starburst",
    password="starburst_pass",
    port="300402",
)

try:
    domain = StarburstDomainInfo(
        name="test_api_python",
        description="creation de domain via python",
        schema_location="s3://starburst/Test_api_python/"
    )

except ValueError as e:
    print(f"Error: {e}")
else:
    # Création de l'instance de Starburst
    starburst_client = Starburst(connection_info)
    
    # Utilisation de la méthode create_domain pour créer le domaine
    starburst_client.create_domain(domain)

    # List all domain
    print(starburst_client.list_domains())

    # Delete domain
    starburst_client.delete_domain_by_name(domain.name)

    # Create data product
    data_product = DataProduct(
        name = "api_python_product",
        catalog_name = "minio",
        data_domain_id = starburst_client.get_domain_by_name(domain.name)["id"],
        summary = "Data product create via api python",
        owners = [Owner(
                name = "Nelson",
                email = "nelson.gougou@orange.com"
            )
        ],
        views = [DatasetView(
                    name = "api_python_dataset",
                    description = "dataset create from python api",
                    definition_query = "select * from galera.omer_ht.suivi_solde_airtime",
                    columns = read_excel_to_dataset_colums("test_starburst_api.xlsx")
                    )]
    )
    starburst_client.create_data_product(data_product)

    # Find data product from domain
    product = starburst_client.get_data_product(domain.name, data_product.name)
    print(product)

    # Update data product
    starburst_client.update_data_product(DataProduct(
        id = product["id"],
        name = "api_python_product_v2",
        catalog_name = "minio",
        data_domain_id = product["dataDomainId"],
        summary = "Data product create via api python"
        )
    )

    # Delete data product
    starburst_client.delete_data_product(domain.name, "api_python_product")

    # Publish data product
    starburst_client.publish_data_product(domain.name, data_product.name)

    # Write table schema to excel
    create_excel_schema_from_starburst_table(connection_info,
        "postgres.ventes.clients",
        "test_schema.xlsx")

    # execute query
    query = """
    select * from postgres.ventes.clients
    """
    res = starburst_client.execute_query(query=query, to_pandas=False)

    # create materialized view
    res = starburst_client.create_mv_view(query=query,
    view_name="postgres.mv_views.ventes_clients",
    cron="0 5 * * *")
    print(res)

    # create view
    res = starburst_client.create_view(query=query,
    view_name="postgres.views.ventes_clients"
    )
    print(res)
```
