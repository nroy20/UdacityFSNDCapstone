from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:temppass@localhost:5432/capstone'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.String)
    gender = db.Column(db.String)

'''
@app.route('/movies/create', methods=['POST'])
def create_movie():
    error = False
    body = {}
    try:
        title = request.get_json()['title']
        movie = Movie(title=title)
        db.session.add(movie)
        db.session.commit()
        body['title'] = movie.title
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        return jsonify(body) 
    else:
        abort(500)
'''
def shorten_actor(self):
    return {
        "name": self.name
    }

def shorten_movie(self):
    return {
        "title": self.title
    }
@app.route('/actors', methods=['GET'])
def list_actors():
    actors = Actor.query.all()

    if len(actors) == 0:
        abort(404)

    short_list = [actor.shorten_actor() for actor in actors]

    return jsonify({
        "success": True,
        "actors": short_list
    })


@app.route('/')
def index():
    return render_template('home_page.html')
    #return render_template('index.html', data=Movie.query.all())

