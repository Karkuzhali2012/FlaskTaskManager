from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task
from db import db

task_blueprint = Blueprint('tasks', __name__)

@task_blueprint.route('/', methods=['GET'])
def index():
    return render_template('task_manager.html')

@task_blueprint.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=current_user).all()
    tasks_data = [{'id': task.id, 'description': task.description} for task in tasks]
    return jsonify(tasks_data), 200

@task_blueprint.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    data = request.get_json()
    description = data.get('description')
    current_user = get_jwt_identity()
    new_task = Task(description=description, user_id=current_user)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

@task_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    new_description = data.get('description')
    current_user = get_jwt_identity()
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    if task.user_id != current_user:
        return jsonify({'message': 'Unauthorized'}), 403
    task.description = new_description
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200

@task_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    if task.user_id != current_user:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200
