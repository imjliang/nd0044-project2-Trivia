import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10



def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [q.format() for q in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={'/': {'origins': '*'}})

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add(
      "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
      "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response

  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    format_categories = {cate.id: cate.type for cate in categories}
    if len(categories) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'categories': format_categories,
      'total_categories': len(format_categories)
    })


  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/questions", methods=['GET'])
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    categories = Category.query.order_by(Category.id).all()
    format_categories = {cate.id: cate.type for cate in categories}

    return jsonify(
      {
        "success": True,
        "questions": current_questions,
        "total_questions": len(Question.query.all()),
        "categories": format_categories,
        'currentCategory': None
      }
    )



  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
      abort(422)
    question.delete()
    return jsonify(
      {
        "success": True,
        "deleted": question.id,
      }
    )

  '''
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_questions():
    body = request.get_json()
    new_question = body.get("question", None)
    new_answer  = body.get("answer", None)
    new_difficulty= body.get("difficulty", None)
    new_category = body.get("category", None)
    search_term =  body.get("searchTerm", None)
    try:
      # do search if search_term exist; otherwise, create a new question
      if search_term:
        selection = Question.query.filter(Question.question.ilike("%" + search_term + "%"))
        current_questions = paginate_questions(request, selection)
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(current_questions),
          'currentCategory': None
        })
      else:
        if not (new_question and new_answer and new_difficulty and new_category):
          abort(422)

        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
        question.insert()

        return jsonify(
          {
            "success": True,
            "created": question.id,
            "question": question.format()
          }
        )
    except:
      abort(422)

  '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # done. Check search clause in create_questions()


  '''
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:category_id>/questions", methods=['GET'])
  def get_questionsPerCategory(category_id):
    category = Category.query.filter(Category.id == category_id).one_or_none()
    if category is None:
      abort(404)
    selection = Question.query.filter(Question.category == category_id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    return jsonify(
      {
        "success": True,
        "questions": current_questions,
        "total_questions": len(current_questions),
        'currentCategory': category.type
      }
    )

  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz_game():
    body = request.get_json()
    quiz_category = body.get('quiz_category', None)
    prev_questions = body.get('previous_questions', [])
    if not quiz_category:
      abort(422)
    # check that if category is specified
    if quiz_category['id'] == 0:
      questions = Question.query.all()
    else:
      questions = Question.query.filter(Question.category == quiz_category['id']).all()

    # filter out all previous question
    questions = [q for q in questions if q.id not in prev_questions]

    # if all questions has been played, return None
    if len(questions) == 0:
      return jsonify({
      'success': True,
      'question': None
    })

    question = random.choice(questions)
    return jsonify({
      'success': True,
      'question': question.format()
    })

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return (
      jsonify({"success": False, "error": 404, "message": "resource not found"}),
      404,
    )

  @app.errorhandler(422)
  def unprocessable(error):
    return (
      jsonify({"success": False, "error": 422, "message": "unprocessable"}),
      422,
    )

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

  @app.errorhandler(405)
  def methods_not_allowed(error):
    return jsonify({"success": False, "error": 405, "message": "methods not allowed"}), 405
  
  return app

    