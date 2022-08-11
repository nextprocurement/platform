# platform
this repository contains a docker with:  
  - The data processing pipeline with an API ready for data reception and connected to virtuoso for publishing the prepared data.  
  - An instance of virtuoso for persistently linked data storage.   
  - A sparql endpoint ready to receive queries.  
  - A simple web page explaining the status of the project, its steps, some examples and offering a direct link to perform the sparql queries.

## Basic Overview

Easy deployment of nextProcurement tools and services into a local environment.

## Quick Start

1. Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/)
1. Clone this repo

	```
	git clone https://github.com/nextprocurement/platform.git
1. Enter to the folder NextProc and run the platform by:
    ```
	cd platform/NextProc
    sudo docker-compose up --build -d
    ```
If there is a problem with virtuoso, you must add your folder to Docker file sharing and retry.

1. Wait for all services to be available. The first time it may take a few minutes to download the Docker images.
    ```
    sudo docker-compose logs -f
	```
1. Process preprocess the parquet file (that must be placed in the data folder): 
    ```
    sudo python3 ./pipeline/py/applyRules.py -i data -o out -r 'pipeline/py/rml-mappings/mapping.rml.ttl'
	```
	If at any point a module is missing, install it using "sudo pip install moduleName" (there is also a requirement.txt file available).
1. Initialize the RDF repository
    1. Go to the Virtuoso administration GUI, [http://localhost:8890](http://localhost:8890)
    1. Create a new dataset `tbfy` following the instructions below:
	    1. Go to Virtuoso conductor and log in (dba/dba)
		1. Go to the tab System Admin > User Accounts.
		1. Grant permission SPARQL_UPDATE to the user SPARQL
		1. Go to http://localhost:8890/sparql/ and create the tbfy graph querying the following: 
		```
		CREATE GRAPH <http://127.0.0.1:8890/tbfy>
		```
1. Upload the triples to the graph (depending on the size it may take time; timeout is set to 300s): 
    ```
    sudo python3 ./pipeline/py/publish_rdf.py -i out
	```

1. That's all! 

