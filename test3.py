from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mars_db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def get_all_start():
    my_coll = mongo.db.mars_coll
    output = []
    for s in my_coll.find():
        output.append({
            "News Title": s['News Title'],
            "News Description": s['News Description'],
            "Featured Space Image": s['Featured Space Image'],
            "Mars Weather": s['Mars Weather'],
            "Mars Facts": s['Mars Facts'],
            "Hemispheres": s['Hemispheres']
        })
    return jsonify({'result' : output})

app.run(debug=True, port=5545)