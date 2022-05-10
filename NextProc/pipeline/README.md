1. Move to the root of project.

2. Install Docker Image:

docker image build -t pipeline:lastest .
 

3. Run the Docker Container

docker run -d --name pipeline pipeline:lastest


4. Find the Continer Name

docker ps


5. Login the Docker Continer

docker exec -it container_name bash