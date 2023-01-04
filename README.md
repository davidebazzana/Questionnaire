# Usage
## Locally
When using the flask development server or gunicorn, create a python venv, install the dependencies listed in the requirements file and set the `SECRET_KEY` environment variable:  
`python3 -m venv /path/to/new/virtual/environment`  
`source /path/to/new/virtual/environment/bin/activate`  
`python3 -m pip install --upgrade pip`  
`pip install -r /path/to/Questionnaire/services/questionnaire/requirements.txt`  
`export SECRET_KEY=some_random_value`   
`export STATISTICS_DB_PASSWORD=admin_password_for_postgres_db`   
Note: `SECRET_KEY` can be set to any value, since the server will run locally and in a development environment.
### Using the default flask development web server (not production!)
Initialize the database and import the content of the csv files inside it:  
`/path/to/Questionnaire/services/questionnaire$ flask --app questionnaire_app init-db`  
Start the flask server:  
`/path/to/Questionnaire/services/questionnaire$ flask --app questionnaire_app --debug run`  
  
### Using a Gunicorn web server
Initialize the database and import the content of the csv files inside it:  
`/path/to/Questionnaire/services/questionnaire$ flask --app questionnaire_app init-db`  
Start the Gunicorn server:  
`/path/to/Questionnaire/services/questionnaire$ gunicorn -w 2 --bind 0.0.0.0:5000 wsgi:app`  
  
### Dockerized
If the docker images of the app already exist, then just start the containers:  
`docker-compose up --build`   

## On the cloud (Azure)
If the docker images of the app already exists in a container registry, then all you need to do is to run a group of container based on those images.  
First, log in to azure with the docker login command:  
`docker login azure`  
Log in to your azure account using the azure cli:   
`az login --use-device-code`   
Log in to your azure container registry:   
`az acr login --name questionariomollami`   
Then create a context in order to perform the docker commands into the remote azure cloud:  
`docker context create aci questionariomollami`  
Switch to that context:  
`docker context use questionariomollami`  
Run the container:  
`docker compose up`  
To shut down the containers:  
`docker compose down`  
  
If the images do not exist in any container registry already then upload the images.  
First, log in to your azure account (only first access):  
`az login --use-device-code`  
Then create a resource group and a container register (if not existing already):  
`az group create --name questionnaire --location westeurope`  
`az acr create --resource-group questionnaire --name questionariomollami --sku Standard`  
Log in to your azure container registry (the registry must exists):  
`az acr login --name questionariomollami`  
Use the default context:  
`docker context use default`  
Push the docker image of the app to your azure container registry:  
`docker-compose push`  
In order to delete a specific image from the container registry:  
`az acr repository delete --name questionariomollami --image name_of_the_image:vX.X`  

## Connect, initialize and query remote PostgreSQL database on azure
In order to connect to the remote postgres db on azure run:   
`psql "host=mollami-log.postgres.database.azure.com port=5432 dbname=log user=mollami@mollami-log password=admin_password sslmode=require"`   
If it is the first time accessing a new azure postgresql server, then access the default database first:   
`psql "host=mollami-log.postgres.database.azure.com port=5432 dbname=postgres user=mollami@mollami-log password=admin_password sslmode=require"`   
Then, create the database:   
`CREATE DATABASE log;`   
Access the new database with:   
`\c log`   
Create the tables:   
`CREATE TABLE visit (id SERIAL, ts TIMESTAMP WITHOUT TIME ZONE default (now() at time zone 'utc'));`   
`CREATE TABLE log (id SERIAL, ts TIMESTAMP WITHOUT TIME ZONE default (now() at time zone 'utc'), result TEXT);`   

## Notes
All the commands relative to docker and azure cli may need `sudo` to work properly.   
   
A file .env is needed when the application runs on docker. The file .env should contain the following:   
```
SECRET_KEY=<the_secret_key_of_the_app>
STATISTICS_DB_PASSWORD=<the_password_of_the_postgresql_user>
```
