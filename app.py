import os
from flask import Flask
from models import setup_db, db
from flask_cors import CORS
from flask_migrate import Migrate

def create_app(test_config=None):

    app = Flask(__name__)
    migrate = Migrate(app,db)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()