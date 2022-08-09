# -*- coding: utf-8 -*-

# #####################################################################################################
# Data ingestion script for the TBFY Knowledge Graph (http://data.tbfy.eu/). 
# Modified for the project Next Procurement.
# 
# This file contains configuration parameters for the data ingestion process.
#####################################################################################################
import socket 
import os

# Para conectarse con Fuseki
#VAR_NAME = os.environ['PLATFORM_IP']
#ip = socket.gethostbyname(VAR_NAME)

#Para conectarse con Virtuoso en local
ip = "127.0.0.1"

logging = {
    "level": "INFO"
}

openopps = {
    "api_url": "https://api.openopps.com/api/",
    "page_size": 1000,
    "sleep": 5
}

# opencorporates = {
#     "reconcile_api_url": "https://reconcile.opencorporates.com",
#     "reconcile_score": 60,
#     "companies_api_url": "http://api.opencorporates.com",
#     "smart_address_check": False,
#     "country_name_codes_simulation": False,
#     "use_cached_company_database": True,
#     "cached_company_database_retention_days": 100,
#     "cached_company_database_filename": "shelve/company_database_dict"
# }

rml = {
    "rml_filename": "rmlmapper.jar",
    "mapping_filename": "mapping.ttl",
    # "rml_input_filename": "input.xml",
    "rml_input_filename": "outsiders_2021.parquet",
    "rml_output_filename": "output.nt"
}

jena_tools = {
    "riot_command": "riot"
}

virtuoso = {
    "virtuoso_url": "http://" + ip + ":8890", 
    #"fuseki_url": "http://" + ip + ":3030", 
    "dataset": "tbfy",
    "virtuoso_user" : "dba",
    "virtuoso_pass" : "dba"
}
