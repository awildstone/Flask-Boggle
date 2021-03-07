/* Save constants for jquery use */
const $form = $('.guess_form');
const $message = $('.message');
const $score = $('.score');
const $start = $('#start_game');
const $newGame = $('#new_game');
const $timer = $('.game_timer');

/* Values for game */
let GAME_TIMER = 60;
let SCORE = 0;
const GUESSES = new Set();

/* function for handling form submissions of guesses */
async function handleFormSubmit(event) {
    //prevent default form submission
    event.preventDefault();

    //get the form value
    const $guess = $('#guess').val();

    if (GUESSES.has($guess)) {
        // notify user word already guessed, clear form and ignore guess
        displayResponse(`You already guessed ${$guess}!`, 'error');
        $('#guess').val('');
        return
    }

    //add guess to our guess tracker
    GUESSES.add($guess);

    const response = await checkGuess($guess);

    //clear form input value
    $('#guess').val('');

    checkResponse(response['result'], $guess);
}

$form.on('submit', handleFormSubmit);

/* function for sending guess to the server */
async function checkGuess(guess) {
    let response = await axios.get('/check-guess', { params: { guess: guess }});

    return response.data
}

/* function for displaying messages to the user in the DOM */
function displayResponse(msg, id) {
    $message.attr('id', id);
    $message.text(msg);
}

/* updates the current game score and displays the score on the page */
function updateDisplayScore(points) {
    SCORE += points;
    $score.text(`Score: ${SCORE}`);
}

/* checks the response message from the server and decides which message to display to the user per the response */
function checkResponse(response, word) {
    if (response == 'ok') {
        displayResponse(`${word} is on the board! You get ${word.length} points`, 'success');
        updateDisplayScore(word.length);

    } else if (response === 'not-on-board') {
        displayResponse(`${word} is not on the board!`, 'error');

    } else {
        displayResponse(`${word} is not a word!`, 'error');

    }
}

/* Clicking the start button starts the game. */
$start.on('click', function() {
    //hide start button
    $start.hide();
    //show play form
    $form.show();
    //show counter
    $timer.text('Game Timer: 60 Seconds');
    startTimer();
});

function startTimer() {
    //start game timer
    const countdown = setInterval(function(){
        if (GAME_TIMER == 0) {
            $timer.text('GAME OVER');
            $form.hide();
            updateUserStatistics();
            newGame();
            //stop countdown
            clearInterval(countdown);
        } else {
            $timer.text(`Game Timer: ${GAME_TIMER -= 1} Seconds`);
        }
    }, 1000);
}

/* displays new game button to reload the page and start a new game */
async function newGame() {
    $newGame.show();
    $newGame.on('click', function() {
        //reload the page to start new game
        location.reload();
    });
}

/* sends score for current game to the server to check if this score is the new high score */
async function updateUserStatistics() {
    const stats = await axios.post('/stats', { params: { score: SCORE }});

    if (SCORE == stats.data.score) {
        displayResponse(`${SCORE} is the new high score!`, 'success');
    }
}