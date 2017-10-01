from flask import Flask
from flask_pymongo import PyMongo

app = Flask('FoodBot')
app.config.from_object('config')
app.config.from_envvar('FLASK_TEST_SETTINGS', silent=True)
mongo = PyMongo(app)

from FoodBot import views