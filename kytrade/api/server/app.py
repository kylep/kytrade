"""Kytrade API server entrypoint"""
from flask import Flask, jsonify

app = Flask("kytrade")

@app.route("/")
def index():
    return jsonify({"status": "OK"}), 200

