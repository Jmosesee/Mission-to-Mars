from flask import Flask, render_template
from flask import jsonify
from flask import request

app = Flask(__name__)

data = {
    "first_name" : "Jeff",
    "last_name" : "James"
}

@app.route('/', methods=['GET'])
def homepage():
    return render_template("home.html", data=data)

app.run(debug=True, port=5545)