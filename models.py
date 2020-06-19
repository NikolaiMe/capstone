import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()


'''
Person
Have title and release year
'''
class Movies(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  releasedate = Column(db.DateTime(), nullable = False )

  def __init__(self, name, releasedate):
    self.name = name
    self.releasedate = releasedate

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'releasedate': self.releasedate
      }

class Actors(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable = False)
  age = Column(db.Integer, nullable = False)
  gender = Column(String, nullable=False)

  def __init__(self, name, releasedate):
    self.name = name
    self.releasedate = releasedate

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
      }