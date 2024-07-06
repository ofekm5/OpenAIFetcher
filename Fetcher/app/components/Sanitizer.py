from flask_marshmallow import Marshmallow
from marshmallow import fields, validate, pre_load, ValidationError
import bleach
from components.Logger import create_logger

ma = Marshmallow()

class Sanitizer:
    class QuestionSchema(ma.Schema):
        question = fields.Str(required=True, validate=validate.Length(min=1))

        @pre_load
        def sanitize_question(self, data, **kwargs):
            if 'question' in data:
                data['question'] = bleach.clean(data['question'])
            return data

    def __init__(self, app) -> None:
        ma.init_app(app)
        self.question_schema = self.QuestionSchema()
        self.__logger = create_logger(__name__, 'logs/sanitizer.log')

    def validate_request(self, json_data):
        try:
            self.__logger.info('validating request')
            return self.question_schema.load(json_data)
        except ValidationError as err:
            self.__logger.error(f"Validation failed: {err.messages}")
            raise