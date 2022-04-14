"""Kytrade API server entrypoint"""
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from kytrade.data.db import CONN_STRING


app = Flask("kytrade")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = CONN_STRING
db = SQLAlchemy(app)

@app.route("/")
def index():
    return jsonify({"status": "OK"}), 200

