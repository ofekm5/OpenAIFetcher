from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from components.Logger import create_logger
from components.OpenAIHandler import OpenAIFetcher
from components.Sanitizer import Sanitizer

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.logger = create_logger('app', 'logs/app.log')

    with app.app_context():
        from routes import routes, models
        db.create_all()
    
    app.logger.info('app created')

    app.sanitizer = Sanitizer(app)
    app.openAI_fetcher = OpenAIFetcher()

    return app
