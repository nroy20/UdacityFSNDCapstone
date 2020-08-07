from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, session, make_response
from flask_cors import CORS
from auth import AuthError, requires_auth
from functools import wraps
from models import Actor, Movie, setup_db
import json
import os
import requests

token_var = ""

def create_app(test_config=None):
    app = Flask(__name__, static_folder="templates/stylesheets")
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route('/actors/list', methods=['GET'])
    def actor_list():
        return render_template('actor_list.html', token=token_var)
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:information')
    def list_actors(payload):
        actors = Actor.query.order_by('id').all()

        if len(actors) == 0:
            abort(404)

        formatted_actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': formatted_actors
        }), 200

        #return render_template('actor_list.html', actors=formatted_actors)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:information')
    def list_movies(payload):
        movies = Movie.query.order_by('id').all()

        if len(movies) == 0:
            abort(404)

        formatted_movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formatted_movies
        }), 200
        #return render_template('movie_list.html', movies=formatted_movies)

    @app.route('/actors/<int:actor_id>', methods=["GET"])
    @requires_auth('get:information')
    def get_actor_profile(payload, actor_id):
        if actor_id == 0:
            abort(400)

        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        formatted_actor = actor.format()

        return jsonify ({
            'success': True,
            'id': actor_id
        }), 200

        #return render_template('actor_profile.html', actor=formatted_actor)

    @app.route('/movies/<int:movie_id>', methods=["GET"])
    @requires_auth('get:information')
    def get_movie_description(payload, movie_id,):
        if movie_id == 0:
            abort(400)

        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        formatted_movie = movie.format()

        return jsonify({
            'success': True,
            'id': movie_id
        })

        #return render_template('movie_description.html', movie=formatted_movie)

    @app.route('/actors/add', methods=["GET"])
    @requires_auth('post:actor')
    def create_actor_form(payload):
        return render_template('add_actor.html')

    @app.route('/actors/add', methods=["POST"])
    @requires_auth('post:actor')
    def add_actor(payload):
        
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

            if not actor:
                abort(404)

            actor.insert()

            return jsonify({
                "success": True,
                "name": body.get('name'),
                "age": body.get('age'),
                "gender": body.get('gender')
            }), 200
        except:
            abort(422)

    @app.route('/movies/add', methods=["GET"])
    @requires_auth('post:movie')
    def create_movie_form(payload):
        return render_template('add_movie.html')

    @app.route('/movies/add', methods=["POST"])
    @requires_auth('post:movie')
    def add_movie(payload):

        body = request.get_json()
        try:
            title = body.get('title')
            release_date = body.get('release_date')
            movie = Movie(
                title = title,
                release_date = release_date
            )

            if not movie:
                abort(404)

            movie.insert()

            return jsonify({
                "success": True,
                "title": body.get('title'),
                "release_date": body.get('release_date')
            }), 200

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=["DELETE"])
    @requires_auth('delete:actor')
    def remove_actor(payload, actor_id):
        if actor_id == 0:
                abort(400)

        actor = Actor.query.get(actor_id)

        if not actor:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'id': actor_id
        }), 200

    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    @requires_auth('delete:movie')
    def remove_movie(payload, movie_id):
        if movie_id == 0:
            abort(400)

        movie = Movie.query.get(movie_id)

        if not movie:
            abort(404)
                
        movie.delete()

        return jsonify({
            'success': True,
            'id': movie_id
        }), 200

    @app.route('/actors/<int:actor_id>/edit', methods=["GET"])
    @requires_auth('patch:information')
    def modify_actor_form(payload, actor_id):
        return render_template('update_actor.html', actor_id=actor_id)
    @app.route('/actors/<int:actor_id>/edit', methods=["PATCH"])
    @requires_auth('patch:information')
    def modify_actor(payload, actor_id):
        if (actor_id) == 0:
            abort(400)

        actor = Actor.query.get(actor_id)

        if not actor:
            abort(404)

        body = request.get_json()

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

            actor.update()

            return jsonify({
                "success": True,
                "name": body.get('name'),
                "age": body.get('age'),
                "gender": body.get('gender')
            }), 200
        except:
            abort(422)
        
    @app.route('/movies/<int:movie_id>/edit', methods=["GET"])
    @requires_auth('patch:information')
    def modify_movie_form(payload, movie_id):
        return render_template('update_movie.html', movie_id=movie_id)
    @app.route('/movies/<int:movie_id>/edit', methods=["PATCH"])
    @requires_auth('patch:information')
    def modify_movie(payload, movie_id):
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

            movie.update()

            return jsonify({
                "success": True,
                "title": body.get('title'),
                "release_date": body.get('release_date'),
            }), 200

        except:
            abort(422)
    
    @app.route('/login-results', methods=['GET'])
    def login_page():
        return render_template('home_page.html'), 200
    @app.route('/login-results', methods=['POST'])
    def get_token():
        body = request.get_json()
        hash = body.get('hash')
        
        if not hash:
            abort(404)

        token_end_index = len(hash) - 34
        token = hash[13:token_end_index]

        if not token:
            abort(404)

        token_var = token

        if token_var == "":
            abort(400)
            
        return jsonify({
            "success": True,
            "hash": hash,
            "token": token
        })

    @app.route('/')
    def index():
        return render_template('home_page.html'), 200

#Error Handlers----------------------------------------------------

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

    @app.errorhandler(AuthError)
    def error_auth(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()
app.secret_key = os.getenv('SECRET_KEY')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)