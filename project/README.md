# Project :
  Our Project uses the assignment infrastructure code base as the fundamental
building block for project.

# Architecture

The project seperates the building blocks of the appplication to 3 different
dockers in deployment.
    - A Docker for running the Web Server
    - A Docker for running the application Server
    - A Docker for running the Database (Mongo DB)
    - In the Deployment glue these containers using Docker Networking

*NOTE* : There is no assumption that the applicaton would be deployed on only one server
    

## Why choose this Architecture ?
The application architecture is based on micro-services. This is a disaggregated
architecture. Say if the application needs to scale, we can take any of the 
components and run them in different servers. With very little changes in 
configuration all the infrastructure can be made to work seamlessly and scale 
up to serve more users.


*TODO:* redo the bottom part of the write up

# Bringing up the uWSGI server and routing the traffic through Nginx

## Manual Steps to create a web application stack using nginx-uWSGI-flask

- Step 1: Create a requirments.txt file with dependencies for python application
- Step 2: Create an projectapp.py file with web application logic
- Step 3: Create an projectapp.ini file with uWSGI operation logic
- Step 4: Build the flask docker image
- Step 5: Create an projectapp.conf file with configuration for routing traffic to uWSGI
- Step 6: Build the nginx docker image
- Step 7: Create the docker compose yaml file
- Step 8: Run the below command for building and deploying
    ```
    docker build -t my-flask -f Dockerfile-flask .
	docker build -t my-nginx -f Dockerfile-nginx .
	docker network create my-network
	docker run -d --name flask --net my-network -v "./project_app" my-flask
	docker run -d --name nginx --net my-network -p "80:80" my-nginx
    ```


# Assignemnt2: Design and Build an Online Bookstore Enterprise Database

## Manual Steps to bring up the mongodb container

```
docker build -t my-mongodb -f Dockerfile-mongodb .
docker run -d --name mongodb  -d -v /tmp/mongodb:/data/db -p 27017:27017 my-mongodb
```


# Build, deploy and Clean
./deploy-project.sh -h


