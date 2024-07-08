from flask import Flask
from app.components.Logger import create_logger
from app.components.Scheduler import Scheduler
from app.components.Sanitizer import Sanitizer
from .database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.logger = create_logger('app', 'logs/app.log')

    with app.app_context():
        from app import models 
        from app.routes import bp as main_bp
        db.create_all()

        app.logger.info('app created')
        app.sanitizer = Sanitizer(app)
        app.scheduler = Scheduler()
        app.register_blueprint(main_bp)

    return app
