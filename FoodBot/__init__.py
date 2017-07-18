from flask import Flask

app = Flask('FoodBot')
app.config.from_object('config')
app.config.from_envvar('FLASK_TEST_SETTINGS', silent=True)

from FoodBot import views