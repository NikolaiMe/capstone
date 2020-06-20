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
Movies
Have title and release year
Can be formatted, created, deleted, changed
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
  
  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()


'''
Actors
Have name, age and gender
Can be formatted, created, deleted, changed
'''
class Actors(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key = True)
  name = Column(String, nullable = False)
  age = Column(Integer, nullable = False)
  gender = Column(String, nullable = False)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
      }
  
  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()