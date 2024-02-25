from flask import Blueprint, jsonify, request, render_template
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_manager, create_access_token
from models import User
from db import db  # Import db directly from db.py

auth_blueprint = Blueprint('auth', __name__)

bcrypt = Bcrypt()

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    return render_template('register.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    return render_template('login.html')