from scrape_mars import scrape
import pymongo
from pymongo import MongoClient

def setup_mongo():
    client = MongoClient('localhost', 27017)
    db = client.mars_db
    collection = db.mars_coll
    return collection

collection = setup_mongo()
collection.insert_one(scrape())

