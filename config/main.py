import os
import sys
from flask import Flask, request, jsonify
from auth_gateway.config import Config
from auth_gateway.database import Database

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_mapping(test_config or {})

    @app.route('/login', methods=['POST'])
    def login():
        user_data = request.json
        db = Database()
        user = db.get_user(user_data['username'], user_data['password'])
        if user:
            return jsonify({'token': user['token']})
        return jsonify({'error': 'Invalid credentials'}), 401

    @app.route('/register', methods=['POST'])
    def register():
        user_data = request.json
        db = Database()
        user = db.create_user(user_data['username'], user_data['password'])
        if user:
            return jsonify({'token': user['token']})
        return jsonify({'error': 'User already exists'}), 409

    return app

if __name__ == '__main__':
    app = create_app()
    if len(sys.argv) > 1:
        app.run(host='0.0.0.0', port=int(sys.argv[1]))
    else:
        app.run(host='0.0.0.0', port=5000)