# Coffee Shop Backend

# Full Stack Trivia API Backend

## Getting Started

### Pre-requisites

In order to run this project properly, make sure you have the following installed:
  * Python 3
  * Flask
  * SQL Alchemy
  * Jose - python-jose

## Initial Setup (Windows Based)
  1. Install the dependencies:
      ```
      pip install -r requirements.txt
      ```
  2. Set up the environment:
      ```
      $env:FLASK_ENV = "development"
      ```
  3. Set up the Flask App:
      ```
      $env:FLASK_APP = "api.py"
      ```
  4. Go to src folder and the run the app:
      ```
      flask run
      ```
  
## API Reference (Windows Based)
 * As mentioned at the Project Documentation README, this project was intended to run locally, thus the backend is hosted at the default ```http://127.0.0.1:5000/```, also set as an environment variable in the frontend configuration.
 * Authentication: This application uses Auth0 authentication and permission will be granted as users sign-in.

### Error Handling
The errors in this application are returned as JSON objects in the following format:
```
        {
          "success": False,
          "error": 404,
          "message": "Not found"
        }
```

This API handles the following errors:
* 400 - Bad Request
* 404 - Not Found
* 422 - Unprocessable Entity
* 500 - Internal Server Error



### Endpoints
There are 5 endpoints in this Application:
    1. GET/DRINKS
    2. GET/DRINKS-DETAIL
    3. POST/DRINKS
    4. PATCH/DRINKS/DRINK_ID
    5. DELETE/DRINKS/DRINK_ID
    
You can test them and check the documentation specific for each endpoint by using the postman collection located at the src folder.

