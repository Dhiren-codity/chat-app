"""
Auto-generated tests using LLM and RAG
"""

import pytest


from functools import wraps
from unittest.mock import Mock, patch
import pytest
from flask import Flask, request, jsonify

from routes.reactions import require_auth

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app.config['TESTING'] = True
    return app

@pytest.fixture
def mock_function():
    """Create a mock function to be decorated."""
    mock_func = Mock()
    mock_func.__name__ = 'test_function'
    mock_func.return_value = ('success', 200)
    return mock_func

class TestRequireAuth:
    """Test cases for the require_auth decorator."""

    @patch('routes.reactions.request')

    def test_auth_with_header_user_id(self, mock_request, app, mock_function):
        """Test authentication with user ID in headers."""
        with app.test_request_context():
            mock_request.headers.get.return_value = '123'
            mock_request.args.get.return_value = None
            
            decorated_func = require_auth(mock_function)
            result = decorated_func('arg1', kwarg1='value1')
            
            assert result == ('success', 200)
            mock_function.assert_called_once_with('arg1', user_id=123, kwarg1='value1')

    @patch('routes.reactions.request')

    def test_auth_with_query_param_user_id(self, mock_request, app, mock_function):
        """Test authentication with user ID in query parameters."""
        with app.test_request_context():
            mock_request.headers.get.return_value = None
            mock_request.args.get.return_value = '456'
            
            decorated_func = require_auth(mock_function)
            result = decorated_func('arg1', kwarg1='value1')
            
            assert result == ('success', 200)
            mock_function.assert_called_once_with('arg1', user_id=456, kwarg1='value1')

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_auth_header_priority_over_query_param(self, mock_jsonify, mock_request, app, mock_function):
        """Test that header user ID takes priority over query parameter."""
        with app.test_request_context():
            mock_request.headers.get.return_value = '789'
            mock_request.args.get.return_value = '999'
            
            decorated_func = require_auth(mock_function)
            result = decorated_func('arg1', kwarg1='value1')
            
            assert result == ('success', 200)
            mock_function.assert_called_once_with('arg1', user_id=789, kwarg1='value1')

    @pytest.mark.parametrize("header_value,query_value", [
        (None, None),
        ('', None),
        (None, ''),
        ('', ''),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_auth_missing_user_id_scenarios(self, mock_jsonify, mock_request, header_value, query_value, app, mock_function):
        """Test various scenarios where user ID is missing or empty."""
        with app.test_request_context():
            mock_request.headers.get.return_value = header_value
            mock_request.args.get.return_value = query_value
            mock_jsonify.return_value = {"error": "Authentication required"}
            
            decorated_func = require_auth(mock_function)
            result = decorated_func('arg1', kwarg1='value1')
            
            mock_jsonify.assert_called_once_with({"error": "Authentication required"})
            assert result == ({"error": "Authentication required"}, 401)
            mock_function.assert_not_called()

    @pytest.mark.parametrize("user_id_str,expected_int", [
        ('0', 0),
        ('1', 1),
        ('999999', 999999),
        ('-1', -1),
    ])
    @patch('routes.reactions.request')

    def test_user_id_conversion_to_int(self, mock_request, user_id_str, expected_int, app, mock_function):
        """Test conversion of string user ID to integer."""
        with app.test_request_context():
            mock_request.headers.get.return_value = user_id_str
            mock_request.args.get.return_value = None
            
            decorated_func = require_auth(mock_function)
            result = decorated_func()
            
            assert result == ('success', 200)
            mock_function.assert_called_once_with(user_id=expected_int)

    @patch('routes.reactions.request')

    def test_invalid_user_id_conversion(self, mock_request, app, mock_function):
        """Test handling of invalid user ID that cannot be converted to int."""
        with app.test_request_context():
            mock_request.headers.get.return_value = 'invalid_id'
            mock_request.args.get.return_value = None
            
            decorated_func = require_auth(mock_function)
            
            with pytest.raises(ValueError):
                decorated_func()

    @patch('routes.reactions.request')

    def test_decorated_function_preserves_metadata(self, mock_request, app):
        """Test that the decorator preserves function metadata."""
        def sample_function():
            """Sample function docstring."""
            return "original"
        
        with app.test_request_context():
            mock_request.headers.get.return_value = '123'
            mock_request.args.get.return_value = None
            
            decorated_func = require_auth(sample_function)
            
            assert decorated_func.__name__ == 'sample_function'
            assert decorated_func.__doc__ == 'Sample function docstring.'

    @patch('routes.reactions.request')

    def test_function_with_no_args_or_kwargs(self, mock_request, app):
        """Test decorator with function that takes no arguments."""
        mock_func = Mock()
        mock_func.__name__ = 'no_args_function'
        mock_func.return_value = 'no_args_result'
        
        with app.test_request_context():
            mock_request.headers.get.return_value = '555'
            mock_request.args.get.return_value = None
            
            decorated_func = require_auth(mock_func)
            result = decorated_func()
            
            assert result == 'no_args_result'
            mock_func.assert_called_once_with(user_id=555)

    @patch('routes.reactions.request')

    def test_function_with_only_args(self, mock_request, app):
        """Test decorator with function that only takes positional arguments."""
        mock_func = Mock()
        mock_func.__name__ = 'args_only_function'
        mock_func.return_value = 'args_result'
        
        with app.test_request_context():
            mock_request.headers.get.return_value = '777'
            mock_request.args.get.return_value = None
            
            decorated_func = require_auth(mock_func)
            result = decorated_func('pos1', 'pos2', 'pos3')
            
            assert result == 'args_result'
            mock_func.assert_called_once_with('pos1', 'pos2', 'pos3', user_id=777)

    @patch('routes.reactions.request')

    def test_function_with_only_kwargs(self, mock_request, app):
        """Test decorator with function that only takes keyword arguments."""
        mock_func = Mock()
        mock_func.__name__ = 'kwargs_only_function'
        mock_func.return_value = 'kwargs_result'
        
        with app.test_request_context():
            mock_request.headers.get.return_value = '888'
            mock_request.args.get.return_value = None
            
            decorated_func = require_auth(mock_func)
            result = decorated_func(key1='value1', key2='value2')
            
            assert result == 'kwargs_result'
            mock_func.assert_called_once_with(user_id=888, key1='value1', key2='value2')

    @patch('routes.reactions.request')

    def test_user_id_kwarg_override_behavior(self, mock_request, app):
        """Test that user_id kwarg is properly added without conflicts."""
        mock_func = Mock()
        mock_func.__name__ = 'test_function'
        mock_func.return_value = 'success'
        
        with app.test_request_context():
            mock_request.headers.get.return_value = '999'
            mock_request.args.get.return_value = None
            
            decorated_func = require_auth(mock_func)
            result = decorated_func(existing_param='value')
            
            assert result == 'success'
            mock_func.assert_called_once_with(existing_param='value', user_id=999)

# Standard library
# Third-party
# Local


import json
from unittest.mock import Mock, patch
import pytest
from flask import Flask

from routes.reactions import add_reaction

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app.config['TESTING'] = True
    return app

@pytest.fixture
def app_context(app):
    """Create Flask app context for testing."""
    with app.app_context():
        yield app

@pytest.fixture
def request_context(app):
    """Create Flask request context for testing."""
    with app.test_request_context():
        yield

@pytest.fixture
def mock_reaction_manager():
    """Mock reaction manager."""
    with patch('routes.reactions.reaction_manager') as mock:
        yield mock

@pytest.fixture
def mock_request():
    """Mock Flask request object."""
    with patch('routes.reactions.request') as mock:
        yield mock

@pytest.fixture
def mock_jsonify():
    """Mock Flask jsonify function."""
    with patch('routes.reactions.jsonify') as mock:
        mock.side_effect = lambda x: x  # Return the dict as-is for testing
        yield mock

class TestAddReaction:
    """Test cases for add_reaction function."""


    def test_successful_reaction_addition(self, mock_request, mock_jsonify, mock_reaction_manager):
        """Test successful reaction addition."""
        # Arrange
        user_id = 123
        request_data = {"message_id": 456, "emoji": "👍"}
        mock_request.get_json.return_value = request_data
        mock_reaction_manager.add_reaction.return_value = {"success": True, "reaction_id": 789}

        # Act
        result, status_code = add_reaction(user_id)

        # Assert
        mock_request.get_json.assert_called_once()
        mock_reaction_manager.add_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji="👍"
        )
        mock_jsonify.assert_called_once_with({"success": True, "reaction_id": 789})
        assert result == {"success": True, "reaction_id": 789}
        assert status_code == 200


    def test_unsuccessful_reaction_addition(self, mock_request, mock_jsonify, mock_reaction_manager):
        """Test unsuccessful reaction addition returns 400."""
        # Arrange
        user_id = 123
        request_data = {"message_id": 456, "emoji": "👍"}
        mock_request.get_json.return_value = request_data
        mock_reaction_manager.add_reaction.return_value = {"success": False, "error": "Duplicate reaction"}

        # Act
        result, status_code = add_reaction(user_id)

        # Assert
        mock_reaction_manager.add_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji="👍"
        )
        mock_jsonify.assert_called_once_with({"success": False, "error": "Duplicate reaction"})
        assert result == {"success": False, "error": "Duplicate reaction"}
        assert status_code == 400

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "message_id and emoji are required"),
        ({}, "message_id and emoji are required"),
        ({"message_id": 123}, "message_id and emoji are required"),
        ({"emoji": "👍"}, "message_id and emoji are required"),
        ({"message_id": 123, "other_field": "value"}, "message_id and emoji are required"),
    ])

    def test_invalid_request_data(self, mock_request, mock_jsonify, mock_reaction_manager, request_data, expected_error):
        """Test various invalid request data scenarios."""
        # Arrange
        user_id = 123
        mock_request.get_json.return_value = request_data

        # Act
        result, status_code = add_reaction(user_id)

        # Assert
        mock_request.get_json.assert_called_once()
        mock_reaction_manager.add_reaction.assert_not_called()
        mock_jsonify.assert_called_once_with({"error": expected_error})
        assert result == {"error": expected_error}
        assert status_code == 400


    def test_value_error_handling(self, mock_request, mock_jsonify, mock_reaction_manager):
        """Test ValueError exception handling."""
        # Arrange
        user_id = 123
        request_data = {"message_id": 456, "emoji": "👍"}
        mock_request.get_json.return_value = request_data
        mock_reaction_manager.add_reaction.side_effect = ValueError("Invalid emoji format")

        # Act
        result, status_code = add_reaction(user_id)

        # Assert
        mock_reaction_manager.add_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji="👍"
        )
        mock_jsonify.assert_called_once_with({"error": "Invalid emoji format"})
        assert result == {"error": "Invalid emoji format"}
        assert status_code == 400


    def test_generic_exception_handling(self, mock_request, mock_jsonify, mock_reaction_manager):
        """Test generic exception handling."""
        # Arrange
        user_id = 123
        request_data = {"message_id": 456, "emoji": "👍"}
        mock_request.get_json.return_value = request_data
        mock_reaction_manager.add_reaction.side_effect = RuntimeError("Database connection failed")

        # Act
        result, status_code = add_reaction(user_id)

        # Assert
        mock_reaction_manager.add_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji="👍"
        )
        mock_jsonify.assert_called_once_with({"error": "Failed to add reaction: Database connection failed"})
        assert result == {"error": "Failed to add reaction: Database connection failed"}
        assert status_code == 500

    @pytest.mark.parametrize("user_id,message_id,emoji", [
        (0, 1, "👍"),  # Zero user_id
        (123, 0, "👎"),  # Zero message_id
        (-1, 456, "❤️"),  # Negative user_id
        (123, -1, "😂"),  # Negative message_id
        (999999, 999999, "🔥"),  # Large values
        (1, 1, "🎉"),  # Minimum positive values
    ])

    def test_boundary_values(self, mock_request, mock_jsonify, mock_reaction_manager, user_id, message_id, emoji):
        """Test boundary value conditions."""
        # Arrange
        request_data = {"message_id": message_id, "emoji": emoji}
        mock_request.get_json.return_value = request_data
        mock_reaction_manager.add_reaction.return_value = {"success": True, "reaction_id": 1}

        # Act
        result, status_code = add_reaction(user_id)

        # Assert
        mock_reaction_manager.add_reaction.assert_called_once_with(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        )
        assert status_code == 200


    def test_special_emoji_characters(self, mock_request, mock_jsonify, mock_reaction_manager):
        """Test handling of various emoji formats."""
        # Arrange
        user_id = 123
        special_emojis = ["👨‍💻", "🏳️‍🌈", "👍🏽", "🤷‍♀️", "💯"]
        
        for emoji in special_emojis:
            request_data = {"message_id": 456, "emoji": emoji}
            mock_request.get_json.return_value = request_data
            mock_reaction_manager.add_reaction.return_value = {"success": True, "reaction_id": 1}

            # Act
            result, status_code = add_reaction(user_id)

            # Assert
            mock_reaction_manager.add_reaction.assert_called_with(
                message_id=456,
                user_id=123,
                emoji=emoji
            )
            assert status_code == 200

        # Verify call count
        assert mock_reaction_manager.add_reaction.call_count == len(special_emojis)


    def test_request_json_exception(self, mock_request, mock_jsonify, mock_reaction_manager):
        """Test when request.get_json() raises an exception."""
        # Arrange
        user_id = 123
        mock_request.get_json.side_effect = Exception("JSON parsing error")

        # Act
        result, status_code = add_reaction(user_id)

        # Assert
        mock_request.get_json.assert_called_once()
        mock_reaction_manager.add_reaction.assert_not_called()
        mock_jsonify.assert_called_once_with({"error": "Failed to add reaction: JSON parsing error"})
        assert result == {"error": "Failed to add reaction: JSON parsing error"}
        assert status_code == 500


    def test_none_user_id(self, mock_request, mock_jsonify, mock_reaction_manager):
        """Test with None user_id."""
        # Arrange
        user_id = None
        request_data = {"message_id": 456, "emoji": "👍"}
        mock_request.get_json.return_value = request_data
        mock_reaction_manager.add_reaction.return_value = {"success": True, "reaction_id": 1}

        # Act
        result, status_code = add_reaction(user_id)

        # Assert
        mock_reaction_manager.add_reaction.assert_called_once_with(
            message_id=456,
            user_id=None,
            emoji="👍"
        )
        assert status_code == 200


    def test_empty_string_emoji(self, mock_request, mock_jsonify, mock_reaction_manager):
        """Test with empty string emoji."""
        # Arrange
        user_id = 123
        request_data = {"message_id": 456, "emoji": ""}
        mock_request.get_json.return_value = request_data
        mock_reaction_manager.add_reaction.return_value = {"success": True, "reaction_id": 1}

        # Act
        result, status_code = add_reaction(user_id)

        # Assert
        mock_reaction_manager.add_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji=""
        )
        assert status_code == 200

# Standard library
# Third-party
# Local


import json
from unittest.mock import patch, Mock
import pytest
from flask import Flask

from routes.reactions import remove_reaction

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app.config['TESTING'] = True
    return app

@pytest.fixture
def app_context(app):
    """Create application context for testing."""
    with app.app_context():
        yield app

class TestRemoveReaction:
    """Test cases for remove_reaction function."""

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_successful_reaction_removal(self, mock_jsonify, mock_reaction_manager, mock_request, app_context):
        """Test successful removal of a reaction."""
        # Arrange
        user_id = 123
        mock_request.get_json.return_value = {
            'message_id': 456,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.return_value = {'success': True}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = remove_reaction(user_id)
        
        # Assert
        mock_reaction_manager.remove_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({'success': True})
        assert result[1] == 200

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_not_found(self, mock_jsonify, mock_reaction_manager, mock_request, app_context):
        """Test when reaction to remove is not found."""
        # Arrange
        user_id = 123
        mock_request.get_json.return_value = {
            'message_id': 456,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.return_value = {'success': False}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = remove_reaction(user_id)
        
        # Assert
        mock_reaction_manager.remove_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({'success': False})
        assert result[1] == 404

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "message_id and emoji are required"),
        ({}, "message_id and emoji are required"),
        ({'message_id': 456}, "message_id and emoji are required"),
        ({'emoji': '👍'}, "message_id and emoji are required"),
        ({'message_id': None, 'emoji': '👍'}, "message_id and emoji are required"),
        ({'message_id': 456, 'emoji': None}, "message_id and emoji are required"),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_invalid_request_data(self, mock_jsonify, mock_request, request_data, expected_error, app_context):
        """Test various invalid request data scenarios."""
        # Arrange
        user_id = 123
        mock_request.get_json.return_value = request_data
        mock_jsonify.return_value = Mock()
        
        # Act
        result = remove_reaction(user_id)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": expected_error})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_exception(self, mock_jsonify, mock_reaction_manager, mock_request, app_context):
        """Test when reaction_manager raises an exception."""
        # Arrange
        user_id = 123
        mock_request.get_json.return_value = {
            'message_id': 456,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.side_effect = Exception("Database connection failed")
        mock_jsonify.return_value = Mock()
        
        # Act
        result = remove_reaction(user_id)
        
        # Assert
        mock_reaction_manager.remove_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({"error": "Failed to remove reaction: Database connection failed"})
        assert result[1] == 500

    @pytest.mark.parametrize("user_id,message_id,emoji", [
        (0, 1, '👍'),
        (-1, 999999, '🎉'),
        (999999, 0, '❤️'),
        (1, 1, '🔥'),
        (2147483647, 2147483647, '💯'),  # Max int values
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_boundary_values(self, mock_jsonify, mock_reaction_manager, mock_request, user_id, message_id, emoji, app_context):
        """Test with boundary values for user_id and message_id."""
        # Arrange
        mock_request.get_json.return_value = {
            'message_id': message_id,
            'emoji': emoji
        }
        mock_reaction_manager.remove_reaction.return_value = {'success': True}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = remove_reaction(user_id)
        
        # Assert
        mock_reaction_manager.remove_reaction.assert_called_once_with(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        )
        mock_jsonify.assert_called_once_with({'success': True})
        assert result[1] == 200

    @pytest.mark.parametrize("emoji", [
        '👍',
        '👎',
        '❤️',
        '😂',
        '😮',
        '😢',
        '😡',
        '🎉',
        '🔥',
        '💯',
        '👏',
        '🙏',
        '',  # Empty emoji
        'not_an_emoji',  # Text instead of emoji
        '👍👎',  # Multiple emojis
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_various_emoji_types(self, mock_jsonify, mock_reaction_manager, mock_request, emoji, app_context):
        """Test with various emoji types and edge cases."""
        # Arrange
        user_id = 123
        mock_request.get_json.return_value = {
            'message_id': 456,
            'emoji': emoji
        }
        mock_reaction_manager.remove_reaction.return_value = {'success': True}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = remove_reaction(user_id)
        
        # Assert
        mock_reaction_manager.remove_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji=emoji
        )
        mock_jsonify.assert_called_once_with({'success': True})
        assert result[1] == 200

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_returns_none(self, mock_jsonify, mock_reaction_manager, mock_request, app_context):
        """Test when reaction_manager returns None."""
        # Arrange
        user_id = 123
        mock_request.get_json.return_value = {
            'message_id': 456,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.return_value = None
        mock_jsonify.return_value = Mock()
        
        # Act
        result = remove_reaction(user_id)
        
        # Assert
        mock_reaction_manager.remove_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with(None)
        assert result[1] == 404  # None is falsy, so success is False

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_returns_empty_dict(self, mock_jsonify, mock_reaction_manager, mock_request, app_context):
        """Test when reaction_manager returns empty dictionary."""
        # Arrange
        user_id = 123
        mock_request.get_json.return_value = {
            'message_id': 456,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.return_value = {}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = remove_reaction(user_id)
        
        # Assert
        mock_reaction_manager.remove_reaction.assert_called_once_with(
            message_id=456,
            user_id=123,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({})
        assert result[1] == 404  # Empty dict doesn't have 'success' key, so falsy

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_user_id_none(self, mock_jsonify, mock_reaction_manager, mock_request, app_context):
        """Test when user_id is None."""
        # Arrange
        user_id = None
        mock_request.get_json.return_value = {
            'message_id': 456,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.return_value = {'success': True}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = remove_reaction(user_id)
        
        # Assert
        mock_reaction_manager.remove_reaction.assert_called_once_with(
            message_id=456,
            user_id=None,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({'success': True})
        assert result[1] == 200

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_complex_exception_message(self, mock_jsonify, mock_reaction_manager, mock_request, app_context):
        """Test exception handling with complex error messages."""
        # Arrange
        user_id = 123
        mock_request.get_json.return_value = {
            'message_id': 456,
            'emoji': '👍'
        }
        complex_error = Exception("Connection timeout: Unable to reach database server at 192.168.1.100:5432")
        mock_reaction_manager.remove_reaction.side_effect = complex_error
        mock_jsonify.return_value = Mock()
        
        # Act
        result = remove_reaction(user_id)
        
        # Assert
        expected_error = "Failed to remove reaction: Connection timeout: Unable to reach database server at 192.168.1.100:5432"
        mock_jsonify.assert_called_once_with({"error": expected_error})
        assert result[1] == 500

# Standard library
# Third-party
# Local


import json
import pytest
from flask import Flask
from unittest.mock import patch, Mock

from routes.reactions import toggle_reaction

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app.config['TESTING'] = True
    return app

@pytest.fixture
def app_context(app):
    """Create application context for testing."""
    with app.app_context():
        yield app

@pytest.fixture
def request_context(app):
    """Create request context for testing."""
    with app.test_request_context():
        yield

@pytest.fixture
def valid_request_data():
    """Valid request data for testing."""
    return {
        "message_id": 123,
        "emoji": "👍"
    }

@pytest.fixture
def mock_reaction_result():
    """Mock reaction manager result."""
    return {
        "message_id": 123,
        "user_id": 456,
        "emoji": "👍",
        "action": "added"
    }

class TestToggleReaction:
    """Test cases for toggle_reaction function."""

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_success_add(self, mock_reaction_manager, mock_request, 
                                       app_context, valid_request_data, mock_reaction_result):
        """Test successful reaction toggle - add reaction."""
        # Arrange
        user_id = 456
        mock_request.get_json.return_value = valid_request_data
        mock_reaction_manager.toggle_reaction.return_value = mock_reaction_result
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data == mock_reaction_result
        mock_reaction_manager.toggle_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji="👍"
        )

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_success_remove(self, mock_reaction_manager, mock_request, 
                                          app_context, valid_request_data):
        """Test successful reaction toggle - remove reaction."""
        # Arrange
        user_id = 789
        remove_result = {
            "message_id": 123,
            "user_id": 789,
            "emoji": "👍",
            "action": "removed"
        }
        mock_request.get_json.return_value = valid_request_data
        mock_reaction_manager.toggle_reaction.return_value = remove_result
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data == remove_result
        mock_reaction_manager.toggle_reaction.assert_called_once_with(
            message_id=123,
            user_id=789,
            emoji="👍"
        )

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "message_id and emoji are required"),
        ({}, "message_id and emoji are required"),
        ({"message_id": 123}, "message_id and emoji are required"),
        ({"emoji": "👍"}, "message_id and emoji are required"),
        ({"message_id": 123, "other_field": "value"}, "message_id and emoji are required"),
    ])
    @patch('routes.reactions.request')
    def test_toggle_reaction_invalid_request_data(self, mock_request, app_context, 
                                                request_data, expected_error):
        """Test toggle_reaction with invalid request data."""
        # Arrange
        user_id = 456
        mock_request.get_json.return_value = request_data
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data["error"] == expected_error

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_value_error(self, mock_reaction_manager, mock_request, 
                                       app_context, valid_request_data):
        """Test toggle_reaction when reaction_manager raises ValueError."""
        # Arrange
        user_id = 456
        error_message = "Invalid message ID"
        mock_request.get_json.return_value = valid_request_data
        mock_reaction_manager.toggle_reaction.side_effect = ValueError(error_message)
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data["error"] == error_message

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_general_exception(self, mock_reaction_manager, mock_request, 
                                             app_context, valid_request_data):
        """Test toggle_reaction when reaction_manager raises general exception."""
        # Arrange
        user_id = 456
        error_message = "Database connection failed"
        mock_request.get_json.return_value = valid_request_data
        mock_reaction_manager.toggle_reaction.side_effect = Exception(error_message)
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert response_data["error"] == f"Failed to toggle reaction: {error_message}"

    @pytest.mark.parametrize("user_id,message_id,emoji", [
        (0, 1, "👍"),
        (999999, 999999, "❤️"),
        (1, 1, "🎉"),
        (-1, 1, "👎"),  # Edge case: negative user_id
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_boundary_values(self, mock_reaction_manager, mock_request, 
                                           app_context, user_id, message_id, emoji):
        """Test toggle_reaction with boundary values."""
        # Arrange
        request_data = {"message_id": message_id, "emoji": emoji}
        expected_result = {
            "message_id": message_id,
            "user_id": user_id,
            "emoji": emoji,
            "action": "added"
        }
        mock_request.get_json.return_value = request_data
        mock_reaction_manager.toggle_reaction.return_value = expected_result
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data == expected_result
        mock_reaction_manager.toggle_reaction.assert_called_once_with(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        )

    @pytest.mark.parametrize("emoji", [
        "👍", "👎", "❤️", "😂", "😮", "😢", "😡",  # Standard emojis
        "🎉", "🔥", "💯", "👏",  # Popular reaction emojis
        "🚀", "⭐", "✅", "❌",  # Symbol emojis
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_various_emojis(self, mock_reaction_manager, mock_request, 
                                          app_context, emoji):
        """Test toggle_reaction with various emoji types."""
        # Arrange
        user_id = 456
        message_id = 123
        request_data = {"message_id": message_id, "emoji": emoji}
        expected_result = {
            "message_id": message_id,
            "user_id": user_id,
            "emoji": emoji,
            "action": "added"
        }
        mock_request.get_json.return_value = request_data
        mock_reaction_manager.toggle_reaction.return_value = expected_result
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data == expected_result

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction_reaction_manager_called_correctly(self, mock_reaction_manager, 
                                                             mock_request, app_context, 
                                                             valid_request_data):
        """Test that reaction_manager.toggle_reaction is called with correct parameters."""
        # Arrange
        user_id = 456
        mock_request.get_json.return_value = valid_request_data
        mock_reaction_manager.toggle_reaction.return_value = {"action": "added"}
        
        # Act
        toggle_reaction(user_id)
        
        # Assert
        mock_reaction_manager.toggle_reaction.assert_called_once_with(
            message_id=valid_request_data["message_id"],
            user_id=user_id,
            emoji=valid_request_data["emoji"]
        )

    @patch('routes.reactions.request')

    def test_toggle_reaction_request_get_json_called(self, mock_request, app_context):
        """Test that request.get_json() is called."""
        # Arrange
        user_id = 456
        mock_request.get_json.return_value = None
        
        # Act
        toggle_reaction(user_id)
        
        # Assert
        mock_request.get_json.assert_called_once()

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock

from routes.reactions import get_message_reactions

@pytest.fixture
def mock_reactions_data():
    """Sample reactions data for testing."""
    return {
        "👍": [
            {"user_id": "user1", "timestamp": "2023-01-01T10:00:00Z"},
            {"user_id": "user2", "timestamp": "2023-01-01T10:01:00Z"}
        ],
        "❤️": [
            {"user_id": "user3", "timestamp": "2023-01-01T10:02:00Z"}
        ]
    }

@pytest.fixture
def empty_reactions_data():
    """Empty reactions data for testing."""
    return {}

class TestGetMessageReactions:
    """Test cases for get_message_reactions function."""

    @patch('routes.reactions.reaction_manager')

    def test_successful_reaction_retrieval(self, mock_reaction_manager, mock_reactions_data):
        """Test successful retrieval of message reactions."""
        # Arrange
        message_id = "msg_123"
        mock_reaction_manager.get_message_reactions.return_value = mock_reactions_data
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == mock_reactions_data
        mock_reaction_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_empty_reactions_response(self, mock_reaction_manager, empty_reactions_data):
        """Test handling of message with no reactions."""
        # Arrange
        message_id = "msg_456"
        mock_reaction_manager.get_message_reactions.return_value = empty_reactions_data
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == {}
        mock_reaction_manager.get_message_reactions.assert_called_once_with(message_id)

    @pytest.mark.parametrize("message_id,expected_message_id", [
        ("msg_123", "msg_123"),
        ("", ""),
        ("msg_with_special_chars_!@#", "msg_with_special_chars_!@#"),
        ("very_long_message_id_" + "x" * 100, "very_long_message_id_" + "x" * 100),
        (None, None),
        (0, 0),
        (12345, 12345)
    ])
    @patch('routes.reactions.reaction_manager')

    def test_various_message_id_formats(self, mock_reaction_manager, message_id, expected_message_id, mock_reactions_data):
        """Test function with various message ID formats and types."""
        # Arrange
        mock_reaction_manager.get_message_reactions.return_value = mock_reactions_data
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == expected_message_id
        assert response_data["reactions"] == mock_reactions_data
        mock_reaction_manager.get_message_reactions.assert_called_once_with(message_id)

    @pytest.mark.parametrize("exception_type,exception_message", [
        (ValueError, "Invalid message ID format"),
        (KeyError, "Message not found"),
        (ConnectionError, "Database connection failed"),
        (TimeoutError, "Request timeout"),
        (RuntimeError, "Unexpected error occurred"),
        (Exception, "Generic error")
    ])
    @patch('routes.reactions.reaction_manager')

    def test_exception_handling(self, mock_reaction_manager, exception_type, exception_message):
        """Test proper handling of various exceptions."""
        # Arrange
        message_id = "msg_error"
        mock_reaction_manager.get_message_reactions.side_effect = exception_type(exception_message)
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get reactions: {exception_message}" in response_data["error"]
        mock_reaction_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_reaction_manager_called_with_correct_parameters(self, mock_reaction_manager):
        """Test that reaction_manager is called with the correct parameters."""
        # Arrange
        message_id = "test_msg_789"
        mock_reaction_manager.get_message_reactions.return_value = {}
        
        # Act
        get_message_reactions(message_id)
        
        # Assert
        mock_reaction_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_complex_reactions_data_structure(self, mock_reaction_manager):
        """Test handling of complex reactions data structure."""
        # Arrange
        message_id = "msg_complex"
        complex_reactions = {
            "👍": [
                {"user_id": "user1", "timestamp": "2023-01-01T10:00:00Z", "metadata": {"source": "web"}},
                {"user_id": "user2", "timestamp": "2023-01-01T10:01:00Z", "metadata": {"source": "mobile"}}
            ],
            "🎉": [
                {"user_id": "user3", "timestamp": "2023-01-01T10:02:00Z", "metadata": {"source": "api"}}
            ],
            "custom_emoji": [
                {"user_id": "user4", "timestamp": "2023-01-01T10:03:00Z", "metadata": {"custom": True}}
            ]
        }
        mock_reaction_manager.get_message_reactions.return_value = complex_reactions
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == complex_reactions
        assert len(response_data["reactions"]) == 3
        assert "👍" in response_data["reactions"]
        assert "🎉" in response_data["reactions"]
        assert "custom_emoji" in response_data["reactions"]

    @patch('routes.reactions.reaction_manager')

    def test_response_structure_consistency(self, mock_reaction_manager, mock_reactions_data):
        """Test that response structure is consistent across different scenarios."""
        # Arrange
        message_id = "msg_structure_test"
        mock_reaction_manager.get_message_reactions.return_value = mock_reactions_data
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        response_data = json.loads(response.data)
        required_keys = ["success", "message_id", "reactions"]
        
        for key in required_keys:
            assert key in response_data, f"Missing required key: {key}"
        
        assert isinstance(response_data["success"], bool)
        assert response_data["message_id"] == message_id
        assert isinstance(response_data["reactions"], dict)

    @patch('routes.reactions.reaction_manager')

    def test_exception_with_empty_message(self, mock_reaction_manager):
        """Test exception handling when error message is empty."""
        # Arrange
        message_id = "msg_empty_error"
        mock_reaction_manager.get_message_reactions.side_effect = Exception("")
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Failed to get reactions: " in response_data["error"]

    @patch('routes.reactions.reaction_manager')

    def test_exception_with_special_characters_in_message(self, mock_reaction_manager):
        """Test exception handling with special characters in error message."""
        # Arrange
        message_id = "msg_special_error"
        error_message = "Error with special chars: àáâãäå æç èéêë ìíîï ñ òóôõö ùúûü ý"
        mock_reaction_manager.get_message_reactions.side_effect = Exception(error_message)
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get reactions: {error_message}" in response_data["error"]

# Standard library
# Third-party
# Local


import json
from unittest.mock import patch, Mock
import pytest
from flask import Flask

from routes.reactions import get_user_reactions

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app.config['TESTING'] = True
    return app

@pytest.fixture
def app_context(app):
    """Create application context for testing."""
    with app.app_context():
        yield app

@pytest.fixture
def request_context(app):
    """Create request context for testing."""
    with app.test_request_context():
        yield

@pytest.fixture
def mock_reaction_data():
    """Sample reaction data for testing."""
    return [
        {
            "id": 1,
            "message_id": 101,
            "user_id": 1,
            "reaction_type": "like",
            "created_at": "2023-01-01T10:00:00Z"
        },
        {
            "id": 2,
            "message_id": 102,
            "user_id": 1,
            "reaction_type": "love",
            "created_at": "2023-01-01T11:00:00Z"
        }
    ]

class TestGetUserReactions:
    """Test cases for get_user_reactions function."""

    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_success_no_message_filter(self, mock_reaction_manager, app, mock_reaction_data):
        """Test successful retrieval of user reactions without message filter."""
        mock_reaction_manager.get_user_reactions.return_value = mock_reaction_data
        
        with app.test_request_context('/?'):
            response, status_code = get_user_reactions(1)
            
            response_data = json.loads(response.data)
            
            assert status_code == 200
            assert response_data["success"] is True
            assert response_data["user_id"] == 1
            assert response_data["reactions"] == mock_reaction_data
            mock_reaction_manager.get_user_reactions.assert_called_once_with(1, None)

    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_success_with_message_filter(self, mock_reaction_manager, app, mock_reaction_data):
        """Test successful retrieval of user reactions with message filter."""
        filtered_data = [mock_reaction_data[0]]
        mock_reaction_manager.get_user_reactions.return_value = filtered_data
        
        with app.test_request_context('/?message_id=101'):
            response, status_code = get_user_reactions(1)
            
            response_data = json.loads(response.data)
            
            assert status_code == 200
            assert response_data["success"] is True
            assert response_data["user_id"] == 1
            assert response_data["reactions"] == filtered_data
            mock_reaction_manager.get_user_reactions.assert_called_once_with(1, 101)

    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_empty_results(self, mock_reaction_manager, app):
        """Test successful request with empty reaction results."""
        mock_reaction_manager.get_user_reactions.return_value = []
        
        with app.test_request_context('/?'):
            response, status_code = get_user_reactions(1)
            
            response_data = json.loads(response.data)
            
            assert status_code == 200
            assert response_data["success"] is True
            assert response_data["user_id"] == 1
            assert response_data["reactions"] == []
            mock_reaction_manager.get_user_reactions.assert_called_once_with(1, None)

    @pytest.mark.parametrize("user_id,message_id,expected_user_id", [
        (1, None, 1),
        (999, None, 999),
        (0, None, 0),
        (-1, None, -1),
        (1, 101, 1),
        (1, 0, 1),
        (1, -1, 1),
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_various_inputs(self, mock_reaction_manager, app, user_id, message_id, expected_user_id):
        """Test get_user_reactions with various user_id and message_id combinations."""
        mock_reaction_manager.get_user_reactions.return_value = []
        
        query_string = f'/?message_id={message_id}' if message_id is not None else '/?'
        
        with app.test_request_context(query_string):
            response, status_code = get_user_reactions(user_id)
            
            response_data = json.loads(response.data)
            
            assert status_code == 200
            assert response_data["success"] is True
            assert response_data["user_id"] == expected_user_id
            mock_reaction_manager.get_user_reactions.assert_called_once_with(user_id, message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_invalid_message_id_type(self, mock_reaction_manager, app):
        """Test get_user_reactions with invalid message_id type (should be ignored)."""
        mock_reaction_manager.get_user_reactions.return_value = []
        
        with app.test_request_context('/?message_id=invalid'):
            response, status_code = get_user_reactions(1)
            
            response_data = json.loads(response.data)
            
            assert status_code == 200
            assert response_data["success"] is True
            assert response_data["user_id"] == 1
            mock_reaction_manager.get_user_reactions.assert_called_once_with(1, None)

    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_reaction_manager_exception(self, mock_reaction_manager, app):
        """Test error handling when reaction_manager raises an exception."""
        error_message = "Database connection failed"
        mock_reaction_manager.get_user_reactions.side_effect = Exception(error_message)
        
        with app.test_request_context('/?'):
            response, status_code = get_user_reactions(1)
            
            response_data = json.loads(response.data)
            
            assert status_code == 500
            assert "error" in response_data
            assert f"Failed to get user reactions: {error_message}" in response_data["error"]
            mock_reaction_manager.get_user_reactions.assert_called_once_with(1, None)

    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_generic_exception(self, mock_reaction_manager, app):
        """Test error handling with generic exception."""
        mock_reaction_manager.get_user_reactions.side_effect = RuntimeError("Unexpected error")
        
        with app.test_request_context('/?message_id=101'):
            response, status_code = get_user_reactions(999)
            
            response_data = json.loads(response.data)
            
            assert status_code == 500
            assert "error" in response_data
            assert "Failed to get user reactions: Unexpected error" in response_data["error"]
            mock_reaction_manager.get_user_reactions.assert_called_once_with(999, 101)

    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_multiple_query_params(self, mock_reaction_manager, app):
        """Test get_user_reactions with multiple query parameters (only message_id should be used)."""
        mock_reaction_manager.get_user_reactions.return_value = []
        
        with app.test_request_context('/?message_id=101&other_param=value&limit=10'):
            response, status_code = get_user_reactions(1)
            
            response_data = json.loads(response.data)
            
            assert status_code == 200
            assert response_data["success"] is True
            # Only message_id should be extracted and used
            mock_reaction_manager.get_user_reactions.assert_called_once_with(1, 101)

    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_boundary_values(self, mock_reaction_manager, app):
        """Test get_user_reactions with boundary values."""
        mock_reaction_manager.get_user_reactions.return_value = []
        
        # Test with very large message_id
        with app.test_request_context('/?message_id=2147483647'):  # Max 32-bit int
            response, status_code = get_user_reactions(1)
            
            response_data = json.loads(response.data)
            
            assert status_code == 200
            assert response_data["success"] is True
            mock_reaction_manager.get_user_reactions.assert_called_once_with(1, 2147483647)

    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_response_structure(self, mock_reaction_manager, app, mock_reaction_data):
        """Test that response structure is correct and contains all required fields."""
        mock_reaction_manager.get_user_reactions.return_value = mock_reaction_data
        
        with app.test_request_context('/?'):
            response, status_code = get_user_reactions(42)
            
            response_data = json.loads(response.data)
            
            # Verify response structure
            assert isinstance(response_data, dict)
            assert set(response_data.keys()) == {"success", "user_id", "reactions"}
            assert response_data["success"] is True
            assert response_data["user_id"] == 42
            assert isinstance(response_data["reactions"], list)
            assert response_data["reactions"] == mock_reaction_data

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock

from routes.reactions import get_reaction_count

@pytest.fixture
def mock_reaction_manager(self):
        """Mock reaction_manager for testing."""
        with patch('routes.reactions.reaction_manager') as mock:
            yield mock

    @pytest.fixture
def mock_jsonify(self):
        """Mock jsonify for testing."""
        with patch('routes.reactions.jsonify') as mock:
            mock.side_effect = lambda x: (x, None)
            yield mock

class TestGetReactionCount:
    """Test cases for get_reaction_count function."""


    def test_successful_reaction_count_retrieval(self, mock_reaction_manager, mock_jsonify):
        """Test successful retrieval of reaction count."""
        # Arrange
        message_id = "msg_123"
        expected_count = 42
        mock_reaction_manager.get_reaction_count.return_value = expected_count
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "count": expected_count
        })

    @pytest.mark.parametrize("message_id,expected_count", [
        ("msg_001", 0),
        ("msg_002", 1),
        ("msg_003", 999),
        ("", 5),
        (None, 10),
        (123, 7),
        ("special-chars-!@#$%", 3)
    ])

    def test_various_message_ids_and_counts(self, message_id, expected_count, mock_reaction_manager, mock_jsonify):
        """Test reaction count retrieval with various message IDs and count values."""
        # Arrange
        mock_reaction_manager.get_reaction_count.return_value = expected_count
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "count": expected_count
        })


    def test_zero_reaction_count(self, mock_reaction_manager, mock_jsonify):
        """Test handling of zero reaction count."""
        # Arrange
        message_id = "msg_no_reactions"
        mock_reaction_manager.get_reaction_count.return_value = 0
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "count": 0
        })


    def test_negative_reaction_count(self, mock_reaction_manager, mock_jsonify):
        """Test handling of negative reaction count (edge case)."""
        # Arrange
        message_id = "msg_negative"
        mock_reaction_manager.get_reaction_count.return_value = -1
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "count": -1
        })

    @pytest.mark.parametrize("exception_type,exception_message", [
        (ValueError, "Invalid message ID"),
        (KeyError, "Message not found"),
        (ConnectionError, "Database connection failed"),
        (TimeoutError, "Request timeout"),
        (RuntimeError, "Unexpected error occurred"),
        (Exception, "Generic exception")
    ])

    def test_exception_handling(self, exception_type, exception_message, mock_reaction_manager, mock_jsonify):
        """Test exception handling for various error types."""
        # Arrange
        message_id = "msg_error"
        mock_reaction_manager.get_reaction_count.side_effect = exception_type(exception_message)
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        mock_reaction_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get reaction count: {exception_message}"
        })


    def test_exception_with_empty_message(self, mock_reaction_manager, mock_jsonify):
        """Test exception handling when exception has empty message."""
        # Arrange
        message_id = "msg_empty_error"
        mock_reaction_manager.get_reaction_count.side_effect = Exception("")
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        mock_reaction_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": "Failed to get reaction count: "
        })


    def test_exception_with_none_message(self, mock_reaction_manager, mock_jsonify):
        """Test exception handling when exception message is None."""
        # Arrange
        message_id = "msg_none_error"
        mock_reaction_manager.get_reaction_count.side_effect = Exception(None)
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        mock_reaction_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": "Failed to get reaction count: None"
        })


    def test_large_reaction_count(self, mock_reaction_manager, mock_jsonify):
        """Test handling of very large reaction count."""
        # Arrange
        message_id = "msg_viral"
        large_count = 999999999
        mock_reaction_manager.get_reaction_count.return_value = large_count
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "count": large_count
        })


    def test_reaction_manager_called_with_correct_parameter(self, mock_reaction_manager, mock_jsonify):
        """Test that reaction_manager.get_reaction_count is called with the correct parameter."""
        # Arrange
        message_id = "test_message_id_123"
        mock_reaction_manager.get_reaction_count.return_value = 15
        
        # Act
        get_reaction_count(message_id)
        
        # Assert
        mock_reaction_manager.get_reaction_count.assert_called_once_with(message_id)


    def test_jsonify_response_structure_success(self, mock_reaction_manager, mock_jsonify):
        """Test that jsonify is called with correct response structure for success case."""
        # Arrange
        message_id = "msg_structure_test"
        count = 25
        mock_reaction_manager.get_reaction_count.return_value = count
        
        # Act
        get_reaction_count(message_id)
        
        # Assert
        expected_response = {
            "success": True,
            "message_id": message_id,
            "count": count
        }
        mock_jsonify.assert_called_once_with(expected_response)


    def test_jsonify_response_structure_error(self, mock_reaction_manager, mock_jsonify):
        """Test that jsonify is called with correct response structure for error case."""
        # Arrange
        message_id = "msg_error_structure"
        error_message = "Test error message"
        mock_reaction_manager.get_reaction_count.side_effect = Exception(error_message)
        
        # Act
        get_reaction_count(message_id)
        
        # Assert
        expected_response = {
            "error": f"Failed to get reaction count: {error_message}"
        }
        mock_jsonify.assert_called_once_with(expected_response)

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock

from routes.reactions import get_most_popular

@pytest.fixture
def mock_reaction_manager(self):
        """Mock reaction_manager for testing."""
        with patch('routes.reactions.reaction_manager') as mock:
            yield mock

    @pytest.fixture
def mock_jsonify(self):
        """Mock jsonify for testing."""
        with patch('routes.reactions.jsonify') as mock:
            mock.side_effect = lambda x: (x, None)
            yield mock

class TestGetMostPopular:
    """Test cases for get_most_popular function."""


    def test_successful_emoji_retrieval(self, mock_reaction_manager, mock_jsonify):
        """Test successful retrieval of most popular emoji."""
        # Arrange
        message_id = "msg_123"
        expected_emoji = "👍"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })

    @pytest.mark.parametrize("message_id,expected_emoji", [
        ("msg_001", "😂"),
        ("msg_999", "❤️"),
        ("", "🎉"),
        ("special-chars-123!@#", "🔥"),
        ("very_long_message_id_with_many_characters_12345", "⭐"),
    ])

    def test_various_message_ids_and_emojis(self, message_id, expected_emoji, mock_reaction_manager, mock_jsonify):
        """Test function with various message IDs and emoji responses."""
        # Arrange
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })


    def test_none_message_id(self, mock_reaction_manager, mock_jsonify):
        """Test function with None message_id."""
        # Arrange
        message_id = None
        expected_emoji = "👍"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })


    def test_empty_emoji_response(self, mock_reaction_manager, mock_jsonify):
        """Test function when reaction_manager returns empty/None emoji."""
        # Arrange
        message_id = "msg_123"
        expected_emoji = None
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })

    @pytest.mark.parametrize("exception_type,exception_message", [
        (ValueError, "Invalid message ID"),
        (KeyError, "Message not found"),
        (ConnectionError, "Database connection failed"),
        (RuntimeError, "Service unavailable"),
        (Exception, "Generic error occurred"),
    ])

    def test_exception_handling(self, exception_type, exception_message, mock_reaction_manager, mock_jsonify):
        """Test exception handling for various error types."""
        # Arrange
        message_id = "msg_123"
        mock_reaction_manager.get_most_popular_emoji.side_effect = exception_type(exception_message)
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 500
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get popular emoji: {exception_message}"
        })


    def test_reaction_manager_method_not_called_on_exception(self, mock_reaction_manager, mock_jsonify):
        """Test that reaction_manager method is called even when it raises exception."""
        # Arrange
        message_id = "msg_123"
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("Test error")
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 500
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)


    def test_jsonify_called_with_correct_error_format(self, mock_reaction_manager, mock_jsonify):
        """Test that jsonify is called with correct error format on exception."""
        # Arrange
        message_id = "msg_123"
        error_message = "Custom error message"
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception(error_message)
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 500
        expected_error_dict = {"error": f"Failed to get popular emoji: {error_message}"}
        mock_jsonify.assert_called_once_with(expected_error_dict)


    def test_numeric_message_id(self, mock_reaction_manager, mock_jsonify):
        """Test function with numeric message ID."""
        # Arrange
        message_id = 12345
        expected_emoji = "🚀"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })


    def test_boolean_message_id(self, mock_reaction_manager, mock_jsonify):
        """Test function with boolean message ID."""
        # Arrange
        message_id = True
        expected_emoji = "✅"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })


    def test_exception_with_empty_message(self, mock_reaction_manager, mock_jsonify):
        """Test exception handling when exception has empty message."""
        # Arrange
        message_id = "msg_123"
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("")
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 500
        mock_jsonify.assert_called_once_with({
            "error": "Failed to get popular emoji: "
        })


    def test_unicode_emoji_response(self, mock_reaction_manager, mock_jsonify):
        """Test function with various unicode emoji responses."""
        # Arrange
        message_id = "msg_unicode"
        expected_emoji = "🎭🎪🎨"  # Multiple emojis
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock

from routes.reactions import get_allowed_emojis

class TestGetAllowedEmojis:
    """Test cases for get_allowed_emojis function."""

    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.ReactionManager')

    def test_get_allowed_emojis_success(self, mock_reaction_manager, mock_jsonify):
        """Test successful retrieval of allowed emojis."""
        # Arrange
        expected_emojis = ['👍', '👎', '❤️', '😂', '😮', '😢', '😡']
        mock_reaction_manager.get_allowed_emojis.return_value = expected_emojis
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        assert result == mock_response
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": expected_emojis
        })

    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.ReactionManager')

    def test_get_allowed_emojis_empty_list(self, mock_reaction_manager, mock_jsonify):
        """Test when ReactionManager returns empty emoji list."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.return_value = []
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        assert result == mock_response
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": []
        })

    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.ReactionManager')

    def test_get_allowed_emojis_none_return(self, mock_reaction_manager, mock_jsonify):
        """Test when ReactionManager returns None."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.return_value = None
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        assert result == mock_response
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": None
        })

    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.ReactionManager')

    def test_get_allowed_emojis_large_list(self, mock_reaction_manager, mock_jsonify):
        """Test with large emoji list to verify no size limitations."""
        # Arrange
        large_emoji_list = ['😀'] * 1000  # Large list of emojis
        mock_reaction_manager.get_allowed_emojis.return_value = large_emoji_list
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        assert result == mock_response
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": large_emoji_list
        })

    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.ReactionManager')

    def test_get_allowed_emojis_reaction_manager_exception(self, mock_reaction_manager, mock_jsonify):
        """Test when ReactionManager.get_allowed_emojis raises an exception."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            get_allowed_emojis()
        
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_not_called()

    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.ReactionManager')

    def test_get_allowed_emojis_jsonify_exception(self, mock_reaction_manager, mock_jsonify):
        """Test when jsonify raises an exception."""
        # Arrange
        expected_emojis = ['👍', '👎']
        mock_reaction_manager.get_allowed_emojis.return_value = expected_emojis
        mock_jsonify.side_effect = Exception("JSON serialization error")
        
        # Act & Assert
        with pytest.raises(Exception, match="JSON serialization error"):
            get_allowed_emojis()
        
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": expected_emojis
        })

    @pytest.mark.parametrize("emoji_data,expected_success", [
        (['👍', '👎', '❤️'], True),
        (['🎉', '🔥', '💯', '✨'], True),
        (['😀', '😃', '😄', '😁', '😆'], True),
        ([], True),
        (None, True),
    ])
    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.ReactionManager')

    def test_get_allowed_emojis_various_data_types(self, mock_reaction_manager, mock_jsonify, emoji_data, expected_success):
        """Test function with various emoji data types and contents."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.return_value = emoji_data
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        assert result == mock_response
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": expected_success,
            "emojis": emoji_data
        })

    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.ReactionManager')

    def test_get_allowed_emojis_response_structure(self, mock_reaction_manager, mock_jsonify):
        """Test that response structure is always consistent."""
        # Arrange
        test_emojis = ['👍', '❤️']
        mock_reaction_manager.get_allowed_emojis.return_value = test_emojis
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        mock_jsonify.assert_called_once()
        
        # Verify the structure of the JSON response
        call_args = mock_jsonify.call_args[0][0]
        assert "success" in call_args
        assert "emojis" in call_args
        assert call_args["success"] is True
        assert call_args["emojis"] == test_emojis
        assert len(call_args) == 2  # Only success and emojis keys

    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.ReactionManager')

    def test_get_allowed_emojis_unicode_handling(self, mock_reaction_manager, mock_jsonify):
        """Test handling of various Unicode emoji formats."""
        # Arrange
        unicode_emojis = [
            '👍',  # Standard emoji
            '👨‍💻',  # Compound emoji with ZWJ
            '🏳️‍🌈',  # Flag with variation selector
            '🤷🏽‍♀️',  # Emoji with skin tone and gender
        ]
        mock_reaction_manager.get_allowed_emojis.return_value = unicode_emojis
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        assert result == mock_response
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": unicode_emojis
        })

# Standard library
# Third-party
# Local


import json
import pytest
from flask import Flask
from unittest.mock import patch, Mock

from routes.reactions import bulk_add_reactions

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def app_context(app):
    """Create application context."""
    with app.app_context():
        yield app

@pytest.fixture
def request_context(app):
    """Create request context."""
    with app.test_request_context():
        yield

@pytest.fixture
def valid_reactions_data():
    """Valid reactions data for testing."""
    return {
        "reactions": [
            {"message_id": 1, "user_id": 123, "emoji": "👍"},
            {"message_id": 2, "user_id": 123, "emoji": "❤️"},
            {"message_id": 3, "user_id": 123, "emoji": "😂"}
        ]
    }

@pytest.fixture
def bulk_add_result():
    """Mock result from reaction_manager.bulk_add_reactions."""
    return {
        "added": 3,
        "failed": 0,
        "details": [
            {"message_id": 1, "status": "success"},
            {"message_id": 2, "status": "success"},
            {"message_id": 3, "status": "success"}
        ]
    }

class TestBulkAddReactions:
    """Test cases for bulk_add_reactions function."""

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')
    def test_successful_bulk_add_reactions(self, mock_request, mock_reaction_manager, 
                                         valid_reactions_data, bulk_add_result, app_context):
        """Test successful bulk addition of reactions."""
        # Arrange
        mock_request.get_json.return_value = valid_reactions_data
        mock_reaction_manager.bulk_add_reactions.return_value = bulk_add_result
        
        # Act
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["result"] == bulk_add_result
        mock_reaction_manager.bulk_add_reactions.assert_called_once_with(valid_reactions_data["reactions"])

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "reactions array is required"),
        ({}, "reactions array is required"),
        ({"other_field": "value"}, "reactions array is required"),
        ({"reactions": None}, "reactions array is required"),
    ])
    @patch('routes.reactions.request')

    def test_invalid_request_data(self, mock_request, request_data, expected_error, app_context):
        """Test handling of invalid request data."""
        # Arrange
        mock_request.get_json.return_value = request_data
        
        # Act
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data["error"] == expected_error

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_empty_reactions_array(self, mock_request, mock_reaction_manager, app_context):
        """Test handling of empty reactions array."""
        # Arrange
        empty_data = {"reactions": []}
        mock_request.get_json.return_value = empty_data
        mock_reaction_manager.bulk_add_reactions.return_value = {"added": 0, "failed": 0, "details": []}
        
        # Act
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        mock_reaction_manager.bulk_add_reactions.assert_called_once_with([])

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_large_reactions_array(self, mock_request, mock_reaction_manager, app_context):
        """Test handling of large reactions array."""
        # Arrange
        large_reactions = {
            "reactions": [
                {"message_id": i, "user_id": 123, "emoji": "👍"} 
                for i in range(1000)
            ]
        }
        mock_request.get_json.return_value = large_reactions
        mock_reaction_manager.bulk_add_reactions.return_value = {"added": 1000, "failed": 0}
        
        # Act
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        mock_reaction_manager.bulk_add_reactions.assert_called_once_with(large_reactions["reactions"])

    @pytest.mark.parametrize("exception_type,exception_message", [
        (ValueError, "Invalid reaction data"),
        (KeyError, "Missing required field"),
        (RuntimeError, "Database connection failed"),
        (Exception, "Unexpected error occurred"),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')
    def test_reaction_manager_exceptions(self, mock_request, mock_reaction_manager, 
                                       exception_type, exception_message, 
                                       valid_reactions_data, app_context):
        """Test handling of various exceptions from reaction_manager."""
        # Arrange
        mock_request.get_json.return_value = valid_reactions_data
        mock_reaction_manager.bulk_add_reactions.side_effect = exception_type(exception_message)
        
        # Act
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert response_data["error"] == f"Failed to bulk add reactions: {exception_message}"

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_malformed_reaction_data(self, mock_request, mock_reaction_manager, app_context):
        """Test handling of malformed reaction data."""
        # Arrange
        malformed_data = {
            "reactions": [
                {"message_id": "invalid", "user_id": 123, "emoji": "👍"},
                {"message_id": 2, "user_id": "invalid", "emoji": "❤️"},
                {"message_id": 3, "user_id": 123, "emoji": ""}
            ]
        }
        mock_request.get_json.return_value = malformed_data
        mock_reaction_manager.bulk_add_reactions.side_effect = ValueError("Invalid data types")
        
        # Act
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "Failed to bulk add reactions: Invalid data types" in response_data["error"]

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')
    def test_partial_success_scenario(self, mock_request, mock_reaction_manager, 
                                    valid_reactions_data, app_context):
        """Test scenario where some reactions succeed and some fail."""
        # Arrange
        partial_result = {
            "added": 2,
            "failed": 1,
            "details": [
                {"message_id": 1, "status": "success"},
                {"message_id": 2, "status": "success"},
                {"message_id": 3, "status": "failed", "error": "Message not found"}
            ]
        }
        mock_request.get_json.return_value = valid_reactions_data
        mock_reaction_manager.bulk_add_reactions.return_value = partial_result
        
        # Act
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["result"]["added"] == 2
        assert response_data["result"]["failed"] == 1

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')
    def test_user_id_parameter_ignored(self, mock_request, mock_reaction_manager, 
                                     valid_reactions_data, bulk_add_result, app_context):
        """Test that user_id parameter is ignored (reactions contain their own user_ids)."""
        # Arrange
        mock_request.get_json.return_value = valid_reactions_data
        mock_reaction_manager.bulk_add_reactions.return_value = bulk_add_result
        
        # Act - Test with different user_id values
        response1, status1 = bulk_add_reactions(123)
        response2, status2 = bulk_add_reactions(999)
        response3, status3 = bulk_add_reactions(None)
        
        # Assert - All should behave identically
        assert status1 == status2 == status3 == 200
        assert mock_reaction_manager.bulk_add_reactions.call_count == 3
        
        # Verify the same reactions data was passed each time
        for call in mock_reaction_manager.bulk_add_reactions.call_args_list:
            assert call[0][0] == valid_reactions_data["reactions"]

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_unicode_emoji_handling(self, mock_request, mock_reaction_manager, app_context):
        """Test handling of various Unicode emoji characters."""
        # Arrange
        unicode_data = {
            "reactions": [
                {"message_id": 1, "user_id": 123, "emoji": "🎉"},
                {"message_id": 2, "user_id": 123, "emoji": "🚀"},
                {"message_id": 3, "user_id": 123, "emoji": "💯"},
                {"message_id": 4, "user_id": 123, "emoji": "🔥"},
            ]
        }
        mock_request.get_json.return_value = unicode_data
        mock_reaction_manager.bulk_add_reactions.return_value = {"added": 4, "failed": 0}
        
        # Act
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        mock_reaction_manager.bulk_add_reactions.assert_called_once_with(unicode_data["reactions"])

# Standard library
# Third-party
# Local


from unittest.mock import Mock, patch
import pytest
from flask import Flask, request, jsonify

from routes.reactions import decorated_function

@pytest.fixture
def app():
    """Create Flask app for testing."""
    try:
from routes.reactions import app as flask_app
    except ImportError:
        # Fallback for different app structures
from flask import Flask
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def mock_flask_app():
    """Create a Flask app for testing context."""
    return app

@pytest.fixture
def mock_function():
    """Create a mock function to be decorated."""
    return Mock(return_value={"success": True, "data": "test_result"})

class TestDecoratedFunction:
    """Test suite for the decorated_function authentication decorator."""

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_authentication_with_header_user_id(self, mock_jsonify, mock_request, mock_function):
        """Test successful authentication using X-User-ID header."""
        # Arrange
        mock_request.headers.get.return_value = "123"
        mock_request.args.get.return_value = None
        expected_result = {"success": True, "data": "test_result"}
        mock_function.return_value = expected_result
        
        # Act
        result = decorated_function(mock_function, "arg1", "arg2", kwarg1="value1")
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_function.assert_called_once_with("arg1", "arg2", user_id=123, kwarg1="value1")
        assert result == expected_result
        mock_jsonify.assert_not_called()

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_authentication_with_query_param_user_id(self, mock_jsonify, mock_request, mock_function):
        """Test successful authentication using user_id query parameter."""
        # Arrange
        mock_request.headers.get.return_value = None
        mock_request.args.get.return_value = "456"
        expected_result = {"success": True, "data": "test_result"}
        mock_function.return_value = expected_result
        
        # Act
        result = decorated_function(mock_function, test_arg="test_value")
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_request.args.get.assert_called_once_with('user_id')
        mock_function.assert_called_once_with(user_id=456, test_arg="test_value")
        assert result == expected_result
        mock_jsonify.assert_not_called()

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_authentication_header_takes_precedence(self, mock_jsonify, mock_request, mock_function):
        """Test that X-User-ID header takes precedence over query parameter."""
        # Arrange
        mock_request.headers.get.return_value = "789"
        mock_request.args.get.return_value = "999"
        expected_result = {"success": True, "data": "test_result"}
        mock_function.return_value = expected_result
        
        # Act
        result = decorated_function(mock_function)
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_function.assert_called_once_with(user_id=789)
        assert result == expected_result
        mock_jsonify.assert_not_called()

    @pytest.mark.parametrize("header_value,query_value", [
        (None, None),
        ("", None),
        (None, ""),
        ("", ""),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_authentication_required_error(self, mock_jsonify, mock_request, mock_function, header_value, query_value):
        """Test authentication error when no user_id is provided."""
        # Arrange
        mock_request.headers.get.return_value = header_value
        mock_request.args.get.return_value = query_value
        mock_jsonify.return_value = {"error": "Authentication required"}
        
        # Act
        result = decorated_function(mock_function, "test_arg")
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        if not header_value:
            mock_request.args.get.assert_called_once_with('user_id')
        mock_jsonify.assert_called_once_with({"error": "Authentication required"})
        mock_function.assert_not_called()
        assert result == ({"error": "Authentication required"}, 401)

    @pytest.mark.parametrize("user_id_value,expected_int", [
        ("1", 1),
        ("0", 0),
        ("999999", 999999),
        ("-1", -1),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_user_id_conversion_to_int(self, mock_jsonify, mock_request, mock_function, user_id_value, expected_int):
        """Test that user_id is properly converted to integer."""
        # Arrange
        mock_request.headers.get.return_value = user_id_value
        mock_request.args.get.return_value = None
        expected_result = {"success": True}
        mock_function.return_value = expected_result
        
        # Act
        result = decorated_function(mock_function)
        
        # Assert
        mock_function.assert_called_once_with(user_id=expected_int)
        assert result == expected_result

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_invalid_user_id_conversion_raises_error(self, mock_jsonify, mock_request, mock_function):
        """Test that invalid user_id values raise ValueError during int conversion."""
        # Arrange
        mock_request.headers.get.return_value = "invalid_id"
        mock_request.args.get.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError):
            decorated_function(mock_function)
        
        mock_function.assert_not_called()

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_function_args_and_kwargs_preservation(self, mock_jsonify, mock_request, mock_function):
        """Test that original function arguments and keyword arguments are preserved."""
        # Arrange
        mock_request.headers.get.return_value = "100"
        mock_request.args.get.return_value = None
        expected_result = {"data": "processed"}
        mock_function.return_value = expected_result
        
        # Act
        result = decorated_function(
            mock_function,
            "pos_arg1", 
            "pos_arg2", 
            keyword_arg="keyword_value",
            another_kwarg=42
        )
        
        # Assert
        mock_function.assert_called_once_with(
            "pos_arg1",
            "pos_arg2",
            user_id=100,
            keyword_arg="keyword_value",
            another_kwarg=42
        )
        assert result == expected_result

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_function_exception_propagation(self, mock_jsonify, mock_request, mock_function):
        """Test that exceptions from the decorated function are properly propagated."""
        # Arrange
        mock_request.headers.get.return_value = "200"
        mock_request.args.get.return_value = None
        mock_function.side_effect = RuntimeError("Function error")
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="Function error"):
            decorated_function(mock_function)

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_no_arguments_passed_to_function(self, mock_jsonify, mock_request, mock_function):
        """Test decorated function works with no arguments passed."""
        # Arrange
        mock_request.headers.get.return_value = "300"
        mock_request.args.get.return_value = None
        expected_result = {"empty": "result"}
        mock_function.return_value = expected_result
        
        # Act
        result = decorated_function(mock_function)
        
        # Assert
        mock_function.assert_called_once_with(user_id=300)
        assert result == expected_result

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_user_id_boundary_values(self, mock_jsonify, mock_request, mock_function):
        """Test boundary values for user_id conversion."""
        # Test with maximum integer value
        mock_request.headers.get.return_value = str(2**31 - 1)
        mock_request.args.get.return_value = None
        mock_function.return_value = {"result": "success"}
        
        result = decorated_function(mock_function)
        
        mock_function.assert_called_once_with(user_id=2**31 - 1)
        assert result == {"result": "success"}

# Standard library
# Third-party
# Local

