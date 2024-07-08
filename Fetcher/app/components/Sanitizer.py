from flask_marshmallow import Marshmallow
from marshmallow import fields, validate, pre_load, ValidationError, Schema
import bleach
from app.components.Logger import create_logger

ma = Marshmallow()

class Sanitizer:
    class QuestionSchema(ma.Schema):
        question = fields.Str(required=True, validate=validate.Length(min=1))

        @pre_load
        def sanitize_question(self, data, **kwargs):
            if 'question' in data:
                data['question'] = bleach.clean(data['question'])
            return data

    class AnswerSchema(ma.Schema):
        questionID = fields.Int(required=True, validate=validate.Range(min=1))

    def __init__(self, app) -> None:
        ma.init_app(app)
        self.question_schema = self.QuestionSchema()
        self.answer_schema = self.AnswerSchema()
        self.__logger = create_logger(__name__, 'logs/sanitizer.log')

    def validate_post_request(self, json_data):
        try:
            self.__logger.info('validating POST request')
            return self.question_schema.load(json_data)
        except ValidationError as err:
            self.__logger.error(f"POST validation failed: {err.messages}")
            raise

    def validate_get_request(self, query_params):
        try:
            self.__logger.info('validating GET request')
            return self.answer_schema.load(query_params)
        except ValidationError as err:
            self.__logger.error(f"GET validation failed: {err.messages}")
            raise