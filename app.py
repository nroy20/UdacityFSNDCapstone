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
    release_date = db.Column(db.DateTime)
    
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



@app.route('/actors', methods=['GET'])
def list_actors():
    '''
    actor = Actor(name="nayo", age="19", gender="female")
    db.session.add(actor)
    db.session.commit()
    return render_template('home_page.html')
    '''
    actors = Actor.query.all()

    if len(actors) == 0:
        abort(404)

    formatted_actors = [actor.format() for actor in actors]

    return render_template('actor_list.html', actors=formatted_actors)

@app.route('/movies', methods=['GET'])
def list_movies():
    '''
    movie = Movie(title="movie1")
    db.session.add(movie)
    db.session.commit()
    return render_template('home_page.html')
    '''
    movies = Movie.query.all()

    if len(movies) == 0:
        abort(404)

    formatted_movies = [movie.format() for movie in movies]

    return render_template('movie_list.html', movies=formatted_movies)

@app.route('/actors/<int:actor_id>', methods=["GET"])
def get_actor_profile(actor_id):
    if actor_id == 0:
        abort(400)

    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)

    formatted_actor = actor.format()

    return render_template('actor_profile.html', actor=formatted_actor)

@app.route('/movies/<int:movie_id>', methods=["GET"])
def get_movie_description(movie_id):
    if movie_id == 0:
        abort(400)

    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)

    formatted_movie = movie.format()

    return render_template('movie_description.html', movie=formatted_movie)

    
@app.route('/')
def index():
    return render_template('home_page.html')
    #return render_template('index.html', data=Movie.query.all())

