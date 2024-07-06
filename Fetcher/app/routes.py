from flask import Blueprint, jsonify, request, current_app
from components.OpenAIHandler import OpenAIQueryError
import asyncio
from app import db
from app.models import Prompt, Response

bp = Blueprint('main', __name__)

@bp.route('/ask', methods=['POST'])
def ask_question():
    current_app.logger.info('Scheduling query for question 1')
    asyncio.run(current_app.openAI_fetcher.send_query_and_store_result("what is the capital of France?", "1"))
    return jsonify({'questionID': 'TODO'}), 201

    # Check if available in DB, return json accordingly
    # data = request.get_json()

    # if not data or 'question' not in data:
    #     app.logger.error('Missing question in request')
    #     return jsonify({'error': 'Missing question'}), 400

    # question = data.get('question')
    # app.logger.info(f"Received question: {question}")

    # try:
    #     answer = openAI_handler.sendQuery(question)
    # except Exception as e:
    #     app.logger.error(f"Error processing question: {e}")
    #     return jsonify({'error': 'Internal server error'}), 500

@bp.route('/answer', methods=['GET'])
def fetch_answer():
    current_app.logger.info('Returning answer for question 1')
    return jsonify({'answer': 'TODO'}), 201

@bp.errorhandler(OpenAIQueryError)
def handle_openai_query_error(e):
    current_app.logger.error(str(e))
    response = jsonify({"error": str(e)})
    response.status_code = 500
    return response

@bp.errorhandler(500)
def handle_500_error(e):
    current_app.logger.error(e)
    response = jsonify({"error": "Internal Server Error"})
    response.status_code = 500
    return response
