from flask import Flask, jsonify, request
from components.OpenAIHandler import OpenAIHandler, OpenAIQueryError
import logging
from logging.handlers import RotatingFileHandler
# from components import DBClient
# from components import Sanitizer

app = Flask(__name__)
#sanitizer = Sanitizer(app)
openAI_handler = OpenAIHandler()

@app.route('/ask', methods=['POST'])
def ask_question():
    #check if available in DB, return json accordingly
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
    answer = openAI_handler.schedule_query("what is the capital of France?", "1")

    return jsonify({'answer': answer}), 201

@app.route('/answer', methods=['POST'])
def fetch_answer():
    return jsonify({'answer': 'TODO'}), 201


@app.errorhandler(OpenAIQueryError)
def handle_openai_query_error(e):
    app.logger.error(str(e))
    response = jsonify({"error": str(e)})
    response.status_code = 500
    return response

@app.errorhandler(500)
def handle_500_error(e):
    response = jsonify({"error": "Internal Server Error"})
    response.status_code = 500
    return response

def init_logger():
    file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 10, backupCount=10)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

if __name__ == '__main__':
    init_logger()
    app.run(debug=True)

