from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime
from flask_migrate import Migrate


database_name = "capstone"
database_path = "postgresql://postgres:temppass@localhost:5432/capstone"

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    
    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.String)
    gender = db.Column(db.String)

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }