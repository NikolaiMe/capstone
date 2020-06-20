import os
from flask import Flask, jsonify, request, abort
from models import setup_db, db, Actors, Movies
from flask_cors import CORS
from flask_migrate import Migrate
from auth import AuthError, requires_auth
import sys



def create_app(test_config=None):

    ### INITIALIZATION

    app = Flask(__name__)
    migrate = Migrate(app,db)
    setup_db(app)
    CORS(app)

    
    '''
    Definition of the CORS response Header

    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    
    ### ENDPOINTS
 
    ### Actor APIs

    '''
    GET /actors

    This API can be used to get all available actors    
    '''
    @app.route('/actors', methods=['GET'])
    def get_actors():
        actorSelection = Actors.query.all()
        actors = [actor.format() for actor in actorSelection]

        return jsonify({
            'success': True,
            'actors': actors
        })

    '''
    POST /actors

    This API can be used to create a new actor in the
    database    
    '''
    @app.route('/actors', methods=['POST'])
    def create_actor():
        abort_code = None

        new_actor_name = None
        new_actor_age = None
        new_actor_gender = None

        # app.logger.info('POST /actors endpoint called')

        body = request.get_json()

        if body is not None:
            new_actor_name = body.get('name', None)
            new_actor_age = body.get('age', None)
            new_actor_gender = body.get('gender', None)

        try:
            if (new_actor_name is None
                    or new_actor_age is None
                    or new_actor_gender is None):
                # app.logger.error('there is something missing')
                abort_code = 422

            if abort_code is None:
                actor_to_insert = Actors(
                    name=new_actor_name,
                    age=new_actor_age,
                    gender=new_actor_gender)
                actor_to_insert.insert()
                return jsonify({
                    'success': True,
                    'created': actor_to_insert.id,
                })
        except BaseException:
            db.session.rollback()
            # app.logger.error(sys.exc_info())
            abort_code = 422
        finally:
            db.session.close

        if abort_code:
            abort(abort_code)

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
        movieSelection = Movies.query.all()
        movies = [movie.format() for movie in movieSelection]

        return jsonify({
            'success': True,
            'movies': movies
        })

    '''
    POST /movies

    This API can be used to create a new movie in the
    database    
    '''
    @app.route('/movies', methods=['POST'])
    def create_movie():
        abort_code = None

        new_movie_name = None
        new_movie_releasedate = None

        body = request.get_json()

        if body is not None:
            new_movie_name = body.get('name', None)
            new_movie_releasedate = body.get('releasedate', None)

        try:
            if (new_movie_name is None
                    or new_movie_releasedate is None):
                    abort_code = 422

            if abort_code is None:
                movie_to_insert = Movies(
                    name=new_movie_name,
                    releasedate=new_movie_releasedate)
                movie_to_insert.insert()
                return jsonify({
                    'success': True,
                    'created': movie_to_insert.id,
                })
        except BaseException:
            db.session.rollback()
            abort_code = 422
        finally:
            db.session.close

        if abort_code:
            abort(abort_code)

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