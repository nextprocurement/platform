# platform
this repository contains a docker with:  
  - The data processing pipeline with an API ready for data reception and connected to virtuoso for publishing the prepared data.  
  - An instance of virtuoso for persistently linked data storage.   
  - A sparql endpoint ready to receive queries.  
  - A simple web page explaining the status of the project, its steps, some examples and offering a direct link to perform the sparql queries.


 ```
    docker-compose up -d
    ```
1. Wait for all services to be available (e.g. `Started Application in xx.xx seconds`). The first time it may take a few minutes to download the Docker images.
    ```
    docker-compose logs -f
	```