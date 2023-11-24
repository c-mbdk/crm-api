# crm-api
REST API created using Flask connected to a PostgreSQL DB (running on a local server but can be run using a Docker container)

A workflow has been set up to run integration tests on the API. The workflow configures a service container using the Postgres image and the same credentials required by the Flask app. After ensuring that the service is running, the environment is set up with the right packages, the app is run in the background and then the tests are executed. If all the tests pass, the Docker Image CI is triggered.

The Docker Image CI workflow builds the image, based on the Dockerfile, then pushes the image to DockerHub. This Docker Image CI is only triggered when the integration tests (Run Integration Tests via Pytest) workflow is successful. The integration tests workflow is only triggered by pull requests or pushes to the main branch.

## Project Structure
- app.py has the implementation for CRUD operations of the CRM API
- tests/ has the API tests written for the CRM API
- bootstrap.sh is the executable file which facilitates the start-up of the application

## Future enhancements
The next major step is to deploy the API.

There could also be more tests added to ensure that the API is thoroughly tested.

## How to run:

1. Ensure you have pipenv installed. More information on installing pipenv is available here: https://pipenv.pypa.io/en/latest/installation/

2. Activate the virtual environment:
```
$ pipenv shell
```

3. Connect to PostgreSQL via the shell:
```
$ psql -U username
```

4. After connecting, create database:
```
$ create database crm_api_db;
```

5. Update the connection variable if needed (line 13 of app.py)

Without Docker? Follow Steps 6 - 8
With Docker? Follow Steps 9 - 11

## Without Docker
6. From a new terminal shell, change to the root directory of the project:
```
$ cd crm-api
```

7. Run the application file:
```
$ python3 app.py
```

Alternatively, you can also run the application using the bootstrap executable file. Run the executable file like this and it will start up the application
```
./bootstrap.sh
```

Steps 3 & 4 can also be completed via the pgAdmin application, if a GUI is preferred.

8. To run the tests (from the root directory):
```
$ pytest tests/crm_test.py
```


## With Docker
9. Build the image:
```
$ docker build -t crm-api-img .
```

10. Run a new Docker container named crm-api
```
$ docker run -d -p 5000:5000 --name crm-api-ctner crm-api-img
```

11. Retrieve contacts from the dockerised instance:
```
$ curl http://localhost:5000/contacts
```
