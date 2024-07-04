from flask_marshmallow import Marshmallow
from marshmallow import fields, validate, post_load
import bleach

class Sanitizer():
    class QuestionSchema(ma.Schema):
        username = fields.Str(required=True, validate=validate.Length(min=3))
        email = fields.Email(required=True)
        age = fields.Int(required=True, validate=validate.Range(min=18, max=99))
        
    def __init__(self, app) -> None:
        ma = Marshmallow(app)
        question_schema = QuestionSchema()

