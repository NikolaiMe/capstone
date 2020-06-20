# Capstone API

This project is the final project of the udacity Full Stack Developer nanodegree. I'm very glad and proud that I made it until here. The project description is the following: "The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process."

The following documentation describes all the tools which were used for the project and gives a clear documentation of all the APIs. 

The backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Installing Backend Dependencies

#### Python 3.8.2

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Python-JOSE] (https://pypi.org/project/python-jose/) can be used to encrypt and/or sign content using a variety of algorithms.

### Database Setup
If you want to do some offline testing you need to create a database for the app. Create a new database with the name "capstone_test"
With Postgres running, restore a database using the capstone_test.psql file provided. From the project folder in terminal run:
```bash
psql capstone_test < capstone_test.psql
```
After you set up the database make sure to change the Database URL in the setup.sh file. You will run that later to set your environment variables. Please adapt the variables "DATABASE_URL" and "TEST_DATABASE_URL".

### Running the server

From within the project directory first ensure you are working using your created virtual environment.

To run the server under MAC or Linux, execute:

```bash
source setup.sh
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Running setup.sh will set your Database URLs and the JWT-Authorization Token.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the capstone app as the application. 

### Running the Unittests

From within the project directory first ensure you are working using your created virtual environment.

To run the server under MAC or Linux, execute:

```bash
source setup.sh
python3 test_app.py
```

Running setup.sh will set your Database URLs and the JWT-Authorization Token.

### Setting up Postman for RBAC Tests

You find a Postman Collection in the project directory (udacity-fsnd-capstone.postman_collection). This postman collection is already set up completely. You only need to run all tests via runner.


### Creating Test JWT Tokens

Basically all JWT Tokens are already in the postman collection and in the setup.sh file, which sets the environment variables. But the tokens can expire (Auth0-tokens have a maximum expire time of 24 hours). If they expire you can follow the instructions below to create new tokens.

You can create Test JWT Tokens using Auth0. Go to the following login URL: https://fsnd-nikolai.eu.auth0.com/authorize?audience=capstone&response_type=token&client_id=xO47Gg7AfYoBNw8360bgGha5j7Umobh3&redirect_uri=http://localhost:8080/login-results

Use the following credentials to create new tokens:

| Token Type   | E-mail   | Password|
| ------------- |-------------- |-------------- |
|Executive Producer|executive_producer@udacity.com|ExecutiveProducer1|
|Casting Assistant|casting_assistant@udacity.com|CastingAssistant1|
|Casting Director|casting_director@udacity.com|CastingDirector1|

After you logged in with the credentials you are forwarded to an empty page. You can copy the JWT from the URL Fragment "access_token=".


## API Documentation

### Base URL
https://nikolaicapstone.herokuapp.com/

### Authentication
You need to authenticate yourself if you want to use the endpoints. Authentication is done via Auth0 JWT-Tokens. Please refer to "Creating Test JWT Tokens" if you need a new token.

### Error Handling
If anything goes wrong while you're using the capstone API you will get an Error. Every error includes an HTTP Error Code and a body which contains more information about the issue.

#### HTTP Error Codes
The following HTTP Error Codes are used:


| Error Codes   | Description   |
| ------------- |--------------:|
|400|bad request|
|404|Resource not found|
|422|unprocessable|
|401|unauthorized|
|403|forbidden|


#### Messages
Every response contains a `success` attribute. The `success` attribute is set to `False` as soon as an error occurs. 

#### Example for an error response
Errors are returned as JSON objects in the following format:
``` 
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

### Endpoint Library

#### GET /actors

This endpoint can be used to get all available actors. You can access this endpoint with jwt-tokens from every role.

Sample Request:
```
curl --location --request GET 'https://nikolaicapstone.herokuapp.com//actors' \
--header 'Authorization: Bearer {Token}'
```

Sample Response:
```
{
  {
    "actors": [
        {
            "age": 27,
            "gender": "female",
            "id": 2,
            "name": "Sarah"
        },
        {
            "age": 31,
            "gender": "female",
            "id": 4,
            "name": "Petra"
        },
        {
            "age": 31,
            "gender": "male",
            "id": 6,
            "name": "Peter"
        }
    ],
    "success": true
}
```

#### POST /actor

If you want to create a new actor in the database you can use POST /actors. You need to add three parameters to your request body:

* name
  * contains the name of the actor as string
* age
  * contains the age of the actor as number
* gender
  * contains the gender of the actor as string

If the creation was successful the endpoints returns a parameter "created" which contains the id of the newly created actor. You can access this endpoint with jwt-tokens from the role "Executive Producer" and "Casting Director".


Sample Request: 
```
curl --location --request POST 'https://nikolaicapstone.herokuapp.com//actors' \
--header 'Authorization: Bearer {Token}' \
--header 'Content-Type: application/json' \
--data-raw '{
	"name": "Peter",
    "age": 31,
    "gender": "male"
}'
```

Sample Response:
```
{
  "created": 30,
  "success": true
}
```

#### PATCH /actor/\<int:actor_id\>

You can use this API to change the data of the actor with the given actor id, if it exists. You can add one or more of the following parameters to your request body:

* name
  * contains the new name of the actor as string
* age
  * contains the new age of the actor as number
* gender
  * contains the new gender of the actor as string

It returns the id of the changed actor and the new dataset of the changed actor. You can access this endpoint with jwt-tokens from the role "Executive Producer" and "Casting Director".

```
curl --location --request PATCH 'https://nikolaicapstone.herokuapp.com//actors/21' \
--header 'Authorization: Bearer {Token} '\
--header 'Content-Type: application/json' \
--data-raw '{
	"name": "Peter Paul",
    "age": 31,
    "gender": "male"
}'
```

Sample Response:
```
{
    "actor": {
        "age": 31,
        "gender": "male",
        "id": 21,
        "name": "Peter Paul"
    },
    "changed": "21",
    "success": true
}
```

#### DELETE /actor/\<int:actor_id\>

This API will delete the actor with the given actor id from the database, if it exists. It returns the id of the deleted actor. You can access this endpoint with jwt-tokens from the role "Executive Producer" and "Casting Director".

Sample Request:
```
curl --location --request DELETE 'https://nikolaicapstone.herokuapp.com//actors/21' \
--header 'Authorization: Bearer {Token}
```

Sample Response:
```
{
  "deleted": 21,
  "success": true
}
```

#### GET /movie

This endpoint can be used to get all available actors. You can access this endpoint with jwt-tokens from every role.

Sample Request:
```
curl --location --request GET 'https://nikolaicapstone.herokuapp.com//movies' \
--header 'Authorization: Bearer {Token}'
```

Sample Response:
```
{
  {
    "movies": [
        {
            "id": 2,
            "name": "Harry Potter",
            "releasedate": "Thu, 21 Dec 2006 19:10:25 GMT"
        },
        {
            "id": 7,
            "name": "Spiderman 2",
            "releasedate": "Thu, 21 Dec 2006 19:10:25 GMT"
        }
    ],
    "success": true
}
```

#### POST /movie

If you want to create a new actor in the database you can use POST /actors. You need to add two parameters to your request body:

* name
  * contains the name of the movie as string
* releasedate
  * contains the releasedate of the movie as string with the following formatting: "YYYY-mm-DD HH:MM:SS"

If the creation was successful the endpoints returns a parameter "created" which contains the id of the newly created movie. You can access this endpoint with jwt-tokens from the role "Executive Producer".


Sample Request: 
```
curl --location --request POST 'https://nikolaicapstone.herokuapp.com//movies' \
--header 'Authorization: Bearer {Token}' \
--header 'Content-Type: application/json' \
--data-raw '{
	"name": "Spiderman 2",
    "releasedate": "2006-12-21 19:10:25"
}'
```

Sample Response:
```
{
  "created": 30,
  "success": true
}
```

#### PATCH /movie/\<int:movie_id\>

You can use this API to change the data of the movie with the given movie id, if it exists. You can add one or more of the following parameters to your request body:

* name
  * contains the name of the movie as string
* releasedate
  * contains the releasedate of the movie as string with the following formatting: "YYYY-mm-DD HH:MM:SS"

It returns the id of the changed movie and the new dataset of the changed movie. You can access this endpoint with jwt-tokens from the role "Executive Producer" and "Casting Director".

```
curl --location --request PATCH 'https://nikolaicapstone.herokuapp.com//movies/1' \
--header 'Authorization: Bearer {Token}' \
--header 'Content-Type: application/json' \
--data-raw '{
	"name": "Superman 2",
    "releasedate": "2020-12-21 23:10:23"
}'
```

Sample Response:
```
{
    "changed": "8",
    "movie": {
        "id": 8,
        "name": "Superman 2",
        "releasedate": "Mon, 21 Dec 2020 23:10:23 GMT"
    },
    "success": true
}
```

#### DELETE /movie/\<int:mobie_id\>

This API will delete the movie with the given movie id from the database, if it exists. It returns the id of the deleted movie. You can access this endpoint with jwt-tokens from the role "Executive Producer".

Sample Request:
```
curl --location --request DELETE 'https://nikolaicapstone.herokuapp.com//movies/8' \
--header 'Authorization: Bearer {Token}'
```

Sample Response:
```
{
  "deleted": 8,
  "success": true
}
```

## Acknowledgements

Thanks to all the udacity tutors for sharing your knowledge. Thanks to all the udacity reviewers for the great and very helpful feedback.

Special thanks to Sarah who pushed my progress and supported me in every project. Also special thanks to Christoph who inspired me to take this course and was a very good peer on this udacity journey.