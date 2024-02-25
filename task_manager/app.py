from flask import Flask
from flask_migrate import Migrate
import logging
from db import db
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_HEADER_TYPE'] = 'JWT'

    logging.basicConfig(filename='app.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    from auth import auth_blueprint
    from routes import task_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(task_blueprint)

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
