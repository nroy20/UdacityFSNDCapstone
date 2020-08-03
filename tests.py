import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie



casting_assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxYN1hWX2JYaUw1bGRCNGtCOU1FZiJ9.eyJpc3MiOiJodHRwczovL215LWNhc3RpbmctYWdlbmN5LWNhcHN0b25lLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjFlMTBlZWU2YTI5MTAwMzcyNzc0ZWMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk2NDkwMTU0LCJleHAiOjE1OTY0OTczNTQsImF6cCI6Im5GNjF5YnZjaGhqQjBDZkZXV0pxUEtWaVlkNkRMSjFOIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6aW5mb3JtYXRpb24iLCJwYXRjaDppbmZvcm1hdGlvbiIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.iW-xyFFQKluBKq2ajCmeQCWA2U-piH0Ff-Js7MO6Z4Bi2dBOx_3r12zT3GnU6DZoiXs16SnumSTaO_G_9IUEhanId_Ot8N17RuRMcyOfd28_NiVn-o9pFShNkDDRwkx5aSXM7deLw35TviIR624BdM-_aCtb0owgpEUOPQYNRNLrcX4l-PZPto7b6rTWhheq8LfAiAWV0crhmX_ncNiAWB-E3EEUBkUXrbSXt0ljSa1h_qAO402894PC2zEkD81xHBzhtuG9V7ym6fRGcjZbXwzrMAT86kQf0wAOAgvnNgaS0YPPp0m7dBqvAAlqZJIVXod9oltXkWsccBEfbNqsIA"
casting_director_token = "eeyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxYN1hWX2JYaUw1bGRCNGtCOU1FZiJ9.eyJpc3MiOiJodHRwczovL215LWNhc3RpbmctYWdlbmN5LWNhcHN0b25lLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjFlMTBlZWU2YTI5MTAwMzcyNzc0ZWMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk2NDkwMTU0LCJleHAiOjE1OTY0OTczNTQsImF6cCI6Im5GNjF5YnZjaGhqQjBDZkZXV0pxUEtWaVlkNkRMSjFOIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6aW5mb3JtYXRpb24iLCJwYXRjaDppbmZvcm1hdGlvbiIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.iW-xyFFQKluBKq2ajCmeQCWA2U-piH0Ff-Js7MO6Z4Bi2dBOx_3r12zT3GnU6DZoiXs16SnumSTaO_G_9IUEhanId_Ot8N17RuRMcyOfd28_NiVn-o9pFShNkDDRwkx5aSXM7deLw35TviIR624BdM-_aCtb0owgpEUOPQYNRNLrcX4l-PZPto7b6rTWhheq8LfAiAWV0crhmX_ncNiAWB-E3EEUBkUXrbSXt0ljSa1h_qAO402894PC2zEkD81xHBzhtuG9V7ym6fRGcjZbXwzrMAT86kQf0wAOAgvnNgaS0YPPp0m7dBqvAAlqZJIVXod9oltXkWsccBEfbNqsIA"
executive_producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxYN1hWX2JYaUw1bGRCNGtCOU1FZiJ9.eyJpc3MiOiJodHRwczovL215LWNhc3RpbmctYWdlbmN5LWNhcHN0b25lLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjFlMTBlZWU2YTI5MTAwMzcyNzc0ZWMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk2NDkwMTU0LCJleHAiOjE1OTY0OTczNTQsImF6cCI6Im5GNjF5YnZjaGhqQjBDZkZXV0pxUEtWaVlkNkRMSjFOIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6aW5mb3JtYXRpb24iLCJwYXRjaDppbmZvcm1hdGlvbiIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.iW-xyFFQKluBKq2ajCmeQCWA2U-piH0Ff-Js7MO6Z4Bi2dBOx_3r12zT3GnU6DZoiXs16SnumSTaO_G_9IUEhanId_Ot8N17RuRMcyOfd28_NiVn-o9pFShNkDDRwkx5aSXM7deLw35TviIR624BdM-_aCtb0owgpEUOPQYNRNLrcX4l-PZPto7b6rTWhheq8LfAiAWV0crhmX_ncNiAWB-E3EEUBkUXrbSXt0ljSa1h_qAO402894PC2zEkD81xHBzhtuG9V7ym6fRGcjZbXwzrMAT86kQf0wAOAgvnNgaS0YPPp0m7dBqvAAlqZJIVXod9oltXkWsccBEfbNqsIA"


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
        self.assertEqual(res.status_code, 200)

    def test_movie_list(self):
        res = self.client().get('/movies', headers=set_header(casting_assistant_token))
        self.assertEqual(res.status_code, 200)

    def test_get_actor(self):
        actor = Actor.query.filter(Actor.name == "test actor")
        actor_id = actor[0].id
        res = self.client().get('/actors/' + str(actor_id), headers=set_header(casting_assistant_token))
        self.assertEqual(res.status_code, 200)

    def test_get_movie(self):
        movie = Movie.query.filter(Movie.title == "test movie")
        movie_id = movie[0].id
        res = self.client().get('/movies/' + str(movie_id), headers=set_header(casting_assistant_token))
        self.assertEqual(res.status_code, 200)

    
    def test_add_actor(self):
        res = self.client().post('/actors/add', headers=set_header(casting_assistant_token), json={
            'name': "test actor"
        })
        self.assertEqual(res.status_code, 200)

    def test_add_movie(self):
        res = self.client().post('/movies/add', headers=set_header(casting_assistant_token), json={
            'title': "test movie",
            'release_date': "1/1/2000"
        })
        self.assertEqual(res.status_code, 200)

    def test_modify_actor(self):
        self.client().post('/actors/add', headers=set_header(casting_assistant_token), json={
            'name': "test actor modify"
        })
        actor = Actor.query.filter(Actor.name == "test actor modify")
        actor_id = actor[0].id
        res = self.client().patch('/actors/' + str(actor_id) + '/edit', headers=set_header(casting_assistant_token), json={
            'name': "actor modified"
        })
        self.assertEqual(res.status_code, 200)

    def test_modify_movie(self):
        self.client().post('/movies/add', headers=set_header(casting_assistant_token), json={
            'title': "test movie modify",
            'release_date': "1/1/2000"
        })
        movie = Movie.query.filter(Movie.title == "test movie modify")
        movie_id = movie[0].id
        res = self.client().patch('/movies/' + str(movie_id) + '/edit', headers=set_header(casting_assistant_token), json={
            'title': "movie modified"
        })
        self.assertEqual(res.status_code, 200)

    def test_delete_actor(self):
        self.client().post('/actors/add', headers=set_header(casting_assistant_token), json={
            'name': "test actor delete"
        })
        actor = Actor.query.filter(Actor.name == "test actor delete")
        actor_id = str(actor[0].id)
        res = self.client().delete('/actors/' + actor_id, headers=set_header(casting_assistant_token))
        self.assertEqual(res.status_code, 200)

    def test_delete_movie(self):
        self.client().post('/movies/add', headers=set_header(casting_assistant_token), json={
            'title': "test movie delete",
            'release_date': '1/1/2000'
        })
        movie = Movie.query.filter(Movie.title == "test movie delete")
        movie_id = str(movie[0].id)
        res = self.client().delete('/movies/' + movie_id, headers=set_header(casting_assistant_token))
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()