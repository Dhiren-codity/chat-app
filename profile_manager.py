from models import db, User
import os
import base64
from datetime import datetime

class ProfileManager:
    def __init__(self):
        self.upload_folder = 'uploads/profiles'

    def upload_profile_picture(self, user_id, image_data, filename):
        user = User.query.get(user_id)
        if not user:
            return None

        os.makedirs(self.upload_folder, exist_ok=True)

        file_path = os.path.join(self.upload_folder, f"{user_id}_{filename}")

        if image_data.startswith('data:image'):
            header, encoded = image_data.split(',', 1)
            image_bytes = base64.b64decode(encoded)
            with open(file_path, 'wb') as f:
                f.write(image_bytes)
        else:
            with open(file_path, 'wb') as f:
                f.write(image_data)

        user.profile_picture = file_path
        db.session.commit()

        return {
            'user_id': user_id,
            'profile_picture': file_path,
            'uploaded_at': datetime.utcnow().isoformat()
        }

    def update_display_name(self, user_id, display_name):
        user = User.query.get(user_id)
        if not user:
            return None

        user.display_name = display_name
        db.session.commit()

        return {
            'user_id': user_id,
            'display_name': display_name
        }

    def update_status_message(self, user_id, status_message):
        user = User.query.get(user_id)
        if not user:
            return None

        user.status_message = status_message
        db.session.commit()

        return {
            'user_id': user_id,
            'status_message': status_message
        }

    def update_bio(self, user_id, bio):
        user = User.query.get(user_id)
        if not user:
            return None

        user.bio = bio
        db.session.commit()

        return {
            'user_id': user_id,
            'bio': bio
        }

    def get_profile(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return None

        return {
            'user_id': user.id,
            'username': user.username,
            'display_name': user.display_name,
            'email': user.email,
            'profile_picture': user.profile_picture,
            'status_message': user.status_message,
            'bio': user.bio,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }

profile_manager = ProfileManager()
