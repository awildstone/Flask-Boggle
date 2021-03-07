from flask import Flask, session, request, render_template, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

BOARD_KEY = 'game_board'
BOGGLE_GAME = Boggle()
HIGH_SCORE_KEY = 'score'
NUM_GAMES_KEY = 'num_games'

@app.route('/')
def make_board():
    ''' Make the gameboard and display it on the page. '''
    #make the game board
    game_board = BOGGLE_GAME.make_board()

    #get high score
    high_score = session.get(HIGH_SCORE_KEY, 0)

    #get num games played
    num_games = session.get(NUM_GAMES_KEY, 0)

    #save the game board in this session
    session[BOARD_KEY] = game_board

    return render_template('index.html', game_board=game_board, high_score=high_score, num_games=num_games)

@app.route('/check-guess')
def check_guess():
    ''' check the guess from the client against the current game board. '''

    #get guess
    guess = request.args['guess'];

    # get the board instance from session
    board = session[BOARD_KEY]

    # check if the word is valid and is on the board
    answer = BOGGLE_GAME.check_valid_word(board, guess)

    return jsonify(result=answer)

@app.route('/stats', methods=['POST'])
def update_stats():
    ''' checks new game score to determine if new high score and updates the number of games played.
    Returns the current high score to the client. '''

    # get the score & current high score
    stats = request.json
    curr_score = stats['params']['score']
    highscore = session.get(HIGH_SCORE_KEY, 0)

    # check for new high score
    if curr_score > highscore:
        session[HIGH_SCORE_KEY] = curr_score

    #get current game number and increment
    num_games = session.get(NUM_GAMES_KEY, 0)
    session[NUM_GAMES_KEY] = num_games + 1

    return jsonify({'score': session.get(HIGH_SCORE_KEY)})




        


    
