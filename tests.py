import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie



casting_assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxYN1hWX2JYaUw1bGRCNGtCOU1FZiJ9.eyJpc3MiOiJodHRwczovL215LWNhc3RpbmctYWdlbmN5LWNhcHN0b25lLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjI4YTVhMTMxYmVkNTAwOTkwNDM5ZWMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk2NzUwNTc1LCJleHAiOjE1OTY3NTc3NzUsImF6cCI6InRCekVqcGVPNXc1WEM2UDJSdE8zQUdkVzVONHlkbE4xIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6aW5mb3JtYXRpb24iXX0.edsKlmEC1h7Zz9oQ22v34vigL7Reumm0jO7eeyDp2AIhcl7jrv0UMK8TqFDQCQGyRiLfgesDDaVXk4YrOAh6cMQvoQJMwu1bx_YIPlF7Qv9kPYw8oIdo4s8jOartz6OX_4cluJ4SISkw9XcyP9MpHQ4MDkFuJF135M-1VrGA2LA8klBWEzEY2nLKfV0-qfLG4Ql-Y1uqGhTv3mMlJ-rYEhvMtWHHp7LmuDslcEZPOtFyPrt-MUYRUjOrE654G-SuhKU684FjfErPITrl9x1J9iS36vqUzF07EK2GchOrh7-IJviNaww6mnjMdXsSMNzkyVpwDWQz3H5qXnXYgYvOeQ"
casting_director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxYN1hWX2JYaUw1bGRCNGtCOU1FZiJ9.eyJpc3MiOiJodHRwczovL215LWNhc3RpbmctYWdlbmN5LWNhcHN0b25lLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjI4YTY1MTVjODQ4ZjAwMzdjNDVjMTMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk2NzUwNjI1LCJleHAiOjE1OTY3NTc4MjUsImF6cCI6InRCekVqcGVPNXc1WEM2UDJSdE8zQUdkVzVONHlkbE4xIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6aW5mb3JtYXRpb24iLCJwYXRjaDppbmZvcm1hdGlvbiIsInBvc3Q6YWN0b3IiXX0.GZ4i8a8T4XDdZif7Sx1T5tipEnappeoH0C_9-fjaSi6-1cKMnYrhnRH4IL1YuAzQfV4HgZXkeRnuFZjucvPuBAbgmpkk-FBjTLF6iBP_2oODRMrFh2j3Cj3GTYn7whP0XkXVVYIuVJAhx6FuhpdulzIcFg-TBZaxpmDd6cpE7kzKO0CIW4QJEmzPYVARPNnccinli6O4IRBfxuL4i2CTmxjSzq2CxOXkjrE7Y-EbU5FHKw-J_XyL39xi7Ug4AkXTUN7Cs0V09GTBZQuxf7X-BIr3sTFZra6kA0SztrHxGIJpd9J0FLzhV9ThcMLek3_hi9lxeGA-__VwjdPXqaIv-w"
executive_producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxYN1hWX2JYaUw1bGRCNGtCOU1FZiJ9.eyJpc3MiOiJodHRwczovL215LWNhc3RpbmctYWdlbmN5LWNhcHN0b25lLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjI4YTZjMWRjNjgyNjAwYTBiNjcwYTIiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk2NzUwNjgxLCJleHAiOjE1OTY3NTc4ODEsImF6cCI6InRCekVqcGVPNXc1WEM2UDJSdE8zQUdkVzVONHlkbE4xIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6aW5mb3JtYXRpb24iLCJwYXRjaDppbmZvcm1hdGlvbiIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.ATcyfaDACFd1eBwnmu9SK1wZ1DjefNKZ3lz90aopYkra5rj6ks6xDYwqJa4nUO69_VLuip3N6LOJkorAb6Yevr32BDO75EsEGwJQE1iUcm8yImLxKYu3UCiZekUuTmfQVoGJ83cYiOD4d0EM9PZ4lxweYRLLb07zg9F8YmUhpIW-MRk8Q_Kz8rZFYuFBgbCzLdyEYPWCRoYukIWduXExOBJj5nuwu9VEHE4EC39a8CUM_cfu6al4bcj67BnNoGdJ9XqX-SEVS4W3CAFyB_RiGXXCd_2PaTJ4dtLumMOm9KcQJT2-9rYPYwPjLcXm8ohuvXqziPlmg4jv7jArarqgOQ"


def set_header(role_token):
    return {'Authorization': 'Bearer {}'.format(role_token)}

class CapstoneTestCase(unittest.TestCase):
    def addInitialData(self):
        actor = Actor(name="initial actor")
        movie = Movie(title="initial movie", release_date="1/1/2000")
        self.db.session.add(actor)
        self.db.session.add(movie)
        self.db.session.commit()
        self.db.session.close()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://postgres:temppass@localhost:5432/{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.addInitialData()

    def tearDown(self):
        pass
#______________________________________________________________________________________

    def test_actor_list(self):
        res = self.client().get('/actors', headers=set_header(casting_assistant_token))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['actors'])
        self.assertEqual(res.status_code, 200)

    def test_actor_list_failure_404(self):
        actors = Actor.query.all()
        for actor in actors:
            actor.delete()
        res = self.client().get('/actors', headers=set_header(casting_assistant_token))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(res.status_code, 404)

    def test_movie_list(self):
        res = self.client().get('/movies', headers=set_header(casting_assistant_token))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['movies'])
        self.assertEqual(res.status_code, 200)

    def test_movie_list_failure_404(self):
        movies = Movie.query.all()
        for movie in movies:
            movie.delete()
        res = self.client().get('/movies', headers=set_header(casting_assistant_token))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(res.status_code, 404)

    def test_get_actor(self):
        actor = Actor.query.filter(Actor.name == "test actor")
        actor_id = actor[0].id
        res = self.client().get('/actors/' + str(actor_id), headers=set_header(casting_assistant_token))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], actor_id)
        self.assertEqual(res.status_code, 200)

    def test_get_actor_failure_400(self):
        res = self.client().get('/actors/0', headers=set_header(casting_assistant_token))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(res.status_code, 400)

    def test_get_actor_failure_404(self):
        res = self.client().get('/actors/9999999999', headers=set_header(casting_assistant_token))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(res.status_code, 404)

    def test_get_movie(self):
        movie = Movie.query.filter(Movie.title == "test movie")
        movie_id = movie[0].id
        res = self.client().get('/movies/' + str(movie_id), headers=set_header(casting_assistant_token))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], movie_id)
        self.assertEqual(res.status_code, 200)

    def test_get_movie_failure_400(self):
        res = self.client().get('/movies/0', headers=set_header(casting_assistant_token))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(res.status_code, 400)

    def test_get_movie_failure_404(self):
        res = self.client().get('/movies/9999999999', headers=set_header(casting_assistant_token))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(res.status_code, 404)

    def test_add_actor(self):
        res = self.client().post('/actors/add', headers=set_header(casting_director_token), json={
            'name': "test actor"
        })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['name'], "test actor")
        self.assertEqual(res.status_code, 200)

    def test_add_actor_failure_422(self):
        res = self.client().post('/actors/add', headers=set_header(casting_director_token), json={
            'age': 123
        })
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "unprocessable")
        self.assertEqual(res.status_code, 422)

    def test_add_movie(self):
        res = self.client().post('/movies/add', headers=set_header(executive_producer_token), json={
            'title': "test movie",
            'release_date': "1/1/2000"
        })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['title'], "test movie")
        self.assertEqual(data['release_date'], "1/1/2000")
        self.assertEqual(res.status_code, 200)

    def test_add_movie_failure_422(self):
        res = self.client().post('/movies/add', headers=set_header(executive_producer_token), json={
            'title': "test movie",
        })
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "unprocessable")
        self.assertEqual(res.status_code, 422)

    def test_modify_actor(self):
        self.client().post('/actors/add', headers=set_header(casting_director_token), json={
            'name': "test actor modify"
        })
        actor = Actor.query.filter(Actor.name == "test actor modify")
        actor_id = actor[0].id
        res = self.client().patch('/actors/' + str(actor_id) + '/edit', headers=set_header(casting_director_token), json={
            'name': "actor modified"
        })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['name'], "actor modified")
        self.assertEqual(res.status_code, 200)

    def test_modify_actor_failure_400(self):
        res = self.client().patch('/actors/0/edit', headers=set_header(casting_director_token), json={
            'name': "actor modified"
        })
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(res.status_code, 400)

    def test_modify_actor_failure_404(self):
        res = self.client().patch('/actors/99999999/edit', headers=set_header(casting_director_token), json={
            'name': "actor modified"
        })
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(res.status_code, 404)

    def test_modify_actor_failure_422(self):
        self.client().post('/actors/add', headers=set_header(casting_director_token), json={
            'name': "test actor modify"
        })
        actor = Actor.query.filter(Actor.name == "test actor modify")
        actor_id = actor[0].id
        res = self.client().patch('/actors/' + str(actor_id) + '/edit', headers=set_header(casting_director_token), json={
            'age': "hello"
        })
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "unprocessable")
        self.assertEqual(res.status_code, 422)

    def test_modify_movie(self):
        self.client().post('/movies/add', headers=set_header(executive_producer_token), json={
            'title': "test movie modify",
            'release_date': "1/1/2000"
        })
        movie = Movie.query.filter(Movie.title == "test movie modify")
        movie_id = movie[0].id
        res = self.client().patch('/movies/' + str(movie_id) + '/edit', headers=set_header(casting_director_token), json={
            'title': "movie modified"
        })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['title'], "movie modified")
        self.assertEqual(res.status_code, 200)

    def test_modify_movie_failure_400(self):
        res = self.client().patch('/movies/0/edit', headers=set_header(casting_director_token), json={
            'title': "movie modified"
        })
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(res.status_code, 400)

    def test_modify_movie_failure_404(self):
        res = self.client().patch('/movies/999999999/edit', headers=set_header(casting_director_token), json={
            'title': "test movie modify",
            'release_date': "1/1/2000"
        })
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(res.status_code, 404)

    def test_modify_movie_failure_422(self):
        self.client().post('/movies/add', headers=set_header(executive_producer_token), json={
            'title': "test movie modify",
            'release_date': "1/1/2000"
        })
        movie = Movie.query.filter(Movie.title == "test movie modify")
        movie_id = movie[0].id
        res = self.client().patch('/movies/' + str(movie_id) + '/edit', headers=set_header(casting_director_token), json={
            'release_date': "hello"
        })
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "unprocessable")
        self.assertEqual(res.status_code, 422)

    def test_delete_actor(self):
        self.client().post('/actors/add', headers=set_header(casting_director_token), json={
            'name': "test actor delete"
        })
        actor = Actor.query.filter(Actor.name == "test actor delete")
        actor_id = actor[0].id
        res = self.client().delete('/actors/' + str(actor_id), headers=set_header(casting_director_token))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], actor_id)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_failure_400(self):
        res = self.client().delete('/actors/0', headers=set_header(casting_director_token))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(res.status_code, 400)

    def test_delete_actor_failure_404(self):
        res = self.client().delete('/actors/99999999', headers=set_header(casting_director_token))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(res.status_code, 404)

    def test_delete_movie(self):
        self.client().post('/movies/add', headers=set_header(executive_producer_token), json={
            'title': "test movie delete",
            'release_date': '1/1/2000'
        })
        movie = Movie.query.filter(Movie.title == "test movie delete")
        movie_id = movie[0].id
        res = self.client().delete('/movies/' + str(movie_id), headers=set_header(executive_producer_token))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], movie_id)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_failure_400(self):
        res = self.client().delete('/movies/0', headers=set_header(executive_producer_token))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(res.status_code, 400)

    def test_delete_movie_failure_404(self):
        res = self.client().delete('/movies/9999999', headers=set_header(executive_producer_token))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(res.status_code, 404)

    def test_role_failure_assistant(self):
        res = self.client().post('/actors/add', headers=set_header(casting_assistant_token), json={
            'name': "test actor"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_role_failure_director(self):
        res = self.client().post('/movies/add', headers=set_header(casting_director_token), json={
            'title': "test movie",
            'release_date': "1/1/2001"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

if __name__ == "__main__":
    unittest.main()