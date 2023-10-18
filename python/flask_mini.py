# -*- coding: utf-8 -*

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(port=5050) # Permet de lancer le serveur directement depuis python en exécutant le programme
