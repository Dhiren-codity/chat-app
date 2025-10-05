from flask import Flask, request, jsonify
from models import db, User, Message, Room
from datetime import datetime

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
