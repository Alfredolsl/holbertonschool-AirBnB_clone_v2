#!/usr/bin/python3
"""Starts a Flask web app."""
from flask import Flask

app = Flask(__name__)

# Define a route with variable
@app.route("/", strict_slashes=False)
def hello_world():
    """returns 'Hello HBNB!'"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
