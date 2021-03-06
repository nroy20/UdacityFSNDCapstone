from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime
from flask_migrate import Migrate


database_path = "postgres://yrpssbmdhpbpcf:3e72289a2991b9c8a380f9d67c92611c59884f7e18dbfaede4554a67fb8aa6a3@ec2-34-195-115-225.compute-1.amazonaws.com:5432/d6flpqcu2sgugl"

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()
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

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()