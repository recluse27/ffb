from flask import Flask
from pymongo import MongoClient
testing = False

app = Flask('FoodBot')
app.config.from_object('config')
app.config.from_envvar('FLASK_TEST_SETTINGS', silent=True)
mongo = (MongoClient(app.config['MONGO_URI']) if not testing
         else MongoClient(app.config["MONGO_TEST"]))

from FoodBot import views