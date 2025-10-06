from datetime import datetime
from models import db, Message

class MessageStatusManager:
    def __init__(self):
        pass

    def mark_as_delivered(self, message_id, user_id):
        message = Message.query.get(message_id)
        if message and message.user_id != user_id:
            message.delivered_at = datetime.utcnow()
            message.status = 'delivered'
            db.session.commit()
            return {
                'message_id': message_id,
                'status': 'delivered',
                'delivered_at': message.delivered_at.isoformat()
            }
        return None

    def mark_as_read(self, message_id, user_id):
        message = Message.query.get(message_id)
        if message and message.user_id != user_id:
            message.read_at = datetime.utcnow()
            message.status = 'read'
            db.session.commit()
            return {
                'message_id': message_id,
                'status': 'read',
                'read_at': message.read_at.isoformat()
            }
        return None

    def get_message_status(self, message_id):
        message = Message.query.get(message_id)
        if message:
            return {
                'message_id': message_id,
                'status': message.status,
                'sent_at': message.sent_at.isoformat() if message.sent_at else None,
                'delivered_at': message.delivered_at.isoformat() if message.delivered_at else None,
                'read_at': message.read_at.isoformat() if message.read_at else None
            }
        return None

    def get_room_message_statuses(self, room_id, user_id):
        messages = Message.query.filter_by(room_id=room_id, user_id=user_id).all()
        statuses = []
        for msg in messages:
            statuses.append({
                'message_id': msg.id,
                'status': msg.status,
                'sent_at': msg.sent_at.isoformat() if msg.sent_at else None,
                'delivered_at': msg.delivered_at.isoformat() if msg.delivered_at else None,
                'read_at': msg.read_at.isoformat() if msg.read_at else None
            })
        return statuses

message_status_manager = MessageStatusManager()
