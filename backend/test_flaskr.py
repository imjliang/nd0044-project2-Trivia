import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','0613', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_sent_requesting_category_if_not_exist(self):
        # send request with category_id = 10000
        res = self.client().get('/categories/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # check that if questions are returned
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        # send request with page = 10000
        res = self.client().get("/questions?page=10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_question_success(self):
        res = self.client().post("/questions", json={"question": "TestCase: what is emergency number", \
                                                     'answer': "911",\
                                                     'difficulty': 1,\
                                                     'category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # check that the question is returned
        self.assertTrue(len(data["question"]))

        # check that if the question is "what is emergency number"
        self.assertEqual(data["question"]["question"], "TestCase: what is emergency number")

        # check that if the answer is 911
        self.assertEqual(data["question"]["answer"], "911")

        # check that if the difficulty is 1
        self.assertEqual(data["question"]["difficulty"], 1)

        # check that if the category is 1
        self.assertEqual(data["question"]["category"], 1)

    def test_422_if_create_question_failed(self):
        # send request without answer
        res = self.client().post("/questions", json={"question": "what is emergency number", \
                                                     'difficulty': 1,\
                                                     'category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "what"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # check that the questions are returned
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_get_question_search_without_results(self):
        # send an unknown search_term request
        res = self.client().post("/questions", json={"searchTerm": "applejacks101"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    def test_get_questions_per_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # check that the category is Science
        self.assertEqual(data["currentCategory"], 'Science')

        # check that questions are returned
        self.assertTrue(data["questions"])

    def test_404_if_category_not_exist(self):
        # sent request with category_id = 1000
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question_success(self):
        # create a new question to be deleted
        question = Question(question='how old i am', answer="99",
                            category=1, difficulty=10)
        question.insert()

        # get the id of the new question
        question_id = question.id

        res = self.client().delete("/questions/%s" %question_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        # check that if the id is correct
        self.assertEqual(data["deleted"], question_id)

    def test_422_if_delete_question_fail(self):
        # send request with question_id = 10000
        res = self.client().delete("/questions/10000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'unprocessable')

    def test_play_quiz_success(self):
        res = self.client().post("/quizzes", json={"quiz_category": {'id': 1, 'type': 'Science'},
                                                   'previous_questions': [20, 21, 22]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # check that a question is returned
        self.assertTrue(data['question'])

        # check that category is 1
        self.assertEqual(data["question"]['category'], 1)

        # check that if it is a previous question
        self.assertTrue(data["question"]['id'] not in [20, 21, 22])

    def test_play_quiz_fail(self):
        # send request to quiz game without category
        res = self.client().post("/quizzes", json={'previous_questions': [20, 21, 22]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'unprocessable')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()