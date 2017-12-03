from flask import Flask
app = Flask(__name__)

app.route('/')
def indef():
  return 'Hello world'
