# crm-api
REST API created using Flask connected to a PostgreSQL DB (running on a local server but can be run using a Docker container)

Based on the concept of abstraction and clean architecture, the most recent changes to this API explore decoupling core logic, particularly business logic, from the infrastructure. The API no longer has explicit SQL statements, nor talks directly to the database. Instead, all operations are handled via a Contact service which initiates a unit of work to handle transactions and ensure data consistency. The unit of work creates abstraction between the data access layer and the business logic layer. This unit of work then uses the repository, which manages data access in a centralised manner and acts like the data is stored in memory. This simplifies the database operations for the application further, providing yet another layer of abstraction.

A workflow has been set up to run a full suite of tests (unit, integration, end-to-end) on the API. The workflow ensures the environment is set up with the right packages and the tests are executed. If all the tests pass, the Docker Image CI is triggered.

The Docker Image CI workflow builds the image, based on the Dockerfile, then pushes the image to DockerHub. This Docker Image CI is only triggered when the test suite (Run Test Suite for CRM API) workflow is successful. The test suite workflow is only triggered by pull requests or pushes to the main branch.

## Project Structure
- src/contacts/entrypoints/app/application.py has application factory function for the CRM API
- src/contacts/entrypoints/routes.py has the endpoints and methods where the CRUD operations can take place, using the service layer
- src has all of the files relevant for the application, including the domain model, the implementation of the unit of work, repository and service layer
- tests/ has the API tests written for the CRM API - unit, integration and end-to-end
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
$ FLASK_APP=run.py flask run
```

Alternatively, you can also run the application using the bootstrap executable file. Run the executable file like this and it will start up the application
```
./bootstrap.sh
```

Steps 3 & 4 can also be completed via the pgAdmin application, if a GUI is preferred.

8. To run the tests (from the root directory):
```
$ FLASK_APP=run.py flask test
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
