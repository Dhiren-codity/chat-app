from flask import Flask, request, jsonify
from models import db, User, Message, Room
from datetime import datetime
from status_manager import status_manager
from typing_indicator import typing_indicator
from group_manager import group_manager
from message_status import message_status_manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db.init_app(app)

@app.route('/api/users/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session_token = user.create_session()
        return jsonify({'token': session_token, 'user_id': user.id})

    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/messages', methods=['GET'])
def get_messages():
    room_id = request.args.get('room_id')

    messages = Message.query.filter_by(room_id=room_id).order_by(Message.created_at).all()

    return jsonify([{
        'id': m.id,
        'user_id': m.user_id,
        'content': m.content,
        'created_at': m.created_at.isoformat()
    } for m in messages])

@app.route('/api/status/update', methods=['POST'])
def update_status():
    user_id = request.json.get('user_id')
    is_online = request.json.get('is_online')

    status_manager.update_user_status(user_id, is_online)

    return jsonify({'success': True})

@app.route('/api/status/<int:user_id>', methods=['GET'])
def get_status(user_id):
    status = status_manager.get_user_status(user_id)
    return jsonify(status)

@app.route('/api/typing/start', methods=['POST'])
def start_typing():
    room_id = request.json.get('room_id')
    user_id = request.json.get('user_id')
    username = request.json.get('username')

    typing_indicator.user_started_typing(room_id, user_id, username)

    return jsonify({'success': True})

@app.route('/api/typing/stop', methods=['POST'])
def stop_typing():
    room_id = request.json.get('room_id')
    user_id = request.json.get('user_id')

    typing_indicator.user_stopped_typing(room_id, user_id)

    return jsonify({'success': True})

@app.route('/api/typing/<int:room_id>', methods=['GET'])
def get_typing_users(room_id):
    typers = typing_indicator.get_typing_users(room_id)
    return jsonify(typers)

@app.route('/api/groups/create', methods=['POST'])
def create_group():
    name = request.json.get('name')
    creator_id = request.json.get('creator_id')
    member_ids = request.json.get('member_ids', [])

    group = group_manager.create_group(name, creator_id, member_ids)

    return jsonify(group)

@app.route('/api/groups/<int:group_id>/rename', methods=['POST'])
def rename_group(group_id):
    new_name = request.json.get('new_name')
    user_id = request.json.get('user_id')

    result = group_manager.update_group_name(group_id, new_name, user_id)

    return jsonify(result)

@app.route('/api/groups/<int:group_id>/customize', methods=['POST'])
def customize_group_title(group_id):
    custom_title = request.json.get('custom_title')
    user_id = request.json.get('user_id')

    result = group_manager.customize_room_title(group_id, user_id, custom_title)

    return jsonify(result)

@app.route('/api/messages/<int:message_id>/delivered', methods=['POST'])
def mark_message_delivered(message_id):
    user_id = request.json.get('user_id')
    result = message_status_manager.mark_as_delivered(message_id, user_id)

    if result:
        return jsonify(result)
    return jsonify({'error': 'Failed to update status'}), 400

@app.route('/api/messages/<int:message_id>/read', methods=['POST'])
def mark_message_read(message_id):
    user_id = request.json.get('user_id')
    result = message_status_manager.mark_as_read(message_id, user_id)

    if result:
        return jsonify(result)
    return jsonify({'error': 'Failed to update status'}), 400

@app.route('/api/messages/<int:message_id>/status', methods=['GET'])
def get_message_status(message_id):
    status = message_status_manager.get_message_status(message_id)

    if status:
        return jsonify(status)
    return jsonify({'error': 'Message not found'}), 404

@app.route('/api/rooms/<int:room_id>/message-statuses', methods=['GET'])
def get_room_message_statuses(room_id):
    user_id = request.args.get('user_id', type=int)
    statuses = message_status_manager.get_room_message_statuses(room_id, user_id)
    return jsonify(statuses)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
