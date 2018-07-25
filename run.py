import os
import json
import random
from flask import Flask, render_template, request, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key="some_secret"

# compare submitted answer against name of book
def check_answer(answer, data, turn):
    if answer.lower() == data[turn]["book"].lower():
        return True
    else:
        return False

def write_initial_scores(number_of_players):
    with open ("data/scores.txt","w") as file:
        for player in range(0, number_of_players):
            file.write("0" '\n')
            
def write_players_to_list(form, number_of_players):
    list_of_players = []
    for player in range(1, number_of_players+1):
        list_of_players.append(form["Player " + str(player)])
    return list_of_players
    
def get_current_player(list_of_players, turn):
    if turn < len(list_of_players):
        player_number = turn
    else:
        player_number = turn % len(list_of_players)
    current_player = list_of_players[player_number]
    return current_player
    
  
# index page - finds number of players
@app.route('/', methods=["GET", "POST"])
def index():
    number_of_players=0
    if request.method == "POST":
        session['number_of_players'] = int(request.form["number_of_players"])
        return redirect(url_for('players'))
    return render_template("index.html")

# page where players names are entered
@app.route('/players', methods=["GET", "POST"])
def players():
    turn = 0
    write_initial_scores(session['number_of_players'])
    if request.method == "POST":
        session["list_of_players"] = write_players_to_list(request.form, session['number_of_players'])
        return redirect(turn)
    return render_template("players.html", number_of_players=session['number_of_players'])  

@app.route('/<turn>', methods=["GET", "POST"])
def total (turn):
    list_of_players = session["list_of_players"]
    with open("data/data.json", "r") as json_data:
        data = json.load(json_data)
    turn=int(turn)
    number_of_turns = len(list_of_players)*10
    current_player=get_current_player(list_of_players, turn)
    if request.method == "POST":
        correct_or_not = check_answer(request.form["answer"], data, turn)
        
        # if answer correct, goes to next page
        if correct_or_not is True:
            turn = turn+1
            return redirect(turn)
        
        # if answer not correct gives anaother guess. Number of guesses read/written to file
        else:
            with open("data/guesses.txt", "r") as file:
                guesses = file.read()
            if guesses == "Two guesses":
                open("data/guesses.txt", 'w').close()
                turn = turn+1
                return redirect(turn)
            else: 
                flash('That\'s incorrect. Have one more try.')
                with open("data/guesses.txt", "w") as file:
                    file.write("Two guesses")
    return render_template("question.html", turn=turn, data=data, current_player=current_player)
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)