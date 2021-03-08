from unittest import TestCase
from app import app
from flask import session, request, jsonify
from boggle import Boggle


class FlaskTests(TestCase):
    
    def setUp(self):
        ''' show real errors for tests '''
        app.config['TESTING'] = True
        
    def test_make_board(self):
        with app.test_client() as client:
            res = client.get("/")

            #check that status is 200
            self.assertEqual(res.status_code, 200);

            #check that new session was created with board
            self.assertIn('game_board', session);

            #check that game board was placed in DOM
            html = res.get_data(as_text=True)
            self.assertIn('High Score is 0', html);
            self.assertIn('in 0 plays', html);

    def test_check_guess(self):
        with app.test_client() as client:
            #make new board
            res = client.get('/')

            #check that status is 200
            self.assertEqual(res.status_code, 200);

            #check that response status is 200 and a valid word that is too long gets 'not-on-board' response
            res = client.get('/check-guess?guess=acmesthesia')
            self.assertEqual(res.status_code, 200);
            self.assertEqual(res.json['result'], 'not-on-board')

            #check that response status is 200 and a fake word gets 'not-word' response
            res = client.get('/check-guess?guess=djuedjeumdwo')
            self.assertEqual(res.status_code, 200);
            self.assertEqual(res.json['result'], 'not-word')
    
    def test_update_stats(self):
        with app.test_client() as client:
            #make new board
            res = client.get('/')
            
            res = client.post('/stats', json=({ 'params': { 'score': 5 }}))
            json_res = res.get_data(as_text=True)

            #check that status is 200 for post request
            self.assertEqual(res.status_code, 200)

            #check that response contains score
            self.assertIn(('"score": 5'), json_res)