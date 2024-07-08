from flask import Blueprint, jsonify, request, current_app
from app.components.OpenAIFetcher import OpenAIQueryError
from app import db
from app.models import Prompt, Response
from marshmallow import ValidationError

bp = Blueprint('main', __name__)

@bp.route('/question', methods=['POST'])
def ask_question():
    data = request.get_json()

    try:
        sanitized_data = current_app.sanitizer.validate_post_request(data)
        if not sanitized_data or 'question' not in sanitized_data:
            current_app.logger.error('Missing question in request')
            return jsonify({'error': 'Missing question'}), 400

        question = sanitized_data.get('question')
        current_app.logger.info(f"Received question: {question}")

        prompt = Prompt.query.filter_by(prompt=question).first()
        if prompt:
            response = Response.query.filter_by(prompt_id=prompt.id).first()
            if response:
                return jsonify({'questionID': response.id, 'answer': response.response}), 200
            else:
                return jsonify({'error': 'Response not found for the existing prompt'}), 404
        else:
            try:
                current_app.logger.info('Scheduling query for new question')
                next_id = db.session.query(db.func.max(Prompt.id)).scalar()
                next_id = (next_id or 0) + 1 
                current_app.scheduler.schedule_question(question, str(next_id))
                new_prompt = Prompt(id=next_id, prompt=question)
                db.session.add(new_prompt)
                db.session.commit()
                return jsonify({'questionID': new_prompt.id}), 201
            except Exception as e:
                current_app.logger.error(f"Error processing question: {e}")
                return jsonify({'error': 'Internal server error'}), 500
    except ValidationError as err:
        return jsonify(err.messages), 400


@bp.route('/answer', methods=['GET'])
def fetch_answer():
    query_params  = request.args.to_dict()
    try:
        sanitized_data = current_app.sanitizer.validate_get_request(query_params)
        if not sanitized_data:
            current_app.logger.error('Missing questionID in request')
            return jsonify({'error': 'Missing questionID'}), 400

        response = Response.query.get(sanitized_data['questionID'])
        if response:
            current_app.logger.info(f'Returning answer for questionID {sanitized_data['questionID']}')
            return jsonify({'answer': response.response}), 200
        else:
            current_app.logger.error(f'Response not found for questionID {sanitized_data['questionID']}')
            return jsonify({'error': 'Response not found'}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400

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
