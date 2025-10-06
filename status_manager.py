from datetime import datetime
from models import db

class UserStatus:
    def __init__(self, user_id):
        self.user_id = user_id
        self.is_online = False
        self.last_seen = None

    def set_online(self):
        self.is_online = True
        self.last_seen = datetime.now()

    def set_offline(self):
        self.is_online = False
        self.last_seen = datetime.now()

    def get_status(self):
        return {
            'user_id': self.user_id,
            'is_online': self.is_online,
            'last_seen': self.last_seen
        }

class StatusManager:
    def __init__(self):
        self.user_statuses = {}

    def update_user_status(self, user_id, is_online):
        if user_id not in self.user_statuses:
            self.user_statuses[user_id] = UserStatus(user_id)

        if is_online:
            self.user_statuses[user_id].set_online()
        else:
            self.user_statuses[user_id].set_offline()

    def get_user_status(self, user_id):
        if user_id in self.user_statuses:
            return self.user_statuses[user_id].get_status()
        return {'user_id': user_id, 'is_online': False, 'last_seen': None}

    def get_group_members_status(self, member_ids):
        statuses = []
        for member_id in member_ids:
            statuses.append(self.get_user_status(member_id))
        return statuses

status_manager = StatusManager()
