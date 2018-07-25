import os
import json
import random
from flask import Flask, render_template, request, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key="some_secret"

def check_answer(answer, data, turn):
    if answer.lower() == data[turn]["book"].lower():
        return True
    else:
        return False

@app.route('/', methods=["GET", "POST"])
def index():
    number_of_players=0
    if request.method == "POST":
        session['number_of_players'] = int(request.form["number_of_players"])
        return redirect(url_for('players'))
    return render_template("index.html")
    
@app.route('/players', methods=["GET", "POST"])
def players():
    if request.method == "POST":
        number_of_players = session['number_of_players']
        number_of_turns = number_of_players*10
        turn = 0
        if request.method == "POST":
            return redirect(turn)
    return render_template("players.html", number_of_players=session['number_of_players'])  

@app.route('/<turn>', methods=["GET", "POST"])
def total (turn):
    with open("data/data.json", "r") as json_data:
        data = json.load(json_data)
    turn=int(turn)
    if request.method == "POST":
        correct_or_not = check_answer(request.form["answer"], data, turn)
        if correct_or_not is True:
            turn = turn+1
            return redirect(turn)
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
    return render_template("question.html", turn=turn, data=data)
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)