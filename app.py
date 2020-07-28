from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from auth import AuthError, requires_auth


app = Flask(__name__, static_folder="templates/stylesheets")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:temppass@localhost:5432/capstone'
db = SQLAlchemy(app)
#, static_folder="templates/stylesheets"
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

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/actors', methods=['GET'])
@requires_auth('get:information')
def list_actors(payload):
    actors = Actor.query.order_by('id').all()

    if len(actors) == 0:
        abort(404)

    formatted_actors = [actor.format() for actor in actors]

    return render_template('actor_list.html', actors=formatted_actors)

@app.route('/movies', methods=['GET'])
@requires_auth('get:information')
def list_movies(payload):
    movies = Movie.query.order_by('id').all()

    if len(movies) == 0:
        abort(404)

    formatted_movies = [movie.format() for movie in movies]

    return render_template('movie_list.html', movies=formatted_movies)

@app.route('/actors/<int:actor_id>', methods=["GET"])
@requires_auth('get:information')
def get_actor_profile(actor_id, payload):
    if actor_id == 0:
        abort(400)

    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)

    formatted_actor = actor.format()

    return render_template('actor_profile.html', actor=formatted_actor)

@app.route('/movies/<int:movie_id>', methods=["GET"])
@requires_auth('get:information')
def get_movie_description(movie_id, payload):
    if movie_id == 0:
        abort(400)

    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)

    formatted_movie = movie.format()

    return render_template('movie_description.html', movie=formatted_movie)

@app.route('/actors/add', methods=["GET"])
@requires_auth('post:actor')
def create_actor_form(payload):
    return render_template('add_actor.html')
@app.route('/actors/add', methods=["POST"])
@requires_auth('post:actor')
def add_actor(payload):
    error = False
    body = request.get_json()
    try:
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        actor = Actor(
            name = name,
            age = age,
            gender = gender
        )
        db.session.add(actor)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        return jsonify({
            "name": body.get('name'),
            "age": body.get('age'),
            "gender": body.get('gender')
        })
    else:
        abort(422)

@app.route('/movies/add', methods=["GET"])
@requires_auth('post:movie')
def create_movie_form(payload):
    return render_template('add_movie.html')
@app.route('/movies/add', methods=["POST"])
@requires_auth('post:movie')
def add_movie(payload):
    error = False
    body = request.get_json()
    try:
        title = body.get('title')
        release_date = body.get('release_date')
        movie = Movie(
            title = title,
            release_date = release_date
        )
        db.session.add(movie)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        return jsonify({
            "title": body.get('title'),
            "release_date": body.get('release_date')
        })
    else:
        abort(422)

@app.route('/actors/<int:actor_id>', methods=["DELETE"])
@requires_auth('delete:actor')
def remove_actor(actor_id, payload):
    if actor_id == 0:
      abort(400)

    actor = Actor.query.get(actor_id)

    if not actor:
        abort(404)

    error = False 
    try:
        db.session.delete(actor)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        return jsonify({
            'success': True
        })
    else:
        abort(422)

@app.route('/movies/<int:movie_id>', methods=["DELETE"])
@requires_auth('delete:movie')
def remove_movie(movie_id, payload):
    if movie_id == 0:
      abort(400)

    movie = Movie.query.get(movie_id)

    if not movie:
        abort(404)

    error = False
    try:
        db.session.delete(movie)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        return jsonify({
            'success': True
        })
    else:
        abort(422)

@app.route('/actors/<int:actor_id>/edit', methods=["GET"])
@requires_auth('patch:information')
def modify_actor_form(actor_id, payload):
    return render_template('update_actor.html', actor_id=actor_id)
@app.route('/actors/<int:actor_id>/edit', methods=["PATCH"])
@requires_auth('patch:information')
def modify_actor(actor_id, payload):
    if (actor_id) == 0:
        abort(400)

    actor = Actor.query.get(actor_id)

    if not actor:
        abort(404)

    body = request.get_json()

    error = False
    try:
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if name:
            actor.name = name 
        if age:
            actor.age = age
        if gender:
            actor.gender = gender
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        return jsonify({
            "name": body.get('name'),
            "age": body.get('age'),
            "gender": body.get('gender')
        })
    else:
        abort(422)
    
@app.route('/movies/<int:movie_id>/edit', methods=["GET"])
@requires_auth('patch:information')
def modify_movie_form(movie_id, payload):
    return render_template('update_movie.html', movie_id=movie_id)
@app.route('/movies/<int:movie_id>/edit', methods=["PATCH"])
@requires_auth('patch:information')
def modify_movie(movie_id, payload):
    if (movie_id) == 0:
        abort(400)

    movie = Movie.query.get(movie_id)

    if not movie:
        abort(404)

    body = request.get_json()

    error = False
    try:
        title = body.get('title')
        release_date = body.get('release_date')

        if title:
            movie.title = title 
        if release_date:
            movie.release_date = release_date
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        return jsonify({
            "title": body.get('title'),
            "release_date": body.get('release_date'),
        })
    else:
        abort(422)
@app.route('/')
def index():
    return render_template('home_page.html')


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def error_auth(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
