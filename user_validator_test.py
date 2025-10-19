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
    ("ab", False),  # Edge case: too short
    ("a" * 21, False),  # Edge case: too long
    ("invalid-user!", False)  # Error case: invalid characters
])

def test_validate_username(username, expected):
    validator = UserValidator()
    assert validator.validate_username(username) == expected


import pytest
from user_validator import UserValidator

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
    ("Short1!", {'valid': False, 'messages': ['Password must be at least 8 characters']}),
    ("nouppercase1!", {'valid': False, 'messages': ['Password must contain at least one uppercase letter']}),
    ("NOLOWERCASE1!", {'valid': False, 'messages': ['Password must contain at least one lowercase letter']}),
    ("NoSpecialChar1", {'valid': False, 'messages': ['Password must contain at least one special character']}),
    ("Valid1Password!", {'valid': True, 'messages': []}),
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
from typing import Dict, Any

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
    def validate_password(password: str) -> Dict[str, Any]:
        if len(password) < UserValidator.MIN_PASSWORD_LENGTH:
            return {'valid': False, 'messages': 'Password too short'}
        return {'valid': True, 'messages': ''}
    @staticmethod
    def validate_display_name(display_name: str) -> bool:
        return len(display_name) > 0
    @staticmethod
    def validate_user_profile(profile: Dict[str, str]) -> Dict[str, Any]:
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
    ({"username": "validuser", "email": "user@example.com", "password": "strongpass"}, {'valid': True, 'errors': {}}),
    # Error case: invalid username
    ({"username": "us", "email": "user@example.com", "password": "strongpass"}, {'valid': False, 'errors': {'username': 'Invalid username format'}}),
    # Error case: invalid email
    ({"username": "validuser", "email": "userexample.com", "password": "strongpass"}, {'valid': False, 'errors': {'email': 'Invalid email format'}}),
    # Edge case: missing password
    ({"username": "validuser", "email": "user@example.com"}, {'valid': True, 'errors': {}}),
    # Edge case: invalid display name
    ({"username": "validuser", "email": "user@example.com", "display_name": ""}, {'valid': False, 'errors': {'display_name': 'Invalid display name'}}),
])

def test_validate_user_profile(profile, expected):
    validator = UserValidator()
    result = validator.validate_user_profile(profile)
    assert result == expected


import pytest
from user_validator import UserValidator

@pytest.mark.parametrize("bio, max_length, expected", [
    ("This is a valid bio.", 500, "This is a valid bio."),  # Happy path
    ("", 500, ""),  # Edge case: empty bio
    ("   Bio with leading and trailing spaces   ", 500, "Bio with leading and trailing spaces"),  # Edge case: whitespace
    ("A" * 600, 500, "A" * 500),  # Edge case: bio longer than max_length
    ("Bio with null byte \x00 in the middle", 500, "Bio with null byte  in the middle"),  # Error case: null byte
])

def test_sanitize_bio(bio, max_length, expected):
    validator = UserValidator()
    assert validator.sanitize_bio(bio, max_length) == expected

