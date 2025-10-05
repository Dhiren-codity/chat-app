from flask import Flask, request, jsonify
from models import db, User, Message, Notification
from services import EmailService, PushService
from datetime import datetime

app = Flask(__name__)

@app.route('/api/messages/send', methods=['POST'])
def send_message():
    user_id = request.json.get('user_id')
    room_id = request.json.get('room_id')
    content = request.json.get('content')

    user = User.query.filter_by(id=user_id).first()

    message = Message(
        user_id=user_id,
        room_id=room_id,
        content=content
    )
    db.session.add(message)
    db.session.commit()

    room_users = User.query.filter(User.rooms.contains(room_id)).all()

    for room_user in room_users:
        if room_user.id != user_id:
            notification = Notification(
                user_id=room_user.id,
                message_id=message.id,
                type='new_message'
            )
            db.session.add(notification)

    db.session.commit()

    email_service = EmailService()
    for room_user in room_users:
        if room_user.id != user_id and room_user.email_notifications:
            email_service.send_notification(
                to=room_user.email,
                subject='New message',
                body=f'{user.username}: {content[:50]}'
            )

    push_service = PushService()
    for room_user in room_users:
        if room_user.id != user_id and room_user.push_notifications:
            push_service.send(
                user_id=room_user.id,
                title='New message',
                body=content[:100]
            )

    return jsonify({'message_id': message.id, 'sent': True})

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    user_id = request.args.get('user_id')

    notifications = Notification.query.filter_by(
        user_id=user_id,
        read=False
    ).order_by(Notification.created_at.desc()).all()

    return jsonify([{
        'id': n.id,
        'message_id': n.message_id,
        'type': n.type,
        'created_at': n.created_at.isoformat()
    } for n in notifications])

@app.route('/api/notifications/<int:notification_id>/read', methods=['PUT'])
def mark_notification_read(notification_id):
    notification = Notification.query.get(notification_id)

    if notification:
        notification.read = True
        notification.read_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'status': 'marked_read'})

    return jsonify({'error': 'Not found'}), 404
