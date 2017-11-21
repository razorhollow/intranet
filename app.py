#!python3
#app.py -- Reynolds Manufacturing Intranet, powered by python/flask

from flask import Flask
app = Flask(__name__)

@app.route('/')

def index():
    return '<h1>Hello World!</h1><p>Future home of RMI Intranet</p>'

if __name__ == '__main__':
    app.run(debug=True, port=int("4000"))
