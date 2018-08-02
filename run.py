import os
import json
import random
from flask import Flask, render_template, request, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key="some_secret"

# ----Creates list of players' names-----         
def write_players_to_list(form, number_of_players):
    list_of_players = []
    for player in range(1, number_of_players+1):
        list_of_players.append(form["Player " + str(player)])
    return list_of_players

# ----Determines who the current player is----       
def get_current_player(list_of_players, turn):
    if turn < len(list_of_players):
        player_number = turn
    else:
        player_number = turn % len(list_of_players)
    current_player = list_of_players[player_number]
    return current_player

# -----generates random sequence the same length as the data-----

def get_random_sequence(data):
    length = len(data)
    random_sequence = []
    for number in range (0, length):
        random_sequence.append(number)
    random.shuffle(random_sequence)  
    return random_sequence
    
# -----generates question based on random sequence-----
def get_question(data, turn, random_sequence):
    question = data[random_sequence[turn]]
    return question

# ----- compare submitted answer against name of book ------
def check_answer(answer, question):
    if answer.lower() == question["book"].lower():
        return True
    else:
        return False
        
#write "no guesses" to text file so it's known 
#there has been no previous guesses

def write_no_guesses():
    with open("data/guesses.txt", "w") as file:
                    file.write("No guesses")

# -----write zero scores to text file-----
def write_initial_scores(number_of_players):
    with open ("data/scores.txt","w") as file:
        for player in range(0, number_of_players):
            file.write("0" '\n')

# ----increases score of current player by 1----   
def amend_scores (list_of_players, list_of_scores, current_player):
    position_in_list = list_of_players.index(current_player)
    score = int(list_of_scores[position_in_list]) +1
    list_of_scores[position_in_list] = str(score)
    return list_of_scores

# ----writes scores to file----       
def write_scores_to_file (list_of_scores):
    with open ("data/scores.txt","w") as file:
        for score in list_of_scores:
            file.write(score + '\n')

# gets highest ever score from text file and amends if a current score is higher            
def get_highest_ever_score(list_of_players_and_scores):
    with open ("data/highest-score.txt","r") as file:
        highest_ever_score = file.read().splitlines()
    for player in range (0, len(list_of_players_and_scores)):
        if int(list_of_players_and_scores[player][1]) >= int(highest_ever_score[1]):
            highest_ever_score = [list_of_players_and_scores[player][0],list_of_players_and_scores[player][1]]
            with open ("data/highest-score.txt","w") as file:
                for item in highest_ever_score:
                    file.write(item + '\n')
    return highest_ever_score
  
# ---- index page - finds number of players ----
@app.route('/', methods=["GET", "POST"])
def index():
    number_of_players=0
    
    # Makes sure file doesn't contain data from previous game
    write_no_guesses()
                    
    if request.method == "POST":
        session['number_of_players'] = int(request.form["number_of_players"])
        return redirect(url_for('players'))
    return render_template("index.html")

# -----page where players names are entered ------
@app.route('/players', methods=["GET", "POST"])
def players():
    with open("data/data.json", "r") as json_data:
        data = json.load(json_data)
    session['random_sequence'] = get_random_sequence(data)
    turn = 0
    write_initial_scores(session['number_of_players'])
    if request.method == "POST":
        session["list_of_players"] = write_players_to_list(request.form, session['number_of_players'])
        return redirect(turn)
    return render_template("players.html", number_of_players=session['number_of_players'])  

# -----question page - also serves as final page------
@app.route('/<turn>', methods=["GET", "POST"])
def total (turn):
    with open("data/data.json", "r") as json_data:
        data = json.load(json_data)
    with open("data/scores.txt", "r") as file:
       list_of_scores = file.read().splitlines()
    
    # -----variables------
    turn=int(turn)
    random_sequence = session ["random_sequence"]
    question = get_question(data, turn, random_sequence)
    list_of_players = session["list_of_players"]
    list_of_players_and_scores = zip(list_of_players, list_of_scores)
    number_of_turns = len(list_of_players)*10
    current_player = get_current_player(list_of_players, turn)
    highest_ever_score = get_highest_ever_score(list_of_players_and_scores)
    
    # -----response to submitted question -check answer, amend score if necessary and redirect------
    if request.method == "POST":
        correct_or_not = check_answer(request.form["answer"], question)
        # if answer correct, goes to next page
        if correct_or_not is True:
            list_of_scores = amend_scores(list_of_players, list_of_scores, current_player)
            write_scores_to_file(list_of_scores)
            write_no_guesses()
            turn = turn+1
            return redirect(turn)
        
        # if answer not correct gives another guess. Number of guesses read/written to file
        else:
            with open("data/guesses.txt", "r") as file:
                guesses = file.read()
            if guesses == "One guess":
                write_no_guesses()
                turn = turn+1
                return redirect(turn)
            else: 
                flash('That\'s incorrect. Have one more try.')
                with open("data/guesses.txt", "w") as file:
                    file.write("One guess")
                    
    # ----variables written to page-----                
    return render_template("question.html", turn=turn, data=data, current_player=current_player, list_of_players_and_scores=list_of_players_and_scores, question=question, random_sequence=random_sequence, highest_ever_score=highest_ever_score, number_of_turns=number_of_turns)
   
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)