import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('nikol', 'hallo', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


    # ACTOR TESTS
    def test_get_all_actors(self):      
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        
        for actor in data['actors']:
            self.assertTrue(actor['id'])
            self.assertTrue(actor['name'])
            self.assertTrue(actor['age'])
            self.assertTrue(actor['gender'])
       
    def test_404_get_all_actors(self):
        res = self.client().get('/actorz')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_create_new_actor(self):
        actor_to_be_created={
            'name': 'Nikolai',
            'age': 27,
            'gender': 'male'
        }

        res = self.client().post('/actors', json = actor_to_be_created)
        data = json.loads(res.data)

        new_actor = Actors.query.get(data['created'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertEqual(new_actor.name, actor_to_be_created['name'])
        self.assertEqual(new_actor.age, actor_to_be_created['age'])
        self.assertEqual(new_actor.gender, actor_to_be_created['gender'])

    def test_422_create_new_actor(self):
        actor_to_be_created={
            'name': 'Nikolai',
            'gender': 'male'
        }

        res = self.client().post('/actors', json = actor_to_be_created)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    
    def test_delete_actor(self):
        actor_id_to_delete = Actors.query.first().id
        res = self.client().delete('/actors/{}'.format(actor_id_to_delete))
        data = json.loads(res.data)
        deleted_actor = Actors.query.get(actor_id_to_delete)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertIsNone(deleted_actor)

    def test_404_delete_actor(self):
        actor_id_to_delete = Actors.query.order_by(Actors.id.desc()).first().id + 1
        res = self.client().delete('/actors/{}'.format(actor_id_to_delete))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    
    def test_change_actor(self):
        changes_to_be_made={
            'name': 'Changed_Name',
            'gender': 'Changed_Gender'
        }
        actor_id_to_change = Actors.query.first().id
        res = self.client().patch('/actors/{}'.format(actor_id_to_change), json = changes_to_be_made)
        data = json.loads(res.data)
        changed_actor = Actors.query.get(data['changed'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['changed'])
        self.assertTrue(data['actor'])
        self.assertEqual(changed_actor.name, changes_to_be_made['name'])
        self.assertEqual(changed_actor.gender, changes_to_be_made['gender'])

    def test_404_change_actor(self):
        changes_to_be_made={
            'name': 'Changed_Name',
            'gender': 'Changed_Gender'
        }
        actor_id_to_change = Actors.query.order_by(Actors.id.desc()).first().id + 1
        res = self.client().patch('/actors/{}'.format(actor_id_to_change), json = changes_to_be_made)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    
    # MOVIE TESTS

    def test_get_all_movies(self):      
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        
        for movie in data['movies']:
            self.assertTrue(movie['id'])
            self.assertTrue(movie['name'])
            self.assertTrue(movie['releasedate'])
       
    def test_404_get_all_movies(self):
        res = self.client().get('/moviez')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_new_movie(self):
        movie_to_be_created={
            'name': 'Lord of the Rings',
            'releasedate': '2016-06-22 19:10:25'
        }

        res = self.client().post('/movies', json =  movie_to_be_created)
        data = json.loads(res.data)

        new_movie = Movies.query.get(data['created'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertEqual(new_movie.name, movie_to_be_created['name'])
        self.assertTrue(new_movie.releasedate.strftime("%Y-%m-%d %H:%M:%S"), movie_to_be_created['releasedate'])

    def test_422_create_new_movie(self):
        movie_to_be_created={
            'name': 'Lord of the Rings',
        }

        res = self.client().post('/actors', json = movie_to_be_created)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    
    def test_delete_movie(self):
        movie_id_to_delete = Movies.query.first().id
        res = self.client().delete('/movies/{}'.format(movie_id_to_delete))
        data = json.loads(res.data)
        deleted_movie = Movies.query.get(movie_id_to_delete)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '{}'.format(movie_id_to_delete))
        self.assertIsNone(deleted_movie)

    def test_404_delete_movie(self):
        movie_id_to_delete = Movies.query.order_by(Movies.id.desc()).first().id + 1
        res = self.client().delete('/movies/{}'.format(movie_id_to_delete))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_change_movie(self):
        changes_to_be_made={
            'name': 'Changed_Name',
            'releasedate': '2000-01-01 00:00:00'
        }
        movie_id_to_change = Movies.query.first().id
        res = self.client().patch('/movies/{}'.format(movie_id_to_change), json = changes_to_be_made)
        data = json.loads(res.data)
        changed_movie = Movies.query.get(data['changed'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['changed'])
        self.assertTrue(data['movie'])
        self.assertEqual(changed_movie.name, changes_to_be_made['name'])
        self.assertTrue(changed_movie.releasedate.strftime("%Y-%m-%d %H:%M:%S"), changes_to_be_made['releasedate'])

    def test_404_change_movie(self):
        changes_to_be_made={
            'name': 'Changed_Name',
            'releasedate': '2000-01-01 00:00:00'
        }
        movie_id_to_change = Movies.query.order_by(Movies.id.desc()).first().id + 1
        res = self.client().patch('/movies/{}'.format(movie_id_to_change), json = changes_to_be_made)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()