import os
from flask import Flask, jsonify, request, abort
from models import setup_db, db, Actors, Movies
from flask_cors import CORS
from flask_migrate import Migrate
from auth import AuthError, requires_auth
import sys


def create_app(test_config=None):

    # INITIALIZATION

    app = Flask(__name__)
    migrate = Migrate(app, db)
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

    # ENDPOINTS

    @app.route('/', methods=['GET'])
    def init():
        return '''
                    <h1>Welcome to the capstone project!</h1>
                    <p>This project is the final project
                    of the udacity Full Stack Developer nanodegree
                    by Nikolai Merz.</p>
                    <p>This is an API, without a frontend. For API
                    documentation and more information please check
                    <a href='https://github.com/NikolaiMe/capstone'>
                    this github repository</a></p>
                '''

    # Actor APIs

    '''
    GET /actors

    This API can be used to get all available actors
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(token):
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
    @requires_auth('post:actors')
    def create_actor(token):
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
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
        abort_code = None

        try:
            actor_to_delete = Actors.query.filter(
                Actors.id == actor_id).one_or_none()

            if actor_to_delete is None:
                abort_code = 404

            if abort_code is None:
                actor_to_delete.delete()
                return jsonify({
                    'success': True,
                    'deleted': actor_id
                })
        except BaseException:
            db.session.rollback()
            abort_code = 422
        finally:
            db.session.close

        if abort_code:
            abort(abort_code)

    '''
    PATCH /actors/<actor_id>

    This API can be used to change the data of an actor
    in the database
    '''
    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def change_actor(token, actor_id):
        abort_code = None

        try:
            actor_to_change = Actors.query.filter(
                Actors.id == actor_id).one_or_none()

            if actor_to_change is None:
                abort_code = 404

            body = request.get_json()

            if body is not None:
                new_actor_name = body.get('name', None)
                new_actor_age = body.get('age', None)
                new_actor_gender = body.get('gender', None)

            if abort_code is None:
                if new_actor_name is not None:
                    actor_to_change.name = new_actor_name

                if new_actor_age is not None:
                    actor_to_change.age = new_actor_age

                if new_actor_gender is not None:
                    actor_to_change.gender = new_actor_gender

                actor_to_change.update()

                return jsonify({
                    'success': True,
                    'changed': actor_id,
                    'actor': actor_to_change.format()
                })
        except BaseException:
            db.session.rollback()
            abort_code = 422
        finally:
            db.session.close

        if abort_code:
            abort(abort_code)

    # Basic movie APIs

    '''
    GET /movies

    This API can be used to get all available movies
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(token):
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
    @requires_auth('post:movies')
    def create_movie(token):
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
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):
        abort_code = None

        try:
            movie_to_delete = Movies.query.filter(
                Movies.id == movie_id).one_or_none()

            if movie_to_delete is None:
                abort_code = 404

            if abort_code is None:
                movie_to_delete.delete()
                return jsonify({
                    'success': True,
                    'deleted': movie_id
                })
        except BaseException:
            db.session.rollback()
            abort_code = 422
        finally:
            db.session.close

        if abort_code:
            abort(abort_code)

    '''
    PATCH /movie/<movie_id>

    This API can be used to change the data of a movie
    in the database
    '''
    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def change_movie(token, movie_id):
        abort_code = None

        try:
            movie_to_change = Movies.query.filter(
                Movies.id == movie_id).one_or_none()

            if movie_to_change is None:
                abort_code = 404

            body = request.get_json()

            if body is not None:
                new_movie_name = body.get('name', None)
                new_movie_releasedate = body.get('releasedate', None)

            if abort_code is None:
                if new_movie_name is not None:
                    movie_to_change.name = new_movie_name

                if new_movie_releasedate is not None:
                    movie_to_change.releasedate = new_movie_releasedate

                movie_to_change.update()

                return jsonify({
                    'success': True,
                    'changed': movie_id,
                    'movie': movie_to_change.format()
                })
        except BaseException:
            db.session.rollback()
            app.logger.error(sys.exc_info())
            abort_code = 422
        finally:
            db.session.close

        if abort_code:
            abort(abort_code)

    # ERROR HANDLING

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
