import os
from flask import Flask, jsonify
from models import setup_db, db
from flask_cors import CORS
from flask_migrate import Migrate
from auth import AuthError, requires_auth


def create_app(test_config=None):

    ### INITIALIZATION

    app = Flask(__name__)
    migrate = Migrate(app,db)
    setup_db(app)
    CORS(app)


    
    ### ROUTES
 
    ### Actor APIs

    '''
    GET /actors

    This API can be used to get all available actors    
    '''
    @app.route('/actors', methods=['GET'])
    def get_actors():
        return "actors"

    '''
    POST /actors

    This API can be used to create a new actor in the
    database    
    '''
    @app.route('/actors', methods=['POST'])
    def create_actor():
        return "new actor created"

    '''
    DELETE /actors/<actor_id>

    This API can be used to delete a specific actor
    from the database    
    '''
    @app.route('/actors/<actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        return "actor deleted"

    '''
    PATCH /actors/<actor_id>

    This API can be used to change the data of an actor
    in the database    
    '''
    @app.route('/actors/<actor_id>', methods=['PATCH'])
    def change_actor(actor_id):
        return "actor changed"


    ### Basic movie APIs

    '''
    GET /movies

    This API can be used to get all available movies    
    '''
    @app.route('/movies', methods=['GET'])
    def get_movies():
        return "movies"

    '''
    POST /movies

    This API can be used to create a new movie in the
    database    
    '''
    @app.route('/movies', methods=['POST'])
    def create_movie():
        return "new movie created"

    '''
    DELETE /movies/<movie_id>

    This API can be used to delete a specific movie
    from the database    
    '''
    @app.route('/movies/<movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        return "movie deleted"

    '''
    PATCH /movie/<movie_id>

    This API can be used to change the data of a movie
    in the database    
    '''
    @app.route('/movies/<movie_id>', methods=['PATCH'])
    def change_movie(movie_id):
        return "movie changed"

    '''
    Error Handling
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error
        }), e.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()