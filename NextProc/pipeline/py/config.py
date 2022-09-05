# -*- coding: utf-8 -*-

# #####################################################################################################
# Data ingestion config file for the nextProcurement project, adapted from TBFY.
# 
# This file contains configuration parameters for the data ingestion process.
#
# Author   : mnavas (UPM) [based on previous code]
# License  : Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Project  : Developed as part of the nextProcurement project
# Funding  : nextProcurement has received funding from the European Union
#####################################################################################################

import socket 
import os

# To conect to Fuseki
#VAR_NAME = os.environ['PLATFORM_IP']
#ip = socket.gethostbyname(VAR_NAME)

# To conect to Virtuoso locally
ip = "127.0.0.1"

logging = {
    "level": "INFO"
}

rml = {
    "rml_filename": "rmlmapper.jar",
    "mapping_filename": "rml-mappings/mapping.rml.ttl",
    "rml_input_filename": "outsiders_2021.parquet",
    "rml_output_filename": "output.nt"
}

jena_tools = {
    "riot_command": "riot"
}

virtuoso = {
    "virtuoso_url": "http://" + ip + ":8890", 
    "virtuoso_docker": "http://virtuoso:8890",
    #"fuseki_url": "http://" + ip + ":3030", 
    "dataset": "tbfy",
    "virtuoso_user" : "dba",
    "virtuoso_pass" : "dba"
}
