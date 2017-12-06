from flask import Flask
from pymongo import MongoClient

app = Flask('FoodBot')
app.config.from_object('config')
app.config.from_envvar('FLASK_TEST_SETTINGS', silent=True)
mongo = MongoClient().heroku_xrfxrbss

from FoodBot import views