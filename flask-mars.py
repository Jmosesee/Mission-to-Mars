from flask import Flask, render_template
from flask import jsonify
from flask import redirect, url_for
from flask_pymongo import PyMongo
from scrape_mars import scrape
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mars_db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'

mongo = PyMongo(app)

def setup_mongo():
    client = MongoClient('localhost', 27017)
    db = client.mars_db
    collection = db.mars_coll
    return collection

@app.route('/', methods=['GET'])
def home_route():
    # Pull data out of mongodb
    d = mongo.db.mars_coll.find_one()
    data = {
        "News Title": d['News Title'],
        "News Description": d['News Description'],
        "Featured Space Image": d['Featured Space Image'],
        "Mars Weather": d['Mars Weather'],
        "Mars Facts": d['Mars Facts'],
        "Hemispheres": d['Hemispheres']
    }
    return render_template("index.html", data=data)

@app.route('/scrape', methods=['GET'])
def scraper():
    # Scrape data and put it into mongodb
    collection = setup_mongo()
    collection.drop()
    collection.insert_one(scrape())
    return redirect('/')

app.run(debug=True, port=5545)

