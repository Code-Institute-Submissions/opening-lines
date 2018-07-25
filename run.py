import os
import json
import random
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    number_of_players=0
    if request.method == "POST":
        session['number_of_players'] = int(request.form["number_of_players"])
        return redirect(url_for('players'))
    return render_template("index.html", number_of_players=number_of_players)
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)