"""
Auto-generated tests using LLM and RAG
"""

import pytest


import pytest
import re

class UserValidator:
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20
    @staticmethod
    def validate_username(username: str) -> bool:
        if not username:
            return False
        if len(username) < UserValidator.MIN_USERNAME_LENGTH:
            return False
        if len(username) > UserValidator.MAX_USERNAME_LENGTH:
            return False
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False
        return True
@pytest.mark.parametrize("username, expected", [
    ("valid_user", True),  # Happy path
    ("", False),  # Error case: empty username
    ("ab", False),  # Edge case: below minimum length
    ("a" * 21, False),  # Edge case: above maximum length
    ("invalid-user!", False)  # Error case: invalid characters
])

def test_validate_username(username, expected):
    assert UserValidator.validate_username(username) == expected


import pytest
import re

@pytest.mark.parametrize("email, expected", [
    ("test@example.com", True),  # Happy path
    ("invalid-email", False),    # Error case: missing '@' and domain
    ("@example.com", False),     # Edge case: missing local part
    ("test@.com", False),        # Edge case: missing domain name
    ("test@com", False),         # Edge case: missing top-level domain
])

def test_validate_email(email, expected):
    validator = UserValidator()
    assert validator.validate_email(email) == expected


import pytest
from typing import Dict
import re

class UserValidator:
    MIN_PASSWORD_LENGTH = 8
    @staticmethod
    def validate_password(password: str) -> Dict[str, any]:
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
@pytest.mark.parametrize("password, expected", [
    ("", {'valid': False, 'messages': ['Password is required']}),
    ("short", {'valid': False, 'messages': ['Password must be at least 8 characters', 'Password must contain at least one uppercase letter', 'Password must contain at least one digit', 'Password must contain at least one special character']}),
    ("NoDigits!", {'valid': False, 'messages': ['Password must contain at least one digit']}),
    ("Valid1!", {'valid': False, 'messages': ['Password must be at least 8 characters']}),
    ("ValidPassword1!", {'valid': True, 'messages': []}),
])

def test_validate_password(password, expected):
    validator = UserValidator()
    assert validator.validate_password(password) == expected


import pytest
from user_validator import UserValidator

@pytest.mark.parametrize("display_name, expected", [
    ("ValidName", True),  # Happy path
    ("", False),  # Error case: empty string
    ("   ", False),  # Edge case: only spaces
    ("A" * 51, False),  # Edge case: exceeds max length
    ("A" * 50, True),  # Edge case: exactly max length
])

def test_validate_display_name(display_name, expected):
    validator = UserValidator()
    assert validator.validate_display_name(display_name) == expected


import pytest
from typing import Dict

class UserValidator:
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20
    MIN_PASSWORD_LENGTH = 8
    @staticmethod
    def validate_username(username: str) -> bool:
        return UserValidator.MIN_USERNAME_LENGTH <= len(username) <= UserValidator.MAX_USERNAME_LENGTH
    @staticmethod
    def validate_email(email: str) -> bool:
        return "@" in email and "." in email
    @staticmethod
    def validate_password(password: str) -> Dict[str, any]:
        if len(password) < UserValidator.MIN_PASSWORD_LENGTH:
            return {'valid': False, 'messages': 'Password too short'}
        return {'valid': True, 'messages': ''}
    @staticmethod
    def validate_display_name(display_name: str) -> bool:
        return len(display_name) > 0
    def validate_user_profile(self, profile: Dict[str, str]) -> Dict[str, any]:
        result = {
            'valid': True,
            'errors': {}
        }
        if 'username' not in profile or not UserValidator.validate_username(profile['username']):
            result['valid'] = False
            result['errors']['username'] = 'Invalid username format'
        if 'email' not in profile or not UserValidator.validate_email(profile['email']):
            result['valid'] = False
            result['errors']['email'] = 'Invalid email format'
        if 'password' in profile:
            password_result = UserValidator.validate_password(profile['password'])
            if not password_result['valid']:
                result['valid'] = False
                result['errors']['password'] = password_result['messages']
        if 'display_name' in profile and not UserValidator.validate_display_name(profile['display_name']):
            result['valid'] = False
            result['errors']['display_name'] = 'Invalid display name'
        return result
@pytest.mark.parametrize("profile, expected", [
    # Happy path
    ({"username": "validUser", "email": "user@example.com", "password": "strongPass123"}, {'valid': True, 'errors': {}}),
    # Missing username
    ({"email": "user@example.com", "password": "strongPass123"}, {'valid': False, 'errors': {'username': 'Invalid username format'}}),
    # Invalid email
    ({"username": "validUser", "email": "userexample.com", "password": "strongPass123"}, {'valid': False, 'errors': {'email': 'Invalid email format'}}),
    # Short password
    ({"username": "validUser", "email": "user@example.com", "password": "short"}, {'valid': False, 'errors': {'password': 'Password too short'}}),
    # Edge case: Empty display name
    ({"username": "validUser", "email": "user@example.com", "password": "strongPass123", "display_name": ""}, {'valid': False, 'errors': {'display_name': 'Invalid display name'}}),
])

def test_validate_user_profile(profile, expected):
    validator = UserValidator()
    result = validator.validate_user_profile(profile)
    assert result == expected


import pytest
from user_validator import UserValidator

@pytest.mark.parametrize("bio, max_length, expected", [
    # Happy path: bio within max length
    ("This is a valid bio.", 500, "This is a valid bio."),
    # Edge case: bio exactly at max length
    ("a" * 500, 500, "a" * 500),
    # Edge case: bio exceeding max length
    ("a" * 501, 500, "a" * 500),
    # Error case: bio with null byte
    ("This bio has a null byte\x00 in it.", 500, "This bio has a null byte in it."),
    # Edge case: empty bio
    ("", 500, ""),
])

def test_sanitize_bio(bio, max_length, expected):
    validator = UserValidator()
    assert validator.sanitize_bio(bio, max_length) == expected

