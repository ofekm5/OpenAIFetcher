from app import db
from datetime import datetime

class Prompt(db.Model):
    __tablename__ = 'prompts'
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Prompt {self.id}: {self.prompt[:20]}>'

class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompts.id'), nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    prompt = db.relationship('Prompt', backref=db.backref('responses', lazy=True))

    def __repr__(self):
        return f'<Response {self.id} to Prompt {self.prompt_id}: {self.response[:20]}>'
