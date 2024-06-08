#!/usr/bin/python3
"""
API for HBnB Evolution
"""

from flask import Flask, jsonify
from models.base_model import BaseModel

app = Flask(__name__)


@app.route('/api/v1/status', methods=['GET'])
def status():
    """
    Return the status of the API
    """
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
