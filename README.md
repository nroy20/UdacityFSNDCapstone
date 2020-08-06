# Casting Agency

This app is a tool that can be used by a casting agency to record and list their movies and the actors they cast in them for organizational purposes. Functions include adding, deleting, modifying or retrieving any actor or movie in the website's database.
Link to website: udacity-fsnd-capstone-v1.herokuapp.com

Example login credentials for Casting Assistant role:
- Email: xxfcmcjnxrpawuwgqj@awdrt.com
- Password: user1!!!

Project reviewers will be provided with login credentials for other roles as well. These can be used to produce new tokens for testing should the provided ones expire.

Please note that the login function has not been completed yet. It will redirect you back to the home page, and an access token will be available in the URL after login.

## Motivation
I chose this project because it seemed like a simple concept that would allow me to focus on utilizing the skills I learned throughout this course. Overall, I felt that this CRUD app was a good demonstration of the progress I've made over the past few months.

## Getting Started

### Installing dependencies

After cloning this project onto your machine, navigate into the directory and run
`pip install -r requirements.txt
` in order to install all the dependencies required to run this project.

### Database Setup

After ensuring that Postgres is running, set the database path in Models.py.

### Running the server

Run:
`FLASK_APP=app.py flask run`

## Roles
There are 3 roles enabled for this app, as follows:
- Casting Assistant
    - Can view all actors and movies
- Casting Director
    - All permissions allowed for Casting Assistant
    - Can add and delete actors from database
    - Can modify all actors and movies
- Executive Producer
    - All permissions allowed for Casting Director
    - Can add or delete movies from database

These roles were enabled using the third-party authorization service Auth0. In order to access a given endpoint, a request must be made with a valid access token that supports the permissions required for that endpoint. While login has not fully been set up yet, endpoints can still be accessed via cURL or Postman.

## Endpoints
- GET /actors
    - Retrieves all actors from the database
    - Example response:
    ```
    {
        "success": true,
        "actors": [
            {
                "id": 1,
                "name": "actor 1",
                "age": "25",
                "gender": "Female"
            }
        ]
    }
    ```
- GET /movies
    - Retrieves all movies from the database
    - Example response:
    ```
    {
        "success": true,
        "movies": [
            {
                "id": 1,
                "title": "movie 1",
                "release_date": "01-01-2001"
            }
        ]
    }
    ```
- GET /actors/id
    - Retrieves specific information about actor with given id
    - Example response:
    ```
    {
        "success": true,
        "id": 1
    }
    ```
- GET /movies/id
    - Retrieves specific information about movie with given id
    - Example response:
    ```
    {
        "success": true,
        "id": 1
    }
    ```
- POST /actors/add
    - Adds new actor to database
    - Example response:
    ```
    {
        "success": true,
        "name": "new actor",
        "age": 22,
        "gender": "Male"
    }
    ```
- POST /movies/add
    - Adds new movie to database
    - Example response:
    ```
    {
        "success": true,
        "title": "new movie",
        "release_date": "01-01-2001"
    }
    ```
- DELETE /actors/id
    - Deletes actor from database
    - Example response:
    ```
    {
        "success": true,
        "id": 2
    }
    ```
- DELETE /movies/id
    - Deletes movie from database
    - Example response:
    ```
    {
        "success": true,
        "id": 2
    }
    ```
- PATCH /actors/id/edit
    - Modifies existing actor details
    - Example response:
    ```
    {
        "success": true,
        "name": "modified actor",
        "age": 22,
        "gender": "Male"
    }
    ```
- PATCH /movies/id/edit
    - Modifies existing movie details
    - Example response:
    ```
    {
        "success": true,
        "title": "modified movie",
        "release_date": "01-01-2001"
    }
    ```

## Tests
In order to run tests, update the database name and path variables in setUp() in the tests.py file. If necessary, update tokens. Then run `python tests.py`


