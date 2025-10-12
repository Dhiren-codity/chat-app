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
    test_app.config['TESTING'] = True
    return test_app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def mock_function():
    """Create mock function to be decorated."""
    mock_func = Mock()
    mock_func.__name__ = 'test_function'
    mock_func.return_value = {'success': True}
    return mock_func

class TestRequireAuth:
    """Test cases for require_auth decorator."""

    @patch('routes.reactions.request')

    def test_auth_with_header_user_id(self, mock_request, mock_function):
        """Test authentication with user ID in headers."""
        # Setup
        mock_request.headers.get.return_value = '123'
        mock_request.args.get.return_value = None
        
        # Apply decorator
        decorated_func = require_auth(mock_function)
        
        # Execute
        result = decorated_func('arg1', kwarg1='value1')
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_function.assert_called_once_with('arg1', user_id=123, kwarg1='value1')
        assert result == {'success': True}

    @patch('routes.reactions.request')

    def test_auth_with_query_param_user_id(self, mock_request, mock_function):
        """Test authentication with user ID in query parameters."""
        # Setup
        mock_request.headers.get.return_value = None
        mock_request.args.get.return_value = '456'
        
        # Apply decorator
        decorated_func = require_auth(mock_function)
        
        # Execute
        result = decorated_func('arg1', kwarg1='value1')
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_request.args.get.assert_called_once_with('user_id')
        mock_function.assert_called_once_with('arg1', user_id=456, kwarg1='value1')
        assert result == {'success': True}

    @patch('routes.reactions.request')

    def test_header_takes_precedence_over_query_param(self, mock_request, mock_function):
        """Test that header user ID takes precedence over query parameter."""
        # Setup
        mock_request.headers.get.return_value = '789'
        mock_request.args.get.return_value = '999'
        
        # Apply decorator
        decorated_func = require_auth(mock_function)
        
        # Execute
        result = decorated_func()
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_request.args.get.assert_not_called()
        mock_function.assert_called_once_with(user_id=789)
        assert result == {'success': True}

    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.request')

    def test_no_authentication_returns_401(self, mock_request, mock_jsonify, mock_function):
        """Test that missing authentication returns 401 error."""
        # Setup
        mock_request.headers.get.return_value = None
        mock_request.args.get.return_value = None
        mock_jsonify.return_value = {"error": "Authentication required"}
        
        # Apply decorator
        decorated_func = require_auth(mock_function)
        
        # Execute
        result, status_code = decorated_func()
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_request.args.get.assert_called_once_with('user_id')
        mock_jsonify.assert_called_once_with({"error": "Authentication required"})
        mock_function.assert_not_called()
        assert result == {"error": "Authentication required"}
        assert status_code == 401

    @pytest.mark.parametrize("user_id_value,expected_int", [
        ('1', 1),
        ('0', 0),
        ('999999', 999999),
        ('-1', -1),
    ])
    @patch('routes.reactions.request')

    def test_user_id_conversion_to_int(self, mock_request, mock_function, user_id_value, expected_int):
        """Test that user ID is properly converted to integer."""
        # Setup
        mock_request.headers.get.return_value = user_id_value
        mock_request.args.get.return_value = None
        
        # Apply decorator
        decorated_func = require_auth(mock_function)
        
        # Execute
        decorated_func()
        
        # Assert
        mock_function.assert_called_once_with(user_id=expected_int)

    @pytest.mark.parametrize("empty_value", [
        '',
        '   ',
        None,
    ])
    @patch('routes.reactions.jsonify')
    @patch('routes.reactions.request')

    def test_empty_user_id_values_return_401(self, mock_request, mock_jsonify, mock_function, empty_value):
        """Test that empty or whitespace user ID values return 401."""
        # Setup
        mock_request.headers.get.return_value = empty_value
        mock_request.args.get.return_value = empty_value
        mock_jsonify.return_value = {"error": "Authentication required"}
        
        # Apply decorator
        decorated_func = require_auth(mock_function)
        
        # Execute
        result, status_code = decorated_func()
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "Authentication required"})
        mock_function.assert_not_called()
        assert status_code == 401

    @patch('routes.reactions.request')

    def test_decorator_preserves_function_metadata(self, mock_request, app):
        """Test that decorator preserves original function metadata."""
        # Setup
        mock_request.headers.get.return_value = '123'
        
        def original_function():
            """Original function docstring."""
            return "original"
        
        # Apply decorator
        decorated_func = require_auth(original_function)
        
        # Assert metadata is preserved
        assert decorated_func.__name__ == 'original_function'
        assert decorated_func.__doc__ == 'Original function docstring.'

    @patch('routes.reactions.request')

    def test_function_with_no_args_or_kwargs(self, mock_request, mock_function):
        """Test decorator works with function that has no arguments."""
        # Setup
        mock_request.headers.get.return_value = '555'
        mock_request.args.get.return_value = None
        
        # Apply decorator
        decorated_func = require_auth(mock_function)
        
        # Execute
        result = decorated_func()
        
        # Assert
        mock_function.assert_called_once_with(user_id=555)
        assert result == {'success': True}

    @patch('routes.reactions.request')

    def test_function_with_mixed_args_and_kwargs(self, mock_request, mock_function):
        """Test decorator works with function that has mixed arguments."""
        # Setup
        mock_request.headers.get.return_value = '777'
        mock_request.args.get.return_value = None
        
        # Apply decorator
        decorated_func = require_auth(mock_function)
        
        # Execute
        result = decorated_func('pos1', 'pos2', kw1='val1', kw2='val2')
        
        # Assert
        mock_function.assert_called_once_with('pos1', 'pos2', user_id=777, kw1='val1', kw2='val2')
        assert result == {'success': True}

    @patch('routes.reactions.request')

    def test_user_id_conversion_error_handling(self, mock_request, mock_function):
        """Test handling of invalid user ID that cannot be converted to int."""
        # Setup
        mock_request.headers.get.return_value = 'invalid_number'
        mock_request.args.get.return_value = None
        
        # Apply decorator
        decorated_func = require_auth(mock_function)
        
        # Execute and assert ValueError is raised
        with pytest.raises(ValueError):
            decorated_func()
        
        # Assert original function was not called
        mock_function.assert_not_called()

    @patch('routes.reactions.request')

    def test_decorated_function_exception_propagation(self, mock_request, mock_function):
        """Test that exceptions from decorated function are properly propagated."""
        # Setup
        mock_request.headers.get.return_value = '888'
        mock_request.args.get.return_value = None
        mock_function.side_effect = RuntimeError("Function error")
        
        # Apply decorator
        decorated_func = require_auth(mock_function)
        
        # Execute and assert exception is propagated
        with pytest.raises(RuntimeError, match="Function error"):
            decorated_func()
        
        # Assert function was called with correct user_id
        mock_function.assert_called_once_with(user_id=888)

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
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def mock_reaction_manager():
    """Mock reaction manager."""
    return Mock()

@pytest.fixture
def valid_request_data():
    """Valid request data for testing."""
    return {
        "message_id": 123,
        "emoji": "👍"
    }

@pytest.fixture
def success_response():
    """Successful reaction manager response."""
    return {"success": True, "reaction_id": 456}

@pytest.fixture
def failure_response():
    """Failed reaction manager response."""
    return {"success": False, "error": "Reaction already exists"}

class TestAddReaction:
    """Test cases for add_reaction function."""

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_success(self, mock_manager, mock_request, valid_request_data, success_response):
        """Test successful reaction addition."""
        # Arrange
        user_id = 789
        mock_request.get_json.return_value = valid_request_data
        mock_manager.add_reaction.return_value = success_response
        
        # Act
        response, status_code = add_reaction(user_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data == success_response
        mock_manager.add_reaction.assert_called_once_with(
            message_id=123,
            user_id=789,
            emoji="👍"
        )

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_manager_failure(self, mock_manager, mock_request, valid_request_data, failure_response):
        """Test reaction manager returns failure."""
        # Arrange
        user_id = 789
        mock_request.get_json.return_value = valid_request_data
        mock_manager.add_reaction.return_value = failure_response
        
        # Act
        response, status_code = add_reaction(user_id)
        
        # Assert
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data == failure_response

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "message_id and emoji are required"),
        ({}, "message_id and emoji are required"),
        ({"message_id": 123}, "message_id and emoji are required"),
        ({"emoji": "👍"}, "message_id and emoji are required"),
        ({"message_id": 123, "other_field": "value"}, "message_id and emoji are required"),
    ])
    @patch('routes.reactions.request')

    def test_add_reaction_invalid_request_data(self, mock_request, request_data, expected_error):
        """Test various invalid request data scenarios."""
        # Arrange
        user_id = 789
        mock_request.get_json.return_value = request_data
        
        # Act
        response, status_code = add_reaction(user_id)
        
        # Assert
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data["error"] == expected_error

    @pytest.mark.parametrize("message_id,emoji", [
        (0, "👍"),
        (-1, "👎"),
        (999999999, "❤️"),
        (123, ""),
        (123, "🎉🎊"),
        (123, "custom_emoji"),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_boundary_values(self, mock_manager, mock_request, message_id, emoji, success_response):
        """Test boundary and edge values for message_id and emoji."""
        # Arrange
        user_id = 789
        request_data = {"message_id": message_id, "emoji": emoji}
        mock_request.get_json.return_value = request_data
        mock_manager.add_reaction.return_value = success_response
        
        # Act
        response, status_code = add_reaction(user_id)
        
        # Assert
        assert status_code == 200
        mock_manager.add_reaction.assert_called_once_with(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        )

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_value_error(self, mock_manager, mock_request, valid_request_data):
        """Test ValueError handling from reaction manager."""
        # Arrange
        user_id = 789
        error_message = "Invalid message ID"
        mock_request.get_json.return_value = valid_request_data
        mock_manager.add_reaction.side_effect = ValueError(error_message)
        
        # Act
        response, status_code = add_reaction(user_id)
        
        # Assert
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data["error"] == error_message

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_generic_exception(self, mock_manager, mock_request, valid_request_data):
        """Test generic exception handling from reaction manager."""
        # Arrange
        user_id = 789
        error_message = "Database connection failed"
        mock_request.get_json.return_value = valid_request_data
        mock_manager.add_reaction.side_effect = Exception(error_message)
        
        # Act
        response, status_code = add_reaction(user_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert response_data["error"] == f"Failed to add reaction: {error_message}"

    @pytest.mark.parametrize("user_id", [
        0,
        -1,
        999999999,
        None,
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_various_user_ids(self, mock_manager, mock_request, user_id, valid_request_data, success_response):
        """Test various user_id values including edge cases."""
        # Arrange
        mock_request.get_json.return_value = valid_request_data
        mock_manager.add_reaction.return_value = success_response
        
        # Act
        response, status_code = add_reaction(user_id)
        
        # Assert
        assert status_code == 200
        mock_manager.add_reaction.assert_called_once_with(
            message_id=123,
            user_id=user_id,
            emoji="👍"
        )

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_request_json_exception(self, mock_manager, mock_request):
        """Test exception when getting JSON from request."""
        # Arrange
        user_id = 789
        mock_request.get_json.side_effect = Exception("Invalid JSON")
        
        # Act
        response, status_code = add_reaction(user_id)
        
        # Assert
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data["error"] == "message_id and emoji are required"

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_complex_emoji_strings(self, mock_manager, mock_request, success_response):
        """Test complex emoji strings and Unicode characters."""
        # Arrange
        user_id = 789
        test_cases = [
            "👨‍👩‍👧‍👦",  # Family emoji
            "🏳️‍🌈",        # Flag emoji
            "🧑🏽‍💻",       # Person with skin tone
            "😀😃😄",       # Multiple emojis
            "🔥💯✨",       # Mixed emojis
        ]
        
        for emoji in test_cases:
            request_data = {"message_id": 123, "emoji": emoji}
            mock_request.get_json.return_value = request_data
            mock_manager.add_reaction.return_value = success_response
            
            # Act
            response, status_code = add_reaction(user_id)
            
            # Assert
            assert status_code == 200
            mock_manager.add_reaction.assert_called_with(
                message_id=123,
                user_id=user_id,
                emoji=emoji
            )
        
        # Verify all calls were made
        assert mock_manager.add_reaction.call_count == len(test_cases)

# Standard library
# Third-party
# Local


import json
from unittest.mock import Mock, patch
import pytest
from flask import Flask

from routes.reactions import remove_reaction

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
def mock_reaction_manager():
    """Mock reaction manager."""
    return Mock()

@pytest.fixture
def valid_request_data():
    """Valid request data for testing."""
    return {
        "message_id": 123,
        "emoji": "👍"
    }

@pytest.fixture
def success_response():
    """Successful reaction manager response."""
    return {"success": True, "message": "Reaction removed successfully"}

@pytest.fixture
def failure_response():
    """Failed reaction manager response."""
    return {"success": False, "message": "Reaction not found"}

class TestRemoveReaction:
    """Test cases for remove_reaction function."""

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_success(self, mock_request, mock_manager, valid_request_data, success_response):
        """Test successful reaction removal."""
        # Arrange
        mock_request.get_json.return_value = valid_request_data
        mock_manager.remove_reaction.return_value = success_response
        user_id = 456
        
        # Act
        response, status_code = remove_reaction(user_id)
        
        # Assert
        assert status_code == 200
        assert response.json == success_response
        mock_manager.remove_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji="👍"
        )

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_not_found(self, mock_request, mock_manager, valid_request_data, failure_response):
        """Test reaction removal when reaction not found."""
        # Arrange
        mock_request.get_json.return_value = valid_request_data
        mock_manager.remove_reaction.return_value = failure_response
        user_id = 456
        
        # Act
        response, status_code = remove_reaction(user_id)
        
        # Assert
        assert status_code == 404
        assert response.json == failure_response
        mock_manager.remove_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
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

    def test_remove_reaction_invalid_request_data(self, mock_request, request_data, expected_error):
        """Test reaction removal with invalid request data."""
        # Arrange
        mock_request.get_json.return_value = request_data
        user_id = 456
        
        # Act
        response, status_code = remove_reaction(user_id)
        
        # Assert
        assert status_code == 400
        assert response.json == {"error": expected_error}

    @pytest.mark.parametrize("message_id,emoji,user_id", [
        (0, "👍", 1),
        (-1, "👎", 2),
        (999999, "❤️", 0),
        (123, "", 456),
        (123, "🎉", -1),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_boundary_values(self, mock_request, mock_manager, message_id, emoji, user_id, success_response):
        """Test reaction removal with boundary values."""
        # Arrange
        request_data = {"message_id": message_id, "emoji": emoji}
        mock_request.get_json.return_value = request_data
        mock_manager.remove_reaction.return_value = success_response
        
        # Act
        response, status_code = remove_reaction(user_id)
        
        # Assert
        assert status_code == 200
        mock_manager.remove_reaction.assert_called_once_with(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        )

    @pytest.mark.parametrize("exception_type,exception_message", [
        (ValueError, "Invalid message ID"),
        (KeyError, "User not found"),
        (ConnectionError, "Database connection failed"),
        (RuntimeError, "Unexpected error occurred"),
        (Exception, "Generic error"),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_exception_handling(self, mock_request, mock_manager, valid_request_data, exception_type, exception_message):
        """Test reaction removal exception handling."""
        # Arrange
        mock_request.get_json.return_value = valid_request_data
        mock_manager.remove_reaction.side_effect = exception_type(exception_message)
        user_id = 456
        
        # Act
        response, status_code = remove_reaction(user_id)
        
        # Assert
        assert status_code == 500
        assert response.json == {"error": f"Failed to remove reaction: {exception_message}"}

    @pytest.mark.parametrize("user_id_type", [
        (None),
        ("string_user_id"),
        (0),
        (-999),
        (99999999),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_various_user_ids(self, mock_request, mock_manager, valid_request_data, success_response, user_id_type):
        """Test reaction removal with various user ID types and values."""
        # Arrange
        mock_request.get_json.return_value = valid_request_data
        mock_manager.remove_reaction.return_value = success_response
        
        # Act
        response, status_code = remove_reaction(user_id_type)
        
        # Assert
        assert status_code == 200
        mock_manager.remove_reaction.assert_called_once_with(
            message_id=123,
            user_id=user_id_type,
            emoji="👍"
        )

    @pytest.mark.parametrize("emoji", [
        ("👍"),
        ("👎"),
        ("❤️"),
        ("😂"),
        ("😢"),
        ("😮"),
        ("😡"),
        ("🎉"),
        ("custom_emoji"),
        ("123"),
        ("!@#$%"),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_various_emojis(self, mock_request, mock_manager, success_response, emoji):
        """Test reaction removal with various emoji types."""
        # Arrange
        request_data = {"message_id": 123, "emoji": emoji}
        mock_request.get_json.return_value = request_data
        mock_manager.remove_reaction.return_value = success_response
        user_id = 456
        
        # Act
        response, status_code = remove_reaction(user_id)
        
        # Assert
        assert status_code == 200
        mock_manager.remove_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji=emoji
        )

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_manager_called_with_correct_params(self, mock_request, mock_manager, valid_request_data, success_response):
        """Test that reaction manager is called with correct parameters."""
        # Arrange
        mock_request.get_json.return_value = valid_request_data
        mock_manager.remove_reaction.return_value = success_response
        user_id = 789
        
        # Act
        remove_reaction(user_id)
        
        # Assert
        mock_manager.remove_reaction.assert_called_once()
        call_args = mock_manager.remove_reaction.call_args
        assert call_args.kwargs['message_id'] == 123
        assert call_args.kwargs['user_id'] == 789
        assert call_args.kwargs['emoji'] == "👍"

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_request_json_called(self, mock_request, mock_manager, valid_request_data, success_response):
        """Test that request.get_json() is called to retrieve data."""
        # Arrange
        mock_request.get_json.return_value = valid_request_data
        mock_manager.remove_reaction.return_value = success_response
        user_id = 456
        
        # Act
        remove_reaction(user_id)
        
        # Assert
        mock_request.get_json.assert_called_once()

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock
from flask import Flask

from routes.reactions import toggle_reaction

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
def mock_reaction_manager():
    """Mock reaction manager."""
    return Mock()

@pytest.fixture
def valid_request_data():
    """Valid request data for testing."""
    return {
        "message_id": 123,
        "emoji": "👍"
    }

@pytest.fixture
def mock_reaction_result():
    """Mock reaction toggle result."""
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

    def test_toggle_reaction_success(self, mock_manager, mock_request, valid_request_data, mock_reaction_result):
        """Test successful reaction toggle."""
        # Arrange
        user_id = 456
        mock_request.get_json.return_value = valid_request_data
        mock_manager.toggle_reaction.return_value = mock_reaction_result
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 200
        mock_manager.toggle_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji="👍"
        )
        assert response.json == mock_reaction_result

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "message_id and emoji are required"),
        ({}, "message_id and emoji are required"),
        ({"message_id": 123}, "message_id and emoji are required"),
        ({"emoji": "👍"}, "message_id and emoji are required"),
        ({"message_id": 123, "other_field": "value"}, "message_id and emoji are required"),
    ])
    @patch('routes.reactions.request')

    def test_toggle_reaction_missing_required_fields(self, mock_request, request_data, expected_error):
        """Test toggle reaction with missing or invalid request data."""
        # Arrange
        user_id = 456
        mock_request.get_json.return_value = request_data
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 400
        assert response.json["error"] == expected_error

    @pytest.mark.parametrize("message_id,emoji", [
        (0, "👍"),
        (-1, "👎"),
        (999999, "❤️"),
        (123, ""),
        (123, "🎉🎊"),
        (123, "custom_emoji"),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_toggle_reaction_boundary_values(self, mock_manager, mock_request, message_id, emoji):
        """Test toggle reaction with boundary and edge case values."""
        # Arrange
        user_id = 456
        request_data = {"message_id": message_id, "emoji": emoji}
        mock_request.get_json.return_value = request_data
        mock_result = {"message_id": message_id, "user_id": user_id, "emoji": emoji, "action": "added"}
        mock_manager.toggle_reaction.return_value = mock_result
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 200
        mock_manager.toggle_reaction.assert_called_once_with(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        )

    @pytest.mark.parametrize("error_message", [
        "Message not found",
        "Invalid emoji format",
        "User not authorized",
        "Message is archived",
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_toggle_reaction_value_error(self, mock_manager, mock_request, valid_request_data, error_message):
        """Test toggle reaction with ValueError from reaction manager."""
        # Arrange
        user_id = 456
        mock_request.get_json.return_value = valid_request_data
        mock_manager.toggle_reaction.side_effect = ValueError(error_message)
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 400
        assert response.json["error"] == error_message

    @pytest.mark.parametrize("exception,error_prefix", [
        (ConnectionError("Database connection failed"), "Failed to toggle reaction: Database connection failed"),
        (RuntimeError("Service unavailable"), "Failed to toggle reaction: Service unavailable"),
        (KeyError("missing_key"), "Failed to toggle reaction: 'missing_key'"),
        (Exception("Unknown error"), "Failed to toggle reaction: Unknown error"),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_toggle_reaction_general_exceptions(self, mock_manager, mock_request, valid_request_data, exception, error_prefix):
        """Test toggle reaction with various exceptions from reaction manager."""
        # Arrange
        user_id = 456
        mock_request.get_json.return_value = valid_request_data
        mock_manager.toggle_reaction.side_effect = exception
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 500
        assert response.json["error"] == error_prefix

    @pytest.mark.parametrize("user_id", [
        0,
        -1,
        999999,
        1,
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_toggle_reaction_different_user_ids(self, mock_manager, mock_request, valid_request_data, user_id):
        """Test toggle reaction with different user ID values."""
        # Arrange
        mock_request.get_json.return_value = valid_request_data
        mock_result = {"message_id": 123, "user_id": user_id, "emoji": "👍", "action": "removed"}
        mock_manager.toggle_reaction.return_value = mock_result
        
        # Act
        response, status_code = toggle_reaction(user_id)
        
        # Assert
        assert status_code == 200
        mock_manager.toggle_reaction.assert_called_once_with(
            message_id=123,
            user_id=user_id,
            emoji="👍"
        )
        assert response.json["user_id"] == user_id

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_toggle_reaction_manager_called_with_correct_params(self, mock_manager, mock_request):
        """Test that reaction manager is called with exact parameters."""
        # Arrange
        user_id = 789
        request_data = {"message_id": 456, "emoji": "🔥"}
        mock_request.get_json.return_value = request_data
        mock_manager.toggle_reaction.return_value = {"action": "added"}
        
        # Act
        toggle_reaction(user_id)
        
        # Assert
        mock_manager.toggle_reaction.assert_called_once_with(
            message_id=456,
            user_id=789,
            emoji="🔥"
        )

    @patch('routes.reactions.request')

    def test_toggle_reaction_request_get_json_called(self, mock_request):
        """Test that request.get_json() is called to retrieve data."""
        # Arrange
        user_id = 123
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
def mock_reaction_manager():
    """Mock reaction manager for testing."""
    return Mock()

@pytest.fixture
def sample_reactions():
    """Sample reaction data for testing."""
    return {
        "👍": [{"user_id": 1, "username": "user1"}, {"user_id": 2, "username": "user2"}],
        "❤️": [{"user_id": 3, "username": "user3"}],
        "😂": []
    }

class TestGetMessageReactions:
    """Test cases for get_message_reactions function."""

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_success(self, mock_manager, sample_reactions):
        """Test successful retrieval of message reactions."""
        # Arrange
        message_id = "msg_123"
        mock_manager.get_message_reactions.return_value = sample_reactions
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == sample_reactions
        mock_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_empty_reactions(self, mock_manager):
        """Test retrieval when message has no reactions."""
        # Arrange
        message_id = "msg_456"
        mock_manager.get_message_reactions.return_value = {}
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == {}
        mock_manager.get_message_reactions.assert_called_once_with(message_id)

    @pytest.mark.parametrize("message_id,expected_id", [
        ("msg_123", "msg_123"),
        ("", ""),
        ("msg_with_special_chars_!@#", "msg_with_special_chars_!@#"),
        ("123456789", "123456789"),
        ("very_long_message_id_" + "x" * 100, "very_long_message_id_" + "x" * 100),
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_various_message_ids(self, mock_manager, message_id, expected_id):
        """Test function with various message ID formats."""
        # Arrange
        mock_manager.get_message_reactions.return_value = {"👍": []}
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["message_id"] == expected_id
        mock_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_none_message_id(self, mock_manager):
        """Test function with None message ID."""
        # Arrange
        message_id = None
        mock_manager.get_message_reactions.return_value = {}
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["message_id"] is None
        mock_manager.get_message_reactions.assert_called_once_with(None)

    @pytest.mark.parametrize("exception_type,exception_message", [
        (ValueError, "Invalid message ID"),
        (KeyError, "Message not found"),
        (ConnectionError, "Database connection failed"),
        (TimeoutError, "Request timeout"),
        (RuntimeError, "Unexpected error occurred"),
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_exceptions(self, mock_manager, exception_type, exception_message):
        """Test function handles various exceptions properly."""
        # Arrange
        message_id = "msg_789"
        mock_manager.get_message_reactions.side_effect = exception_type(exception_message)
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get reactions: {exception_message}" in response_data["error"]
        mock_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_complex_reaction_data(self, mock_manager):
        """Test function with complex reaction data structure."""
        # Arrange
        message_id = "msg_complex"
        complex_reactions = {
            "👍": [
                {"user_id": 1, "username": "user1", "timestamp": "2023-01-01T10:00:00Z"},
                {"user_id": 2, "username": "user2", "timestamp": "2023-01-01T10:01:00Z"}
            ],
            "❤️": [
                {"user_id": 3, "username": "user3", "timestamp": "2023-01-01T10:02:00Z"}
            ],
            "🎉": [],
            "custom_emoji": [
                {"user_id": 4, "username": "user4", "timestamp": "2023-01-01T10:03:00Z"}
            ]
        }
        mock_manager.get_message_reactions.return_value = complex_reactions
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == complex_reactions
        assert len(response_data["reactions"]["👍"]) == 2
        assert len(response_data["reactions"]["❤️"]) == 1
        assert len(response_data["reactions"]["🎉"]) == 0
        assert len(response_data["reactions"]["custom_emoji"]) == 1

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_manager_returns_none(self, mock_manager):
        """Test function when reaction manager returns None."""
        # Arrange
        message_id = "msg_none"
        mock_manager.get_message_reactions.return_value = None
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] is None
        mock_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_unicode_message_id(self, mock_manager):
        """Test function with unicode characters in message ID."""
        # Arrange
        message_id = "msg_测试_🚀_émoji"
        mock_manager.get_message_reactions.return_value = {"🌟": []}
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        mock_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_exception_with_special_characters(self, mock_manager):
        """Test exception handling with special characters in error message."""
        # Arrange
        message_id = "msg_special"
        error_message = "Error with special chars: 测试 & émoji 🚨"
        mock_manager.get_message_reactions.side_effect = Exception(error_message)
        
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
from unittest.mock import Mock, patch
import pytest
from flask import Flask

from routes.reactions import get_user_reactions

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
def mock_reaction_manager():
    """Mock reaction manager."""
    return Mock()

@pytest.fixture
def sample_reactions():
    """Sample reaction data for testing."""
    return [
        {"id": 1, "message_id": 100, "emoji": "👍", "created_at": "2023-01-01T10:00:00Z"},
        {"id": 2, "message_id": 101, "emoji": "❤️", "created_at": "2023-01-01T11:00:00Z"},
        {"id": 3, "message_id": 100, "emoji": "😂", "created_at": "2023-01-01T12:00:00Z"}
    ]

class TestGetUserReactions:
    """Test cases for get_user_reactions function."""

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_success_no_message_filter(self, mock_manager, mock_request, sample_reactions):
        """Test successful retrieval of all user reactions without message filter."""
        # Arrange
        user_id = 123
        mock_request.args.get.return_value = None
        mock_manager.get_user_reactions.return_value = sample_reactions
        
        # Act
        with patch('routes.reactions.jsonify') as mock_jsonify:
            mock_jsonify.return_value = ({"success": True, "user_id": user_id, "reactions": sample_reactions}, 200)
            response, status_code = get_user_reactions(user_id)
        
        # Assert
        assert status_code == 200
        mock_request.args.get.assert_called_once_with('message_id', type=int)
        mock_manager.get_user_reactions.assert_called_once_with(user_id, None)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "user_id": user_id,
            "reactions": sample_reactions
        })

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_success_with_message_filter(self, mock_manager, mock_request, sample_reactions):
        """Test successful retrieval of user reactions filtered by message ID."""
        # Arrange
        user_id = 123
        message_id = 100
        filtered_reactions = [r for r in sample_reactions if r["message_id"] == message_id]
        mock_request.args.get.return_value = message_id
        mock_manager.get_user_reactions.return_value = filtered_reactions
        
        # Act
        with patch('routes.reactions.jsonify') as mock_jsonify:
            mock_jsonify.return_value = ({"success": True, "user_id": user_id, "reactions": filtered_reactions}, 200)
            response, status_code = get_user_reactions(user_id)
        
        # Assert
        assert status_code == 200
        mock_request.args.get.assert_called_once_with('message_id', type=int)
        mock_manager.get_user_reactions.assert_called_once_with(user_id, message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "user_id": user_id,
            "reactions": filtered_reactions
        })

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_empty_results(self, mock_manager, mock_request):
        """Test successful response with empty reactions list."""
        # Arrange
        user_id = 999
        mock_request.args.get.return_value = None
        mock_manager.get_user_reactions.return_value = []
        
        # Act
        with patch('routes.reactions.jsonify') as mock_jsonify:
            mock_jsonify.return_value = ({"success": True, "user_id": user_id, "reactions": []}, 200)
            response, status_code = get_user_reactions(user_id)
        
        # Assert
        assert status_code == 200
        mock_manager.get_user_reactions.assert_called_once_with(user_id, None)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "user_id": user_id,
            "reactions": []
        })

    @pytest.mark.parametrize("user_id,message_id", [
        (0, None),
        (-1, None),
        (1, 0),
        (999999, 999999),
        (1, -1)
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_boundary_values(self, mock_manager, mock_request, user_id, message_id):
        """Test function with boundary and edge case values."""
        # Arrange
        mock_request.args.get.return_value = message_id
        mock_manager.get_user_reactions.return_value = []
        
        # Act
        with patch('routes.reactions.jsonify') as mock_jsonify:
            mock_jsonify.return_value = ({"success": True, "user_id": user_id, "reactions": []}, 200)
            response, status_code = get_user_reactions(user_id)
        
        # Assert
        assert status_code == 200
        mock_manager.get_user_reactions.assert_called_once_with(user_id, message_id)

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_manager_exception(self, mock_manager, mock_request):
        """Test error handling when reaction manager raises an exception."""
        # Arrange
        user_id = 123
        error_message = "Database connection failed"
        mock_request.args.get.return_value = None
        mock_manager.get_user_reactions.side_effect = Exception(error_message)
        
        # Act
        with patch('routes.reactions.jsonify') as mock_jsonify:
            mock_jsonify.return_value = ({"error": f"Failed to get user reactions: {error_message}"}, 500)
            response, status_code = get_user_reactions(user_id)
        
        # Assert
        assert status_code == 500
        mock_manager.get_user_reactions.assert_called_once_with(user_id, None)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get user reactions: {error_message}"
        })

    @pytest.mark.parametrize("exception_type,exception_message", [
        (ValueError, "Invalid user ID"),
        (KeyError, "User not found"),
        (ConnectionError, "Network timeout"),
        (RuntimeError, "Service unavailable")
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_various_exceptions(self, mock_manager, mock_request, exception_type, exception_message):
        """Test error handling for various exception types."""
        # Arrange
        user_id = 123
        mock_request.args.get.return_value = None
        mock_manager.get_user_reactions.side_effect = exception_type(exception_message)
        
        # Act
        with patch('routes.reactions.jsonify') as mock_jsonify:
            mock_jsonify.return_value = ({"error": f"Failed to get user reactions: {exception_message}"}, 500)
            response, status_code = get_user_reactions(user_id)
        
        # Assert
        assert status_code == 500
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get user reactions: {exception_message}"
        })

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_request_args_parsing(self, mock_manager, mock_request):
        """Test that request args are parsed correctly with proper type conversion."""
        # Arrange
        user_id = 123
        mock_request.args.get.return_value = 456
        mock_manager.get_user_reactions.return_value = []
        
        # Act
        with patch('routes.reactions.jsonify') as mock_jsonify:
            mock_jsonify.return_value = ({"success": True, "user_id": user_id, "reactions": []}, 200)
            get_user_reactions(user_id)
        
        # Assert
        mock_request.args.get.assert_called_once_with('message_id', type=int)
        mock_manager.get_user_reactions.assert_called_once_with(user_id, 456)

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_with_none_user_id(self, mock_manager, mock_request):
        """Test function behavior with None user_id."""
        # Arrange
        user_id = None
        mock_request.args.get.return_value = None
        mock_manager.get_user_reactions.return_value = []
        
        # Act
        with patch('routes.reactions.jsonify') as mock_jsonify:
            mock_jsonify.return_value = ({"success": True, "user_id": user_id, "reactions": []}, 200)
            response, status_code = get_user_reactions(user_id)
        
        # Assert
        assert status_code == 200
        mock_manager.get_user_reactions.assert_called_once_with(user_id, None)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "user_id": user_id,
            "reactions": []
        })

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_response_structure(self, mock_manager, mock_request, sample_reactions):
        """Test that the response structure is correct."""
        # Arrange
        user_id = 123
        mock_request.args.get.return_value = None
        mock_manager.get_user_reactions.return_value = sample_reactions
        
        # Act
        with patch('routes.reactions.jsonify') as mock_jsonify:
            expected_response = {
                "success": True,
                "user_id": user_id,
                "reactions": sample_reactions
            }
            mock_jsonify.return_value = (expected_response, 200)
            response, status_code = get_user_reactions(user_id)
        
        # Assert
        mock_jsonify.assert_called_once_with(expected_response)
        # Verify all required keys are present in the response
        call_args = mock_jsonify.call_args[0][0]
        assert "success" in call_args
        assert "user_id" in call_args
        assert "reactions" in call_args
        assert call_args["success"] is True
        assert call_args["user_id"] == user_id
        assert call_args["reactions"] == sample_reactions

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock

from routes.reactions import get_reaction_count

@pytest.fixture
def mock_reaction_manager():
    """Mock reaction manager for testing."""
    return Mock()

class TestGetReactionCount:
    """Test cases for get_reaction_count function."""

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_successful_reaction_count_retrieval(self, mock_jsonify, mock_manager):
        """Test successful retrieval of reaction count."""
        # Arrange
        message_id = "msg_123"
        expected_count = 5
        mock_manager.get_reaction_count.return_value = expected_count
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        mock_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "count": expected_count
        })
        assert status_code == 200

    @pytest.mark.parametrize("message_id,expected_count", [
        ("msg_001", 0),
        ("msg_002", 1),
        ("msg_003", 100),
        ("msg_004", 999999),
        ("", 0),
        ("special-chars-!@#$%", 42),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_various_message_ids_and_counts(self, mock_jsonify, mock_manager, message_id, expected_count):
        """Test reaction count retrieval with various message IDs and count values."""
        # Arrange
        mock_manager.get_reaction_count.return_value = expected_count
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        mock_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "count": expected_count
        })
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_none_message_id(self, mock_jsonify, mock_manager):
        """Test handling of None message_id."""
        # Arrange
        message_id = None
        expected_count = 0
        mock_manager.get_reaction_count.return_value = expected_count
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        mock_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "count": expected_count
        })
        assert status_code == 200

    @pytest.mark.parametrize("exception_type,exception_message", [
        (ValueError, "Invalid message ID"),
        (KeyError, "Message not found"),
        (ConnectionError, "Database connection failed"),
        (TimeoutError, "Request timeout"),
        (RuntimeError, "Unexpected error occurred"),
        (Exception, "Generic error"),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_exception_handling(self, mock_jsonify, mock_manager, exception_type, exception_message):
        """Test exception handling for various error types."""
        # Arrange
        message_id = "msg_error"
        mock_manager.get_reaction_count.side_effect = exception_type(exception_message)
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        mock_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get reaction count: {exception_message}"
        })
        assert status_code == 500

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_exception_with_empty_message(self, mock_jsonify, mock_manager):
        """Test exception handling with empty error message."""
        # Arrange
        message_id = "msg_empty_error"
        mock_manager.get_reaction_count.side_effect = Exception("")
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        mock_manager.get_reaction_count.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": "Failed to get reaction count: "
        })
        assert status_code == 500

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_called_with_correct_parameters(self, mock_jsonify, mock_manager):
        """Test that reaction_manager is called with the exact parameters passed to function."""
        # Arrange
        message_id = "test_message_123"
        mock_manager.get_reaction_count.return_value = 10
        mock_jsonify.return_value = Mock()
        
        # Act
        get_reaction_count(message_id)
        
        # Assert
        mock_manager.get_reaction_count.assert_called_once_with(message_id)
        assert mock_manager.get_reaction_count.call_count == 1

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_jsonify_response_structure_success(self, mock_jsonify, mock_manager):
        """Test that jsonify is called with correct response structure for success case."""
        # Arrange
        message_id = "msg_structure_test"
        count = 25
        mock_manager.get_reaction_count.return_value = count
        mock_jsonify.return_value = Mock()
        
        # Act
        get_reaction_count(message_id)
        
        # Assert
        expected_response = {
            "success": True,
            "message_id": message_id,
            "count": count
        }
        mock_jsonify.assert_called_once_with(expected_response)

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_jsonify_response_structure_error(self, mock_jsonify, mock_manager):
        """Test that jsonify is called with correct response structure for error case."""
        # Arrange
        message_id = "msg_error_structure"
        error_message = "Test error message"
        mock_manager.get_reaction_count.side_effect = Exception(error_message)
        mock_jsonify.return_value = Mock()
        
        # Act
        get_reaction_count(message_id)
        
        # Assert
        expected_response = {
            "error": f"Failed to get reaction count: {error_message}"
        }
        mock_jsonify.assert_called_once_with(expected_response)

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_return_tuple_structure(self, mock_jsonify, mock_manager):
        """Test that function returns tuple with correct structure."""
        # Arrange
        message_id = "msg_tuple_test"
        mock_manager.get_reaction_count.return_value = 15
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result = get_reaction_count(message_id)
        
        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] == mock_response
        assert result[1] in [200, 500]

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_negative_count_handling(self, mock_jsonify, mock_manager):
        """Test handling of negative count values."""
        # Arrange
        message_id = "msg_negative"
        negative_count = -5
        mock_manager.get_reaction_count.return_value = negative_count
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_reaction_count(message_id)
        
        # Assert
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "count": negative_count
        })
        assert status_code == 200

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import Mock, patch

from routes.reactions import get_most_popular

@pytest.fixture
def mock_reaction_manager():
    """Mock reaction manager for testing."""
    return Mock()

class TestGetMostPopular:
    """Test cases for get_most_popular function."""

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_successful_emoji_retrieval(self, mock_jsonify, mock_manager):
        """Test successful retrieval of most popular emoji."""
        # Arrange
        message_id = "msg_123"
        expected_emoji = "👍"
        mock_manager.get_most_popular_emoji.return_value = expected_emoji
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_emoji_retrieval_with_none_result(self, mock_jsonify, mock_manager):
        """Test when reaction manager returns None."""
        # Arrange
        message_id = "msg_456"
        mock_manager.get_most_popular_emoji.return_value = None
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": None
        })
        assert status_code == 200

    @pytest.mark.parametrize("message_id,expected_emoji", [
        ("msg_001", "😂"),
        ("", "❤️"),
        ("very_long_message_id_with_special_chars_123!@#", "🎉"),
        ("123", "🔥"),
        ("msg with spaces", "👏"),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_various_message_ids_and_emojis(self, mock_jsonify, mock_manager, message_id, expected_emoji):
        """Test function with various message IDs and emoji responses."""
        # Arrange
        mock_manager.get_most_popular_emoji.return_value = expected_emoji
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_exception(self, mock_jsonify, mock_manager):
        """Test exception handling when reaction manager fails."""
        # Arrange
        message_id = "msg_error"
        error_message = "Database connection failed"
        mock_manager.get_most_popular_emoji.side_effect = Exception(error_message)
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get popular emoji: {error_message}"
        })
        assert status_code == 500

    @pytest.mark.parametrize("exception_type,error_msg", [
        (ValueError, "Invalid message ID format"),
        (KeyError, "Message not found"),
        (ConnectionError, "Network timeout"),
        (RuntimeError, "Service unavailable"),
        (TypeError, "Invalid parameter type"),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_various_exception_types(self, mock_jsonify, mock_manager, exception_type, error_msg):
        """Test handling of different exception types."""
        # Arrange
        message_id = "msg_test"
        mock_manager.get_most_popular_emoji.side_effect = exception_type(error_msg)
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get popular emoji: {error_msg}"
        })
        assert status_code == 500

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_empty_string_emoji_response(self, mock_jsonify, mock_manager):
        """Test when reaction manager returns empty string."""
        # Arrange
        message_id = "msg_empty"
        mock_manager.get_most_popular_emoji.return_value = ""
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": ""
        })
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_unicode_emoji_handling(self, mock_jsonify, mock_manager):
        """Test handling of complex unicode emojis."""
        # Arrange
        message_id = "msg_unicode"
        complex_emoji = "👨‍👩‍👧‍👦"  # Family emoji with ZWJ sequences
        mock_manager.get_most_popular_emoji.return_value = complex_emoji
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": complex_emoji
        })
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_exception_with_special_characters_in_message(self, mock_jsonify, mock_manager):
        """Test exception handling with special characters in error message."""
        # Arrange
        message_id = "msg_special"
        error_with_special_chars = "Error: 'message' not found in database! @#$%^&*()"
        mock_manager.get_most_popular_emoji.side_effect = Exception(error_with_special_chars)
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get popular emoji: {error_with_special_chars}"
        })
        assert status_code == 500

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_jsonify_called_with_correct_structure(self, mock_jsonify, mock_manager):
        """Test that jsonify is called with the correct response structure."""
        # Arrange
        message_id = "msg_structure"
        emoji = "🚀"
        mock_manager.get_most_popular_emoji.return_value = emoji
        mock_jsonify.return_value = Mock()
        
        # Act
        get_most_popular(message_id)
        
        # Assert
        call_args = mock_jsonify.call_args[0][0]
        assert "success" in call_args
        assert "message_id" in call_args
        assert "most_popular_emoji" in call_args
        assert call_args["success"] is True
        assert call_args["message_id"] == message_id
        assert call_args["most_popular_emoji"] == emoji

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock

from routes.reactions import get_allowed_emojis

@pytest.fixture
def mock_reaction_manager():
    """Mock ReactionManager for testing."""
    return Mock()

class TestGetAllowedEmojis:
    """Test cases for get_allowed_emojis function."""

    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_success(self, mock_jsonify, mock_reaction_manager_class):
        """Test successful retrieval of allowed emojis."""
        # Arrange
        expected_emojis = ['👍', '👎', '❤️', '😂', '😮', '😢', '😡']
        mock_reaction_manager_class.get_allowed_emojis.return_value = expected_emojis
        
        expected_response = {
            "success": True,
            "emojis": expected_emojis
        }
        mock_jsonify.return_value = (expected_response, 200)
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        mock_reaction_manager_class.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": expected_emojis
        })
        assert result == expected_response
        assert status_code == 200

    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_empty_list(self, mock_jsonify, mock_reaction_manager_class):
        """Test when ReactionManager returns empty emoji list."""
        # Arrange
        expected_emojis = []
        mock_reaction_manager_class.get_allowed_emojis.return_value = expected_emojis
        
        expected_response = {
            "success": True,
            "emojis": expected_emojis
        }
        mock_jsonify.return_value = (expected_response, 200)
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        mock_reaction_manager_class.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": expected_emojis
        })
        assert result == expected_response
        assert status_code == 200

    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_none_return(self, mock_jsonify, mock_reaction_manager_class):
        """Test when ReactionManager returns None."""
        # Arrange
        mock_reaction_manager_class.get_allowed_emojis.return_value = None
        
        expected_response = {
            "success": True,
            "emojis": None
        }
        mock_jsonify.return_value = (expected_response, 200)
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        mock_reaction_manager_class.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": None
        })
        assert result == expected_response
        assert status_code == 200

    @pytest.mark.parametrize("emoji_list,expected_count", [
        (['👍'], 1),
        (['👍', '👎'], 2),
        (['👍', '👎', '❤️', '😂', '😮'], 5),
        (['👍', '👎', '❤️', '😂', '😮', '😢', '😡', '🎉', '🔥', '💯'], 10),
    ])
    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_various_counts(self, mock_jsonify, mock_reaction_manager_class, emoji_list, expected_count):
        """Test function with various emoji list sizes."""
        # Arrange
        mock_reaction_manager_class.get_allowed_emojis.return_value = emoji_list
        
        expected_response = {
            "success": True,
            "emojis": emoji_list
        }
        mock_jsonify.return_value = (expected_response, 200)
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        mock_reaction_manager_class.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": emoji_list
        })
        assert result == expected_response
        assert status_code == 200
        assert len(result["emojis"]) == expected_count

    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_reaction_manager_exception(self, mock_jsonify, mock_reaction_manager_class):
        """Test when ReactionManager.get_allowed_emojis raises an exception."""
        # Arrange
        mock_reaction_manager_class.get_allowed_emojis.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            get_allowed_emojis()
        
        mock_reaction_manager_class.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_not_called()

    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_jsonify_exception(self, mock_jsonify, mock_reaction_manager_class):
        """Test when jsonify raises an exception."""
        # Arrange
        expected_emojis = ['👍', '👎', '❤️']
        mock_reaction_manager_class.get_allowed_emojis.return_value = expected_emojis
        mock_jsonify.side_effect = Exception("JSON serialization error")
        
        # Act & Assert
        with pytest.raises(Exception, match="JSON serialization error"):
            get_allowed_emojis()
        
        mock_reaction_manager_class.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": expected_emojis
        })

    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_unicode_emojis(self, mock_jsonify, mock_reaction_manager_class):
        """Test function with various Unicode emoji formats."""
        # Arrange
        unicode_emojis = [
            '👍',  # Standard emoji
            '🏽',  # Skin tone modifier
            '👨‍💻',  # Complex emoji with ZWJ
            '🇺🇸',  # Flag emoji
            '1️⃣',  # Keycap emoji
        ]
        mock_reaction_manager_class.get_allowed_emojis.return_value = unicode_emojis
        
        expected_response = {
            "success": True,
            "emojis": unicode_emojis
        }
        mock_jsonify.return_value = (expected_response, 200)
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        mock_reaction_manager_class.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": unicode_emojis
        })
        assert result == expected_response
        assert status_code == 200

    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_response_structure(self, mock_jsonify, mock_reaction_manager_class):
        """Test that response always has correct structure."""
        # Arrange
        test_emojis = ['👍', '👎']
        mock_reaction_manager_class.get_allowed_emojis.return_value = test_emojis
        
        expected_response = {
            "success": True,
            "emojis": test_emojis
        }
        mock_jsonify.return_value = (expected_response, 200)
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert isinstance(result, dict)
        assert "success" in result
        assert "emojis" in result
        assert result["success"] is True
        assert result["emojis"] == test_emojis
        assert status_code == 200

    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_call_count(self, mock_jsonify, mock_reaction_manager_class):
        """Test that ReactionManager.get_allowed_emojis is called exactly once."""
        # Arrange
        test_emojis = ['👍']
        mock_reaction_manager_class.get_allowed_emojis.return_value = test_emojis
        mock_jsonify.return_value = ({"success": True, "emojis": test_emojis}, 200)
        
        # Act
        get_allowed_emojis()
        
        # Assert
        assert mock_reaction_manager_class.get_allowed_emojis.call_count == 1
        assert mock_jsonify.call_count == 1

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock
from flask import Flask

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
def mock_reaction_manager():
    """Mock reaction manager."""
    return Mock()

@pytest.fixture
def valid_reactions_data():
    """Valid reactions test data."""
    return {
        "reactions": [
            {"message_id": 1, "user_id": 123, "emoji": "👍"},
            {"message_id": 2, "user_id": 123, "emoji": "❤️"},
            {"message_id": 3, "user_id": 123, "emoji": "😂"}
        ]
    }

@pytest.fixture
def bulk_add_result():
    """Mock bulk add result."""
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

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_successful_bulk_add_reactions(self, mock_manager, mock_request, valid_reactions_data, bulk_add_result):
        """Test successful bulk addition of reactions."""
        mock_request.get_json.return_value = valid_reactions_data
        mock_manager.bulk_add_reactions.return_value = bulk_add_result
        
        response, status_code = bulk_add_reactions(123)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["result"] == bulk_add_result
        mock_manager.bulk_add_reactions.assert_called_once_with(valid_reactions_data["reactions"])

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "reactions array is required"),
        ({}, "reactions array is required"),
        ({"other_field": "value"}, "reactions array is required"),
        ({"reactions": None}, "reactions array is required"),
    ])
    @patch('routes.reactions.request')

    def test_missing_or_invalid_request_data(self, mock_request, request_data, expected_error):
        """Test handling of missing or invalid request data."""
        mock_request.get_json.return_value = request_data
        
        response, status_code = bulk_add_reactions(123)
        
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data["error"] == expected_error

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_empty_reactions_array(self, mock_manager, mock_request):
        """Test handling of empty reactions array."""
        empty_data = {"reactions": []}
        mock_request.get_json.return_value = empty_data
        mock_manager.bulk_add_reactions.return_value = {"added": 0, "failed": 0, "details": []}
        
        response, status_code = bulk_add_reactions(123)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["result"]["added"] == 0

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_single_reaction_in_bulk(self, mock_manager, mock_request):
        """Test bulk add with single reaction."""
        single_reaction_data = {
            "reactions": [{"message_id": 1, "user_id": 123, "emoji": "👍"}]
        }
        expected_result = {
            "added": 1,
            "failed": 0,
            "details": [{"message_id": 1, "status": "success"}]
        }
        
        mock_request.get_json.return_value = single_reaction_data
        mock_manager.bulk_add_reactions.return_value = expected_result
        
        response, status_code = bulk_add_reactions(123)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["result"]["added"] == 1

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_large_bulk_reactions(self, mock_manager, mock_request):
        """Test bulk add with large number of reactions."""
        large_reactions_data = {
            "reactions": [
                {"message_id": i, "user_id": 123, "emoji": "👍"} 
                for i in range(1, 101)
            ]
        }
        expected_result = {"added": 100, "failed": 0, "details": []}
        
        mock_request.get_json.return_value = large_reactions_data
        mock_manager.bulk_add_reactions.return_value = expected_result
        
        response, status_code = bulk_add_reactions(123)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["result"]["added"] == 100

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_partial_success_bulk_add(self, mock_manager, mock_request, valid_reactions_data):
        """Test bulk add with partial success."""
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
        mock_manager.bulk_add_reactions.return_value = partial_result
        
        response, status_code = bulk_add_reactions(123)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["result"]["added"] == 2
        assert response_data["result"]["failed"] == 1

    @pytest.mark.parametrize("exception_type,exception_message", [
        (ValueError, "Invalid reaction data"),
        (KeyError, "Missing required field"),
        (RuntimeError, "Database connection failed"),
        (Exception, "Unexpected error occurred"),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_exception_handling(self, mock_manager, mock_request, valid_reactions_data, exception_type, exception_message):
        """Test handling of various exceptions during bulk add."""
        mock_request.get_json.return_value = valid_reactions_data
        mock_manager.bulk_add_reactions.side_effect = exception_type(exception_message)
        
        response, status_code = bulk_add_reactions(123)
        
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "Failed to bulk add reactions" in response_data["error"]
        assert exception_message in response_data["error"]

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_reaction_manager_called_with_correct_data(self, mock_manager, mock_request, valid_reactions_data):
        """Test that reaction manager is called with correct data."""
        mock_request.get_json.return_value = valid_reactions_data
        mock_manager.bulk_add_reactions.return_value = {"added": 3, "failed": 0}
        
        bulk_add_reactions(123)
        
        mock_manager.bulk_add_reactions.assert_called_once_with(valid_reactions_data["reactions"])

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_user_id_parameter_not_used_in_logic(self, mock_manager, mock_request, valid_reactions_data):
        """Test that user_id parameter doesn't affect the logic."""
        mock_request.get_json.return_value = valid_reactions_data
        mock_manager.bulk_add_reactions.return_value = {"added": 3, "failed": 0}
        
        # Test with different user_id values
        response1, status1 = bulk_add_reactions(123)
        response2, status2 = bulk_add_reactions(456)
        response3, status3 = bulk_add_reactions(None)
        
        # All should behave identically
        assert status1 == status2 == status3 == 200
        assert mock_manager.bulk_add_reactions.call_count == 3

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_unicode_emoji_handling(self, mock_manager, mock_request):
        """Test handling of various Unicode emoji characters."""
        unicode_reactions_data = {
            "reactions": [
                {"message_id": 1, "user_id": 123, "emoji": "🎉"},
                {"message_id": 2, "user_id": 123, "emoji": "🚀"},
                {"message_id": 3, "user_id": 123, "emoji": "💯"},
                {"message_id": 4, "user_id": 123, "emoji": "🔥"}
            ]
        }
        expected_result = {"added": 4, "failed": 0, "details": []}
        
        mock_request.get_json.return_value = unicode_reactions_data
        mock_manager.bulk_add_reactions.return_value = expected_result
        
        response, status_code = bulk_add_reactions(123)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        mock_manager.bulk_add_reactions.assert_called_once_with(unicode_reactions_data["reactions"])

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_boundary_values_in_reactions(self, mock_manager, mock_request):
        """Test handling of boundary values in reaction data."""
        boundary_reactions_data = {
            "reactions": [
                {"message_id": 0, "user_id": 0, "emoji": "👍"},
                {"message_id": 999999999, "user_id": 999999999, "emoji": "❤️"},
                {"message_id": -1, "user_id": -1, "emoji": "😂"}
            ]
        }
        expected_result = {"added": 3, "failed": 0, "details": []}
        
        mock_request.get_json.return_value = boundary_reactions_data
        mock_manager.bulk_add_reactions.return_value = expected_result
        
        response, status_code = bulk_add_reactions(123)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        mock_manager.bulk_add_reactions.assert_called_once_with(boundary_reactions_data["reactions"])

# Standard library
# Third-party
# Local


from unittest.mock import Mock, patch
import pytest
from flask import Flask

from routes.reactions import decorated_function
from routes.reactions import app

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def mock_request():
    """Mock Flask request object."""
    return Mock()

@pytest.fixture
def mock_function():
    """Mock function to be decorated."""
    return Mock(return_value="success")

@pytest.fixture
def app():
    """Create Flask app for testing."""
    return app

class TestDecoratedFunction:
    """Test cases for decorated_function authentication decorator."""

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_authentication_with_header_user_id(self, mock_jsonify, mock_request, mock_function):
        """Test successful authentication using X-User-ID header."""
        # Arrange
        mock_request.headers.get.return_value = "123"
        mock_request.args.get.return_value = None
        
        # Act
        result = decorated_function(mock_function, "arg1", "arg2", key="value")
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_function.assert_called_once_with("arg1", "arg2", user_id=123, key="value")
        assert result == "success"

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_authentication_with_query_param_user_id(self, mock_jsonify, mock_request, mock_function):
        """Test successful authentication using query parameter user_id."""
        # Arrange
        mock_request.headers.get.return_value = None
        mock_request.args.get.return_value = "456"
        
        # Act
        result = decorated_function(mock_function, "test_arg", param="test")
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_request.args.get.assert_called_once_with('user_id')
        mock_function.assert_called_once_with("test_arg", user_id=456, param="test")
        assert result == "success"

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_authentication_header_takes_precedence(self, mock_jsonify, mock_request, mock_function):
        """Test that header user_id takes precedence over query parameter."""
        # Arrange
        mock_request.headers.get.return_value = "789"
        mock_request.args.get.return_value = "999"
        
        # Act
        result = decorated_function(mock_function)
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_function.assert_called_once_with(user_id=789)
        assert result == "success"

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_authentication_required_no_user_id(self, mock_jsonify, mock_request, mock_function):
        """Test authentication failure when no user_id is provided."""
        # Arrange
        mock_request.headers.get.return_value = None
        mock_request.args.get.return_value = None
        mock_jsonify.return_value = {"error": "Authentication required"}
        
        # Act
        result = decorated_function(mock_function, "arg1")
        
        # Assert
        mock_request.headers.get.assert_called_once_with('X-User-ID')
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
        """Test that user_id string values are properly converted to integers."""
        # Arrange
        mock_request.headers.get.return_value = user_id_value
        mock_request.args.get.return_value = None
        
        # Act
        result = decorated_function(mock_function)
        
        # Assert
        mock_function.assert_called_once_with(user_id=expected_int)
        assert result == "success"

    @pytest.mark.parametrize("empty_value", [
        "",
        "   ",
        None,
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_authentication_required_empty_user_id(self, mock_jsonify, mock_request, mock_function, empty_value):
        """Test authentication failure with empty or whitespace user_id values."""
        # Arrange
        mock_request.headers.get.return_value = empty_value
        mock_request.args.get.return_value = None
        mock_jsonify.return_value = {"error": "Authentication required"}
        
        # Act
        result = decorated_function(mock_function)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "Authentication required"})
        mock_function.assert_not_called()
        assert result == ({"error": "Authentication required"}, 401)

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_function_called_with_args_and_kwargs(self, mock_jsonify, mock_request, mock_function):
        """Test that decorated function receives all original args and kwargs plus user_id."""
        # Arrange
        mock_request.headers.get.return_value = "100"
        mock_request.args.get.return_value = None
        
        # Act
        result = decorated_function(
            mock_function, 
            "pos_arg1", 
            "pos_arg2", 
            keyword1="value1", 
            keyword2="value2"
        )
        
        # Assert
        mock_function.assert_called_once_with(
            "pos_arg1", 
            "pos_arg2", 
            user_id=100, 
            keyword1="value1", 
            keyword2="value2"
        )
        assert result == "success"

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_function_return_value_preserved(self, mock_jsonify, mock_request, mock_function):
        """Test that the decorated function's return value is preserved."""
        # Arrange
        mock_request.headers.get.return_value = "200"
        mock_request.args.get.return_value = None
        expected_return = {"data": "test", "status": "ok"}
        mock_function.return_value = expected_return
        
        # Act
        result = decorated_function(mock_function)
        
        # Assert
        assert result == expected_return

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_invalid_user_id_conversion_raises_exception(self, mock_jsonify, mock_request, mock_function):
        """Test that invalid user_id values that can't be converted to int raise ValueError."""
        # Arrange
        mock_request.headers.get.return_value = "invalid_number"
        mock_request.args.get.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError):
            decorated_function(mock_function)

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_no_args_no_kwargs(self, mock_jsonify, mock_request, mock_function):
        """Test decorated function with no arguments or keyword arguments."""
        # Arrange
        mock_request.headers.get.return_value = "42"
        mock_request.args.get.return_value = None
        
        # Act
        result = decorated_function(mock_function)
        
        # Assert
        mock_function.assert_called_once_with(user_id=42)
        assert result == "success"

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_user_id_overwrite_protection(self, mock_jsonify, mock_request, mock_function):
        """Test that user_id in kwargs gets overwritten by authenticated user_id."""
        # Arrange
        mock_request.headers.get.return_value = "999"
        mock_request.args.get.return_value = None
        
        # Act
        result = decorated_function(mock_function, user_id=123, other_param="test")
        
        # Assert
        mock_function.assert_called_once_with(user_id=999, other_param="test")
        assert result == "success"

# Standard library
# Third-party
# Local

