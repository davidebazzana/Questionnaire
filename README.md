# Usage
## Locally
### Using the default flask development web server (not production!)
Initialize the database and import the content of the csv files inside it:  
`/path/to/Questionnaire/$ flask --app questionnaire_app init-db`  
Start the flask server:  
`/path/to/Questionnaire/$ flask --app questionnaire_app --debug run`  
  
### Using a Gunicorn web server
Initialize the database and import the content of the csv files inside it:  
`/path/to/Questionnaire/$ flask --app questionnaire_app init-db`  
Start the Gunicorn server:  
`/path/to/Questionnaire/$ gunicorn -w 2 --bind 0.0.0.0:5000 wsgi:app`  
  
### Dockerized
If a docker image of the app already exists, then just start the container:  
`docker run -p 5000:5000 --name questionnaire-container questionnaire gunicorn -w 2 --bind 0.0.0.0:5000 wsgi:app`  
If a docker image is not available then build the image (the project files must be available):  
`/path/to/Questionnaire/$ docker build -t questionnaire:vX.X .`  
Proceed and start the container.  
## On the cloud (Azure)
If a docker image of the app already exists in a container registry, then all you need to do is to run a container based on that image.  
First, login into azure:  
`docker login azure`
Then create a context in order to perform the docker commands into the remote azure cloud:  
`docker context create aci questionnaire`
Run the container:
`docker run -p 80:80 --name questionnaire-container questionnaire.azurecr.io/questionnairev:X.X gunicorn -w 2 --bind 0.0.0.0:80 wsgi:app`  
  
If no image exists in any container registry, then the image must be uploaded.  
First, login into your azure account:  
`az login --use-device-code`  
Then login into your azure container registry (the registry must exists):  
`az acr login --name questionnaire`  
Push the docker image of the app to your azure container registry:  
`docker --context default push questionnaire.azurecr.io/questionnaire:vX.X`  

## Notes
All the above commands may need `sudo` to work properly.