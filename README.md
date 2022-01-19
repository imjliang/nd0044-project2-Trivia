# Full Stack API Final Project


## Full Stack Trivia

Trivia is an app designed for Udacity employees and students to create webpages and play games on a regular basis. The application has the following functionalities.

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Main Files: Project Structure

  ```sh
├── backend
│   ├── README.md
│   ├── flaskr *** the main driver of the app. Includes all endpoints 
│   │ 			"flask run" to run after installing dependencies
│   │ 	└── __init_.py
│   ├── models.py *** Database URLs and SQLAlchemy setup
│   ├── trivia.psql *** Template local database
│   ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
│   └── test_flaskr.py *** Tests for successful and failed operations 
└── frontend
    ├── README.md
    ├── package.json
    ├── package-lock.json      
    ├── public 
    │   ├── art.svg
    │   ├── delete.png
    │   ├── entertainment.svg
    │   ├── favicon.ico
    │   ├── geography.svg
    │   ├── index.html
    │   ├── mainfest.json
    │   ├── science.svg
    │ 	└── sports.svg
    └── src 
        ├── commponents
        │	├── FormView.js
        │   ├── Header.js
        │   ├── Question.js
        │   ├── QuestionView.js
        │   ├── QuizView.js
        │   └── search.js
        ├── stylesheets
        │	├── App.css
        │   ├── FormView.css
        │   ├── Header.css
        │   ├── index.css
        │   ├── Question.css
        │   └── QuizView.css
        ├── App.js
        ├── App.test.js
        ├── index.js
        ├── logo.svg
        └── serviceWorker.js
  ```

Overall:

* Models are located in the `MODELS` section of `models.py`.
* Controllers are located in `__init__.py`.
* The web frontend is located in `frontend/`.

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands (windows):

```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the frontend folder, run the following commands to start the client:

```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000.

### Tests

In order to run tests navigate to the backend folder and run the following commands:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Methods not allowed

### Endpoints

#### GET '/categories'

- General:
  - Fetches a list of question categories, success value, and total number of categories

- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

#### GET '/questions?page=${integer}'

- General:
  - Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
  - Request Arguments: page - integer
  - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category 

- Sample: `curl http://127.0.0.1:5000/questions?page=1`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 25
}
```

#### GET '/categories/${id}/questions'

- General:
  - Fetches questions for a cateogry specified by id request argument 
  - Request Arguments: id - integer
  - Returns: An object with questions for the specified category, total questions, and current category string 

- Sample: `curl http://127.0.0.1:5000/categories/5/questions`

```json
{
  "currentCategory": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#### POST '/questions'

- General:
  - Sends a post request in order to add a new question
  - Return the id of created questions, status code, and the question attributes.
- `Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{"question": "what is emergency number",  "answer": "911","difficulty": 1,"category": 1}"`

```json
{
  "created": 58,
  "question": {
    "answer": "911",
    "category": 1,
    "difficulty": 1,
    "id": 58,
    "question": "what is emergency number"
  },
  "success": true
}
```

#### POST '/questions'

- General:
  - Sends a post request in order to search for a specific question by search term 
  - Return a list of questions that match the search, status code, and the total number of questions.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{"searchTerm":"what"}"`

```json
{
  "currentCategory": null,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "911",
      "category": 1,
      "difficulty": 1,
      "id": 53,
      "question": "TestCase: what is emergency number"
    },
    {
      "answer": "911",
      "category": 1,
      "difficulty": 1,
      "id": 58,
      "question": "what is emergency number"
    }
  ],
  "success": true,
  "total_questions": 10
}
```

#### DELETE '/questions/${id}'

- General:
  - Deletes the question of the given ID if it exists. 
  - Returns the id of the deleted book, success value and total books.
- `curl -X DELETE http://127.0.0.1:5000/questions/31`

```json
{
  "deleted": 31,
  "success": true
}
```



## Deployment N/A

## Authors

Jinjin Liang authored the API (`__init__.py`), test suite (`test_flaskr.py`), and this README.
All other project files, including the models and frontend, were created by [Udacity](https://www.udacity.com/).

## Acknowledgements

The awesome team at Udacity and all of the students, soon to be full stack extraordinaires!

