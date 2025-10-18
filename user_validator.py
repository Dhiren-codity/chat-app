"""
User Profile Validator
Validates user profile data for the chat application
"""
from typing import Dict, Optional, List
import re


class UserValidator:
    """Validates user profile information"""

    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 30
    MIN_PASSWORD_LENGTH = 8

    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Validate username format

        Args:
            username: Username to validate

        Returns:
            True if valid, False otherwise
        """
        if not username:
            return False

        if len(username) < UserValidator.MIN_USERNAME_LENGTH:
            return False

        if len(username) > UserValidator.MAX_USERNAME_LENGTH:
            return False

        # Username can only contain alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False

        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format

        Args:
            email: Email address to validate

        Returns:
            True if valid, False otherwise
        """
        if not email:
            return False

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))

    @staticmethod
    def validate_password(password: str) -> Dict[str, any]:
        """
        Validate password strength

        Args:
            password: Password to validate

        Returns:
            Dictionary with validation result and messages
        """
        result = {
            'valid': True,
            'messages': []
        }

        if not password:
            result['valid'] = False
            result['messages'].append('Password is required')
            return result

        if len(password) < UserValidator.MIN_PASSWORD_LENGTH:
            result['valid'] = False
            result['messages'].append(f'Password must be at least {UserValidator.MIN_PASSWORD_LENGTH} characters')

        if not re.search(r'[A-Z]', password):
            result['valid'] = False
            result['messages'].append('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', password):
            result['valid'] = False
            result['messages'].append('Password must contain at least one lowercase letter')

        if not re.search(r'\d', password):
            result['valid'] = False
            result['messages'].append('Password must contain at least one digit')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            result['valid'] = False
            result['messages'].append('Password must contain at least one special character')

        return result

    @staticmethod
    def validate_display_name(display_name: str) -> bool:
        """
        Validate display name

        Args:
            display_name: Display name to validate

        Returns:
            True if valid, False otherwise
        """
        if not display_name:
            return False

        if len(display_name.strip()) < 1:
            return False

        if len(display_name) > 50:
            return False

        return True

    @staticmethod
    def validate_user_profile(profile: Dict[str, str]) -> Dict[str, any]:
        """
        Validate complete user profile

        Args:
            profile: Dictionary containing user profile data

        Returns:
            Dictionary with validation result and field-specific errors
        """
        result = {
            'valid': True,
            'errors': {}
        }

        # Validate username
        if 'username' not in profile or not UserValidator.validate_username(profile['username']):
            result['valid'] = False
            result['errors']['username'] = 'Invalid username format'

        # Validate email
        if 'email' not in profile or not UserValidator.validate_email(profile['email']):
            result['valid'] = False
            result['errors']['email'] = 'Invalid email format'

        # Validate password if provided
        if 'password' in profile:
            password_result = UserValidator.validate_password(profile['password'])
            if not password_result['valid']:
                result['valid'] = False
                result['errors']['password'] = password_result['messages']

        # Validate display name if provided
        if 'display_name' in profile and not UserValidator.validate_display_name(profile['display_name']):
            result['valid'] = False
            result['errors']['display_name'] = 'Invalid display name'

        return result

    @staticmethod
    def sanitize_bio(bio: str, max_length: int = 500) -> str:
        """
        Sanitize user bio text

        Args:
            bio: Bio text to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized bio text
        """
        if not bio:
            return ""

        # Strip whitespace
        sanitized = bio.strip()

        # Truncate to max length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        # Remove any null bytes or other problematic characters
        sanitized = sanitized.replace('\x00', '')

        return sanitized
