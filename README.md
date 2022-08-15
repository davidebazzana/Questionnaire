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
## Dockerized
If a docker image of the app already exists, then just start the container:  
`docker run -p 5000:5000 --name questionnaire-container questionnaire gunicorn -w 2 --bind 0.0.0.0:5000 wsgi:app`  
If a docker image is not available then build the image (the project files must be available):  
`/path/to/Questionnaire/$ docker build -t questionnaire:vX.X .`  
Proceed and start the container.