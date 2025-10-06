from datetime import datetime, timedelta

class TypingIndicator:
    def __init__(self):
        self.typing_users = {}

    def user_started_typing(self, room_id, user_id, username):
        if room_id not in self.typing_users:
            self.typing_users[room_id] = {}

        self.typing_users[room_id][user_id] = {
            'username': username,
            'started_at': datetime.now()
        }

    def user_stopped_typing(self, room_id, user_id):
        if room_id in self.typing_users and user_id in self.typing_users[room_id]:
            del self.typing_users[room_id][user_id]

    def get_typing_users(self, room_id):
        if room_id not in self.typing_users:
            return []

        current_time = datetime.now()
        active_typers = []

        for user_id, data in list(self.typing_users[room_id].items()):
            if current_time - data['started_at'] < timedelta(seconds=5):
                active_typers.append({
                    'user_id': user_id,
                    'username': data['username']
                })
            else:
                del self.typing_users[room_id][user_id]

        return active_typers

typing_indicator = TypingIndicator()
