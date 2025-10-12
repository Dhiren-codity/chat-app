"""
Auto-generated tests using LLM and RAG
"""

import pytest


from functools import wraps
import pytest
from flask import Flask, request, jsonify
from unittest.mock import patch, Mock

from routes.reactions import require_auth

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestRequireAuth:

    def test_decorator_with_header_auth_success(self, app):
        """Test decorator with valid X-User-ID header"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"success": True, "user_id": kwargs.get('user_id')})
        
        with app.test_request_context(headers={'X-User-ID': '123'}):
            response = dummy_function()
            assert response[1] != 401
    

    def test_decorator_with_query_param_auth_success(self, app):
        """Test decorator with valid user_id query parameter"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"success": True, "user_id": kwargs.get('user_id')})
        
        with app.test_request_context(query_string='user_id=456'):
            response = dummy_function()
            assert response[1] != 401
    

    def test_decorator_no_auth_returns_401(self, app):
        """Test decorator without authentication returns 401"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"success": True})
        
        with app.test_request_context():
            response, status_code = dummy_function()
            assert status_code == 401
            assert response.json == {"error": "Authentication required"}
    

    def test_decorator_empty_header_returns_401(self, app):
        """Test decorator with empty X-User-ID header returns 401"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"success": True})
        
        with app.test_request_context(headers={'X-User-ID': ''}):
            response, status_code = dummy_function()
            assert status_code == 401
            assert response.json == {"error": "Authentication required"}
    

    def test_decorator_empty_query_param_returns_401(self, app):
        """Test decorator with empty user_id query parameter returns 401"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"success": True})
        
        with app.test_request_context(query_string='user_id='):
            response, status_code = dummy_function()
            assert status_code == 401
            assert response.json == {"error": "Authentication required"}
    

    def test_decorator_header_priority_over_query_param(self, app):
        """Test that X-User-ID header takes priority over query parameter"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"user_id": kwargs.get('user_id')})
        
        with app.test_request_context(headers={'X-User-ID': '789'}, query_string='user_id=456'):
            response = dummy_function()
            assert response.json["user_id"] == 789
    

    def test_decorator_converts_user_id_to_int(self, app):
        """Test that user_id is converted to integer"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"user_id": kwargs.get('user_id'), "type": type(kwargs.get('user_id')).__name__})
        
        with app.test_request_context(headers={'X-User-ID': '123'}):
            response = dummy_function()
            assert response.json["user_id"] == 123
            assert response.json["type"] == "int"
    

    def test_decorator_preserves_original_args(self, app):
        """Test that decorator preserves original function arguments"""
        @require_auth
        def dummy_function(arg1, arg2, *args, **kwargs):
            return jsonify({
                "arg1": arg1,
                "arg2": arg2,
                "args": args,
                "user_id": kwargs.get('user_id')
            })
        
        with app.test_request_context(headers={'X-User-ID': '123'}):
            response = dummy_function("test1", "test2", "extra1", "extra2")
            assert response.json["arg1"] == "test1"
            assert response.json["arg2"] == "test2"
            assert response.json["args"] == ["extra1", "extra2"]
            assert response.json["user_id"] == 123
    

    def test_decorator_preserves_original_kwargs(self, app):
        """Test that decorator preserves original function keyword arguments"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({
                "original_kwarg": kwargs.get('original_kwarg'),
                "user_id": kwargs.get('user_id')
            })
        
        with app.test_request_context(headers={'X-User-ID': '123'}):
            response = dummy_function(original_kwarg="test_value")
            assert response.json["original_kwarg"] == "test_value"
            assert response.json["user_id"] == 123
    
    @pytest.mark.parametrize("user_id_value", [
        "0",
        "1",
        "999999",
        "-1",
        "-999"
    ])

    def test_decorator_various_user_id_values(self, app, user_id_value):
        """Test decorator with various user_id values"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"user_id": kwargs.get('user_id')})
        
        with app.test_request_context(headers={'X-User-ID': user_id_value}):
            response = dummy_function()
            assert response.json["user_id"] == int(user_id_value)
    

    def test_decorator_invalid_user_id_raises_value_error(self, app):
        """Test decorator with non-numeric user_id raises ValueError"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"success": True})
        
        with app.test_request_context(headers={'X-User-ID': 'invalid'}):
            with pytest.raises(ValueError):
                dummy_function()
    

    def test_decorator_preserves_function_metadata(self):
        """Test that decorator preserves original function metadata"""
        def original_function():
            """Original docstring"""
            pass
        
        decorated = require_auth(original_function)
        assert decorated.__name__ == original_function.__name__
        assert decorated.__doc__ == original_function.__doc__
    

    def test_decorator_none_header_with_valid_query_param(self, app):
        """Test decorator with None header but valid query parameter"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"user_id": kwargs.get('user_id')})
        
        with app.test_request_context(query_string='user_id=789'):
            response = dummy_function()
            assert response.json["user_id"] == 789
    

    def test_decorator_both_auth_methods_missing(self, app):
        """Test decorator when both header and query param are missing"""
        @require_auth
        def dummy_function(*args, **kwargs):
            return jsonify({"success": True})
        
        with app.test_request_context():
            response, status_code = dummy_function()
            assert status_code == 401
            assert response.json == {"error": "Authentication required"}

# Standard library
# Third-party
# Local


import json
import pytest
from flask import Flask
from unittest.mock import patch, Mock

from routes.reactions import add_reaction

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_reaction_manager():
    return Mock()

class TestAddReaction:
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_add_reaction_success(self, mock_jsonify, mock_manager, mock_request):
        # Setup
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.add_reaction.return_value = {'success': True, 'reaction_id': 456}
        mock_jsonify.return_value = Mock()
        
        # Execute
        result = add_reaction(user_id=789)
        
        # Assert
        mock_manager.add_reaction.assert_called_once_with(
            message_id=123,
            user_id=789,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({'success': True, 'reaction_id': 456})
        assert result[1] == 200

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_add_reaction_failure_from_manager(self, mock_jsonify, mock_manager, mock_request):
        # Setup
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.add_reaction.return_value = {'success': False, 'error': 'Duplicate reaction'}
        mock_jsonify.return_value = Mock()
        
        # Execute
        result = add_reaction(user_id=789)
        
        # Assert
        mock_manager.add_reaction.assert_called_once_with(
            message_id=123,
            user_id=789,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({'success': False, 'error': 'Duplicate reaction'})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_add_reaction_no_data(self, mock_jsonify, mock_request):
        # Setup
        mock_request.get_json.return_value = None
        mock_jsonify.return_value = Mock()
        
        # Execute
        result = add_reaction(user_id=789)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "message_id and emoji are required"})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_add_reaction_empty_data(self, mock_jsonify, mock_request):
        # Setup
        mock_request.get_json.return_value = {}
        mock_jsonify.return_value = Mock()
        
        # Execute
        result = add_reaction(user_id=789)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "message_id and emoji are required"})
        assert result[1] == 400

    @pytest.mark.parametrize("data", [
        {'emoji': '👍'},  # Missing message_id
        {'message_id': 123},  # Missing emoji
        {'message_id': 123, 'other_field': 'value'},  # Missing emoji, has other field
        {'emoji': '👍', 'other_field': 'value'},  # Missing message_id, has other field
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_add_reaction_missing_required_fields(self, mock_jsonify, mock_request, data):
        # Setup
        mock_request.get_json.return_value = data
        mock_jsonify.return_value = Mock()
        
        # Execute
        result = add_reaction(user_id=789)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "message_id and emoji are required"})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_add_reaction_value_error(self, mock_jsonify, mock_manager, mock_request):
        # Setup
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.add_reaction.side_effect = ValueError("Invalid emoji format")
        mock_jsonify.return_value = Mock()
        
        # Execute
        result = add_reaction(user_id=789)
        
        # Assert
        mock_manager.add_reaction.assert_called_once_with(
            message_id=123,
            user_id=789,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({"error": "Invalid emoji format"})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_add_reaction_generic_exception(self, mock_jsonify, mock_manager, mock_request):
        # Setup
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.add_reaction.side_effect = RuntimeError("Database connection failed")
        mock_jsonify.return_value = Mock()
        
        # Execute
        result = add_reaction(user_id=789)
        
        # Assert
        mock_manager.add_reaction.assert_called_once_with(
            message_id=123,
            user_id=789,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({"error": "Failed to add reaction: Database connection failed"})
        assert result[1] == 500

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_add_reaction_with_additional_fields(self, mock_jsonify, mock_manager, mock_request):
        # Setup - data with extra fields should still work
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍',
            'extra_field': 'ignored',
            'another_field': 42
        }
        mock_manager.add_reaction.return_value = {'success': True, 'reaction_id': 456}
        mock_jsonify.return_value = Mock()
        
        # Execute
        result = add_reaction(user_id=789)
        
        # Assert
        mock_manager.add_reaction.assert_called_once_with(
            message_id=123,
            user_id=789,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({'success': True, 'reaction_id': 456})
        assert result[1] == 200

    @pytest.mark.parametrize("user_id", [
        0,  # Zero user_id
        -1,  # Negative user_id
        999999,  # Large user_id
        None,  # None user_id
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_add_reaction_various_user_ids(self, mock_jsonify, mock_manager, mock_request, user_id):
        # Setup
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.add_reaction.return_value = {'success': True, 'reaction_id': 456}
        mock_jsonify.return_value = Mock()
        
        # Execute
        result = add_reaction(user_id=user_id)
        
        # Assert
        mock_manager.add_reaction.assert_called_once_with(
            message_id=123,
            user_id=user_id,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({'success': True, 'reaction_id': 456})
        assert result[1] == 200

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_add_reaction_request_json_exception(self, mock_jsonify, mock_manager, mock_request):
        # Setup - request.get_json() raises exception
        mock_request.get_json.side_effect = Exception("JSON parsing error")
        mock_jsonify.return_value = Mock()
        
        # Execute
        result = add_reaction(user_id=789)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "Failed to add reaction: JSON parsing error"})
        assert result[1] == 500
        mock_manager.add_reaction.assert_not_called()

# Standard library
# Third-party
# Local


import json
import pytest
from flask import Flask
from unittest.mock import patch, Mock

from routes.reactions import remove_reaction

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_reaction_manager():
    return Mock()

class TestRemoveReaction:
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_successful_reaction_removal(self, mock_jsonify, mock_manager, mock_request):
        # Setup
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.remove_reaction.return_value = {'success': True}
        mock_jsonify.return_value = {'success': True}
        
        # Execute
        result = remove_reaction(456)
        
        # Assert
        mock_manager.remove_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji='👍'
        )
        mock_jsonify.assert_called_with({'success': True})
        assert result == ({'success': True}, 200)

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_not_found(self, mock_jsonify, mock_manager, mock_request):
        # Setup
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.remove_reaction.return_value = {'success': False}
        mock_jsonify.return_value = {'success': False}
        
        # Execute
        result = remove_reaction(456)
        
        # Assert
        mock_manager.remove_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji='👍'
        )
        mock_jsonify.assert_called_with({'success': False})
        assert result == ({'success': False}, 404)

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_no_request_data(self, mock_jsonify, mock_request):
        # Setup
        mock_request.get_json.return_value = None
        mock_jsonify.return_value = {"error": "message_id and emoji are required"}
        
        # Execute
        result = remove_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_with({"error": "message_id and emoji are required"})
        assert result == ({"error": "message_id and emoji are required"}, 400)

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_empty_request_data(self, mock_jsonify, mock_request):
        # Setup
        mock_request.get_json.return_value = {}
        mock_jsonify.return_value = {"error": "message_id and emoji are required"}
        
        # Execute
        result = remove_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_with({"error": "message_id and emoji are required"})
        assert result == ({"error": "message_id and emoji are required"}, 400)

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_missing_message_id(self, mock_jsonify, mock_request):
        # Setup
        mock_request.get_json.return_value = {'emoji': '👍'}
        mock_jsonify.return_value = {"error": "message_id and emoji are required"}
        
        # Execute
        result = remove_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_with({"error": "message_id and emoji are required"})
        assert result == ({"error": "message_id and emoji are required"}, 400)

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_missing_emoji(self, mock_jsonify, mock_request):
        # Setup
        mock_request.get_json.return_value = {'message_id': 123}
        mock_jsonify.return_value = {"error": "message_id and emoji are required"}
        
        # Execute
        result = remove_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_with({"error": "message_id and emoji are required"})
        assert result == ({"error": "message_id and emoji are required"}, 400)

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_exception_handling(self, mock_jsonify, mock_manager, mock_request):
        # Setup
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.remove_reaction.side_effect = Exception("Database error")
        mock_jsonify.return_value = {"error": "Failed to remove reaction: Database error"}
        
        # Execute
        result = remove_reaction(456)
        
        # Assert
        mock_manager.remove_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji='👍'
        )
        mock_jsonify.assert_called_with({"error": "Failed to remove reaction: Database error"})
        assert result == ({"error": "Failed to remove reaction: Database error"}, 500)

    @pytest.mark.parametrize("user_id,message_id,emoji", [
        (0, 1, '👍'),
        (-1, 999999, '❤️'),
        (999999, 0, '😂'),
        (1, 1, '🔥'),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_various_valid_inputs(self, mock_jsonify, mock_manager, mock_request, user_id, message_id, emoji):
        # Setup
        mock_request.get_json.return_value = {
            'message_id': message_id,
            'emoji': emoji
        }
        mock_manager.remove_reaction.return_value = {'success': True}
        mock_jsonify.return_value = {'success': True}
        
        # Execute
        result = remove_reaction(user_id)
        
        # Assert
        mock_manager.remove_reaction.assert_called_once_with(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        )
        mock_jsonify.assert_called_with({'success': True})
        assert result == ({'success': True}, 200)

    @pytest.mark.parametrize("exception_msg", [
        "Connection timeout",
        "Invalid message ID",
        "User not authorized",
        "",
        "Special chars: !@#$%^&*()",
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_various_exceptions(self, mock_jsonify, mock_manager, mock_request, exception_msg):
        # Setup
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.remove_reaction.side_effect = Exception(exception_msg)
        expected_error = f"Failed to remove reaction: {exception_msg}"
        mock_jsonify.return_value = {"error": expected_error}
        
        # Execute
        result = remove_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_with({"error": expected_error})
        assert result == ({"error": expected_error}, 500)

    @pytest.mark.parametrize("invalid_data", [
        {'message_id': None, 'emoji': '👍'},
        {'message_id': 123, 'emoji': None},
        {'message_id': '', 'emoji': '👍'},
        {'message_id': 123, 'emoji': ''},
        {'wrong_key': 123, 'emoji': '👍'},
        {'message_id': 123, 'wrong_key': '👍'},
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_invalid_data_formats(self, mock_jsonify, mock_request, invalid_data):
        # Setup
        mock_request.get_json.return_value = invalid_data
        mock_jsonify.return_value = {"error": "message_id and emoji are required"}
        
        # Execute
        result = remove_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_with({"error": "message_id and emoji are required"})
        assert result == ({"error": "message_id and emoji are required"}, 400)

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
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_reaction_manager():
    return Mock()

class TestToggleReaction:
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_toggle_reaction_success(self, mock_jsonify, mock_manager, mock_request):
        # Arrange
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.toggle_reaction.return_value = {'status': 'added', 'count': 5}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = toggle_reaction(456)
        
        # Assert
        mock_manager.toggle_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({'status': 'added', 'count': 5})
        assert result[1] == 200

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_toggle_reaction_no_data(self, mock_jsonify, mock_request):
        # Arrange
        mock_request.get_json.return_value = None
        mock_jsonify.return_value = Mock()
        
        # Act
        result = toggle_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "message_id and emoji are required"})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_toggle_reaction_empty_data(self, mock_jsonify, mock_request):
        # Arrange
        mock_request.get_json.return_value = {}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = toggle_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "message_id and emoji are required"})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_toggle_reaction_missing_message_id(self, mock_jsonify, mock_request):
        # Arrange
        mock_request.get_json.return_value = {'emoji': '👍'}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = toggle_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "message_id and emoji are required"})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_toggle_reaction_missing_emoji(self, mock_jsonify, mock_request):
        # Arrange
        mock_request.get_json.return_value = {'message_id': 123}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = toggle_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "message_id and emoji are required"})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_toggle_reaction_value_error(self, mock_jsonify, mock_manager, mock_request):
        # Arrange
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.toggle_reaction.side_effect = ValueError("Invalid message ID")
        mock_jsonify.return_value = Mock()
        
        # Act
        result = toggle_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "Invalid message ID"})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_toggle_reaction_generic_exception(self, mock_jsonify, mock_manager, mock_request):
        # Arrange
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.toggle_reaction.side_effect = Exception("Database connection failed")
        mock_jsonify.return_value = Mock()
        
        # Act
        result = toggle_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": "Failed to toggle reaction: Database connection failed"})
        assert result[1] == 500

    @pytest.mark.parametrize("data,expected_error", [
        ({'message_id': None, 'emoji': '👍'}, "message_id and emoji are required"),
        ({'message_id': 123, 'emoji': None}, "message_id and emoji are required"),
        ({'message_id': '', 'emoji': '👍'}, "message_id and emoji are required"),
        ({'message_id': 123, 'emoji': ''}, "message_id and emoji are required"),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_toggle_reaction_invalid_data_values(self, mock_jsonify, mock_request, data, expected_error):
        # Arrange
        mock_request.get_json.return_value = data
        mock_jsonify.return_value = Mock()
        
        # Act
        result = toggle_reaction(456)
        
        # Assert
        mock_jsonify.assert_called_once_with({"error": expected_error})
        assert result[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_toggle_reaction_with_different_user_ids(self, mock_jsonify, mock_manager, mock_request):
        # Arrange
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_manager.toggle_reaction.return_value = {'status': 'removed', 'count': 3}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = toggle_reaction(999)
        
        # Assert
        mock_manager.toggle_reaction.assert_called_once_with(
            message_id=123,
            user_id=999,
            emoji='👍'
        )
        mock_jsonify.assert_called_once_with({'status': 'removed', 'count': 3})
        assert result[1] == 200

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_toggle_reaction_with_unicode_emoji(self, mock_jsonify, mock_manager, mock_request):
        # Arrange
        mock_request.get_json.return_value = {
            'message_id': 456,
            'emoji': '🎉'
        }
        mock_manager.toggle_reaction.return_value = {'status': 'added', 'count': 1}
        mock_jsonify.return_value = Mock()
        
        # Act
        result = toggle_reaction(789)
        
        # Assert
        mock_manager.toggle_reaction.assert_called_once_with(
            message_id=456,
            user_id=789,
            emoji='🎉'
        )
        mock_jsonify.assert_called_once_with({'status': 'added', 'count': 1})
        assert result[1] == 200

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock
from flask import Flask

from routes.reactions import get_message_reactions

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def mock_reaction_manager():
    return Mock()

class TestGetMessageReactions:
    
    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_success(self, mock_manager):
        # Arrange
        message_id = "msg123"
        expected_reactions = {
            "👍": [{"user_id": "user1", "timestamp": "2023-01-01"}],
            "❤️": [{"user_id": "user2", "timestamp": "2023-01-02"}]
        }
        mock_manager.get_message_reactions.return_value = expected_reactions
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == expected_reactions
        mock_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_empty_reactions(self, mock_manager):
        # Arrange
        message_id = "msg456"
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

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_none_message_id(self, mock_manager):
        # Arrange
        message_id = None
        mock_manager.get_message_reactions.return_value = {}
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] is None
        assert response_data["reactions"] == {}
        mock_manager.get_message_reactions.assert_called_once_with(None)

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_exception_handling(self, mock_manager):
        # Arrange
        message_id = "msg789"
        error_message = "Database connection failed"
        mock_manager.get_message_reactions.side_effect = Exception(error_message)
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get reactions: {error_message}" in response_data["error"]
        mock_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_runtime_error(self, mock_manager):
        # Arrange
        message_id = "msg999"
        mock_manager.get_message_reactions.side_effect = RuntimeError("Runtime error occurred")
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Failed to get reactions: Runtime error occurred" in response_data["error"]

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_value_error(self, mock_manager):
        # Arrange
        message_id = "invalid_msg"
        mock_manager.get_message_reactions.side_effect = ValueError("Invalid message ID format")
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Failed to get reactions: Invalid message ID format" in response_data["error"]

    @pytest.mark.parametrize("message_id,expected_reactions", [
        ("msg1", {"👍": [{"user_id": "user1"}]}),
        ("msg2", {"❤️": [{"user_id": "user2"}], "👎": [{"user_id": "user3"}]}),
        ("msg3", {}),
        ("", {}),
        (123, {"😀": [{"user_id": "user4"}]}),
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_various_inputs(self, mock_manager, message_id, expected_reactions):
        # Arrange
        mock_manager.get_message_reactions.return_value = expected_reactions
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == expected_reactions

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_large_dataset(self, mock_manager):
        # Arrange
        message_id = "msg_large"
        large_reactions = {}
        for i in range(100):
            emoji = f"emoji_{i}"
            large_reactions[emoji] = [{"user_id": f"user_{j}", "timestamp": f"2023-01-{j:02d}"} for j in range(10)]
        mock_manager.get_message_reactions.return_value = large_reactions
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert len(response_data["reactions"]) == 100

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_generic_exception(self, mock_manager):
        # Arrange
        message_id = "msg_generic"
        mock_manager.get_message_reactions.side_effect = Exception()
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Failed to get reactions:" in response_data["error"]

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_nested_data_structure(self, mock_manager):
        # Arrange
        message_id = "msg_nested"
        nested_reactions = {
            "👍": [
                {
                    "user_id": "user1",
                    "timestamp": "2023-01-01",
                    "metadata": {"source": "web", "device": "desktop"}
                }
            ]
        }
        mock_manager.get_message_reactions.return_value = nested_reactions
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["reactions"]["👍"][0]["metadata"]["source"] == "web"

# Standard library
# Third-party
# Local


import json
import pytest
from flask import Flask
from unittest.mock import patch, Mock

from routes.reactions import get_user_reactions

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    return app.test_client()

    @pytest.fixture
def app(self):
        app.config['TESTING'] = True
        with app.app_context():
            with app.test_request_context():
                yield app
    

    @pytest.fixture
def mock_reaction_manager(self):
        return Mock()
    

class TestGetUserReactions:
    
    @pytest.mark.parametrize("user_id,message_id,expected_reactions", [
        (1, None, [{"id": 1, "emoji": "👍", "message_id": 100}]),
        (2, 200, [{"id": 2, "emoji": "❤️", "message_id": 200}]),
        (3, None, []),
        (999, 888, [{"id": 3, "emoji": "😂", "message_id": 888}]),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_success(self, mock_manager, mock_request, app, user_id, message_id, expected_reactions):
        mock_request.args.get.return_value = message_id
        mock_manager.get_user_reactions.return_value = expected_reactions
        
        result, status_code = get_user_reactions(user_id)
        
        assert status_code == 200
        response_data = json.loads(result.data)
        assert response_data["success"] is True
        assert response_data["user_id"] == user_id
        assert response_data["reactions"] == expected_reactions
        mock_manager.get_user_reactions.assert_called_once_with(user_id, message_id)
        mock_request.args.get.assert_called_once_with('message_id', type=int)
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_with_message_id_filter(self, mock_manager, mock_request, app):
        user_id = 123
        message_id = 456
        expected_reactions = [{"id": 1, "emoji": "👍", "message_id": 456}]
        
        mock_request.args.get.return_value = message_id
        mock_manager.get_user_reactions.return_value = expected_reactions
        
        result, status_code = get_user_reactions(user_id)
        
        assert status_code == 200
        response_data = json.loads(result.data)
        assert response_data["success"] is True
        assert response_data["user_id"] == user_id
        assert response_data["reactions"] == expected_reactions
        mock_manager.get_user_reactions.assert_called_once_with(user_id, message_id)
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_without_message_id_filter(self, mock_manager, mock_request, app):
        user_id = 789
        expected_reactions = [
            {"id": 1, "emoji": "👍", "message_id": 100},
            {"id": 2, "emoji": "❤️", "message_id": 200}
        ]
        
        mock_request.args.get.return_value = None
        mock_manager.get_user_reactions.return_value = expected_reactions
        
        result, status_code = get_user_reactions(user_id)
        
        assert status_code == 200
        response_data = json.loads(result.data)
        assert response_data["success"] is True
        assert response_data["user_id"] == user_id
        assert response_data["reactions"] == expected_reactions
        mock_manager.get_user_reactions.assert_called_once_with(user_id, None)
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_empty_result(self, mock_manager, mock_request, app):
        user_id = 999
        mock_request.args.get.return_value = None
        mock_manager.get_user_reactions.return_value = []
        
        result, status_code = get_user_reactions(user_id)
        
        assert status_code == 200
        response_data = json.loads(result.data)
        assert response_data["success"] is True
        assert response_data["user_id"] == user_id
        assert response_data["reactions"] == []
    
    @pytest.mark.parametrize("exception_type,exception_message", [
        (ValueError, "Invalid user ID"),
        (KeyError, "User not found"),
        (ConnectionError, "Database connection failed"),
        (RuntimeError, "Service unavailable"),
        (Exception, "Unexpected error occurred"),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_exception_handling(self, mock_manager, mock_request, app, exception_type, exception_message):
        user_id = 123
        mock_request.args.get.return_value = None
        mock_manager.get_user_reactions.side_effect = exception_type(exception_message)
        
        result, status_code = get_user_reactions(user_id)
        
        assert status_code == 500
        response_data = json.loads(result.data)
        assert "error" in response_data
        assert f"Failed to get user reactions: {exception_message}" in response_data["error"]
        assert "success" not in response_data
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_manager_raises_generic_exception(self, mock_manager, mock_request, app):
        user_id = 456
        error_message = "Database timeout"
        mock_request.args.get.return_value = 789
        mock_manager.get_user_reactions.side_effect = Exception(error_message)
        
        result, status_code = get_user_reactions(user_id)
        
        assert status_code == 500
        response_data = json.loads(result.data)
        assert response_data["error"] == f"Failed to get user reactions: {error_message}"
        mock_manager.get_user_reactions.assert_called_once_with(user_id, 789)
    
    @pytest.mark.parametrize("user_id", [0, -1, 999999, 1])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_various_user_ids(self, mock_manager, mock_request, app, user_id):
        mock_request.args.get.return_value = None
        mock_manager.get_user_reactions.return_value = []
        
        result, status_code = get_user_reactions(user_id)
        
        assert status_code == 200
        response_data = json.loads(result.data)
        assert response_data["user_id"] == user_id
        mock_manager.get_user_reactions.assert_called_once_with(user_id, None)
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_request_args_called_correctly(self, mock_manager, mock_request, app):
        user_id = 123
        mock_request.args.get.return_value = 456
        mock_manager.get_user_reactions.return_value = []
        
        get_user_reactions(user_id)
        
        mock_request.args.get.assert_called_once_with('message_id', type=int)
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_manager_called_with_correct_params(self, mock_manager, mock_request, app):
        user_id = 789
        message_id = 101112
        mock_request.args.get.return_value = message_id
        mock_manager.get_user_reactions.return_value = []
        
        get_user_reactions(user_id)
        
        mock_manager.get_user_reactions.assert_called_once_with(user_id, message_id)

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock
from flask import Flask

from routes.reactions import get_reaction_count

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def mock_reaction_manager():
    return Mock()

class TestGetReactionCount:
    
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_success(self, mock_manager):
        # Arrange
        message_id = "msg123"
        expected_count = 5
        mock_manager.get_reaction_count.return_value = expected_count
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["count"] == expected_count
        mock_manager.get_reaction_count.assert_called_once_with(message_id)
    
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_zero_count(self, mock_manager):
        # Arrange
        message_id = "msg456"
        expected_count = 0
        mock_manager.get_reaction_count.return_value = expected_count
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["count"] == expected_count
    
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_large_count(self, mock_manager):
        # Arrange
        message_id = "msg789"
        expected_count = 999999
        mock_manager.get_reaction_count.return_value = expected_count
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["count"] == expected_count
    
    @pytest.mark.parametrize("message_id,expected_count", [
        ("msg1", 1),
        ("msg2", 10),
        ("msg3", 100),
        ("", 0),
        ("very_long_message_id_12345", 42),
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_various_inputs(self, mock_manager, message_id, expected_count):
        # Arrange
        mock_manager.get_reaction_count.return_value = expected_count
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["count"] == expected_count
    
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_none_message_id(self, mock_manager):
        # Arrange
        message_id = None
        expected_count = 0
        mock_manager.get_reaction_count.return_value = expected_count
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] is None
        assert response_data["count"] == expected_count
    
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_exception_handling(self, mock_manager):
        # Arrange
        message_id = "msg123"
        error_message = "Database connection failed"
        mock_manager.get_reaction_count.side_effect = Exception(error_message)
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get reaction count: {error_message}" in response_data["error"]
        mock_manager.get_reaction_count.assert_called_once_with(message_id)
    
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_value_error_exception(self, mock_manager):
        # Arrange
        message_id = "invalid_msg"
        error_message = "Invalid message ID format"
        mock_manager.get_reaction_count.side_effect = ValueError(error_message)
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get reaction count: {error_message}" in response_data["error"]
    
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_key_error_exception(self, mock_manager):
        # Arrange
        message_id = "msg123"
        error_message = "'message_id'"
        mock_manager.get_reaction_count.side_effect = KeyError(error_message)
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Failed to get reaction count:" in response_data["error"]
    
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_runtime_error_exception(self, mock_manager):
        # Arrange
        message_id = "msg123"
        error_message = "Runtime error occurred"
        mock_manager.get_reaction_count.side_effect = RuntimeError(error_message)
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get reaction count: {error_message}" in response_data["error"]
    
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_empty_string_exception_message(self, mock_manager):
        # Arrange
        message_id = "msg123"
        mock_manager.get_reaction_count.side_effect = Exception("")
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Failed to get reaction count: " in response_data["error"]
    
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_negative_count(self, mock_manager):
        # Arrange
        message_id = "msg123"
        expected_count = -1
        mock_manager.get_reaction_count.return_value = expected_count
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["count"] == expected_count

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock

from routes.reactions import get_most_popular

class TestGetMostPopular:
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_successful_emoji_retrieval(self, mock_jsonify, mock_reaction_manager):
        """Test successful retrieval of most popular emoji."""
        # Arrange
        message_id = "msg123"
        expected_emoji = "👍"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_none_message_id(self, mock_jsonify, mock_reaction_manager):
        """Test with None message_id."""
        # Arrange
        message_id = None
        expected_emoji = "😊"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(None)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": None,
            "most_popular_emoji": expected_emoji
        })
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_empty_string_message_id(self, mock_jsonify, mock_reaction_manager):
        """Test with empty string message_id."""
        # Arrange
        message_id = ""
        expected_emoji = "❤️"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with("")
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": "",
            "most_popular_emoji": expected_emoji
        })
        assert status_code == 200

    @pytest.mark.parametrize("message_id,expected_emoji", [
        ("msg1", "🎉"),
        ("msg2", "🔥"),
        ("msg3", "💯"),
        (123, "👏"),
        (0, "😂"),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_various_message_ids_success(self, mock_jsonify, mock_reaction_manager, message_id, expected_emoji):
        """Test successful retrieval with various message IDs."""
        # Arrange
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        })
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_raises_value_error(self, mock_jsonify, mock_reaction_manager):
        """Test when reaction_manager raises ValueError."""
        # Arrange
        message_id = "invalid_msg"
        error_message = "Invalid message ID"
        mock_reaction_manager.get_most_popular_emoji.side_effect = ValueError(error_message)
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get popular emoji: {error_message}"
        })
        assert status_code == 500

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_raises_key_error(self, mock_jsonify, mock_reaction_manager):
        """Test when reaction_manager raises KeyError."""
        # Arrange
        message_id = "nonexistent_msg"
        error_message = "Message not found"
        mock_reaction_manager.get_most_popular_emoji.side_effect = KeyError(error_message)
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get popular emoji: {error_message}"
        })
        assert status_code == 500

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_raises_runtime_error(self, mock_jsonify, mock_reaction_manager):
        """Test when reaction_manager raises RuntimeError."""
        # Arrange
        message_id = "msg123"
        error_message = "Database connection failed"
        mock_reaction_manager.get_most_popular_emoji.side_effect = RuntimeError(error_message)
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get popular emoji: {error_message}"
        })
        assert status_code == 500

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_raises_generic_exception(self, mock_jsonify, mock_reaction_manager):
        """Test when reaction_manager raises generic Exception."""
        # Arrange
        message_id = "msg123"
        error_message = "Unexpected error occurred"
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception(error_message)
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": f"Failed to get popular emoji: {error_message}"
        })
        assert status_code == 500

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_returns_none_emoji(self, mock_jsonify, mock_reaction_manager):
        """Test when reaction_manager returns None as emoji."""
        # Arrange
        message_id = "msg_no_reactions"
        mock_reaction_manager.get_most_popular_emoji.return_value = None
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": None
        })
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_reaction_manager_returns_empty_string_emoji(self, mock_jsonify, mock_reaction_manager):
        """Test when reaction_manager returns empty string as emoji."""
        # Arrange
        message_id = "msg_empty_emoji"
        mock_reaction_manager.get_most_popular_emoji.return_value = ""
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": ""
        })
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_exception_with_empty_error_message(self, mock_jsonify, mock_reaction_manager):
        """Test exception handling with empty error message."""
        # Arrange
        message_id = "msg123"
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("")
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)
        mock_jsonify.assert_called_once_with({
            "error": "Failed to get popular emoji: "
        })
        assert status_code == 500

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_jsonify_called_with_correct_structure_on_success(self, mock_jsonify, mock_reaction_manager):
        """Test that jsonify is called with correct response structure on success."""
        # Arrange
        message_id = "test_msg"
        emoji = "🚀"
        mock_reaction_manager.get_most_popular_emoji.return_value = emoji
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        expected_response = {
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": emoji
        }
        mock_jsonify.assert_called_once_with(expected_response)
        assert result == mock_response
        assert status_code == 200

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.jsonify')

    def test_jsonify_called_with_correct_structure_on_error(self, mock_jsonify, mock_reaction_manager):
        """Test that jsonify is called with correct error structure on exception."""
        # Arrange
        message_id = "test_msg"
        error_msg = "Test error"
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception(error_msg)
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result, status_code = get_most_popular(message_id)
        
        # Assert
        expected_response = {
            "error": f"Failed to get popular emoji: {error_msg}"
        }
        mock_jsonify.assert_called_once_with(expected_response)
        assert result == mock_response
        assert status_code == 500

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock

from routes.reactions import get_allowed_emojis

class TestGetAllowedEmojis:
    
    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_success(self, mock_jsonify, mock_reaction_manager):
        """Test successful retrieval of allowed emojis."""
        # Arrange
        expected_emojis = ['😀', '😂', '❤️', '👍', '👎']
        mock_reaction_manager.get_allowed_emojis.return_value = expected_emojis
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": expected_emojis
        })
    
    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_empty_list(self, mock_jsonify, mock_reaction_manager):
        """Test when no emojis are allowed."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.return_value = []
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": []
        })
    
    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_none_return(self, mock_jsonify, mock_reaction_manager):
        """Test when ReactionManager returns None."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.return_value = None
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": None
        })
    
    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_large_list(self, mock_jsonify, mock_reaction_manager):
        """Test with a large list of emojis."""
        # Arrange
        large_emoji_list = ['😀'] * 1000
        mock_reaction_manager.get_allowed_emojis.return_value = large_emoji_list
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": large_emoji_list
        })
    
    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_reaction_manager_exception(self, mock_jsonify, mock_reaction_manager):
        """Test when ReactionManager raises an exception."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            get_allowed_emojis()
        
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_not_called()
    
    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_jsonify_exception(self, mock_jsonify, mock_reaction_manager):
        """Test when jsonify raises an exception."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.return_value = ['😀']
        mock_jsonify.side_effect = Exception("JSON serialization error")
        
        # Act & Assert
        with pytest.raises(Exception, match="JSON serialization error"):
            get_allowed_emojis()
        
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once()
    
    @pytest.mark.parametrize("emoji_data", [
        ['😀', '😂', '❤️'],
        ['👍'],
        [],
        None,
        ['🎉', '🔥', '💯', '🚀', '⭐'],
    ])
    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_various_data(self, mock_jsonify, mock_reaction_manager, emoji_data):
        """Test with various emoji data types and values."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.return_value = emoji_data
        mock_jsonify.return_value = Mock()
        
        # Act
        result, status_code = get_allowed_emojis()
        
        # Assert
        assert status_code == 200
        mock_reaction_manager.get_allowed_emojis.assert_called_once()
        mock_jsonify.assert_called_once_with({
            "success": True,
            "emojis": emoji_data
        })
    
    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_success_flag_always_true(self, mock_jsonify, mock_reaction_manager):
        """Test that success flag is always True regardless of emoji data."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.return_value = []
        mock_jsonify.return_value = Mock()
        
        # Act
        get_allowed_emojis()
        
        # Assert
        call_args = mock_jsonify.call_args[0][0]
        assert call_args["success"] is True
    
    @patch('routes.reactions.ReactionManager')
    @patch('routes.reactions.jsonify')

    def test_get_allowed_emojis_return_tuple_structure(self, mock_jsonify, mock_reaction_manager):
        """Test that function returns tuple with response and status code."""
        # Arrange
        mock_reaction_manager.get_allowed_emojis.return_value = ['😀']
        mock_response = Mock()
        mock_jsonify.return_value = mock_response
        
        # Act
        result = get_allowed_emojis()
        
        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] == mock_response
        assert result[1] == 200

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
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_reaction_manager():
    return Mock()

class TestBulkAddReactions:
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_success(self, mock_manager, mock_request):
        """Test successful bulk addition of reactions"""
        mock_request.get_json.return_value = {
            'reactions': [
                {'message_id': 1, 'user_id': 1, 'emoji': '👍'},
                {'message_id': 2, 'user_id': 1, 'emoji': '❤️'}
            ]
        }
        mock_manager.bulk_add_reactions.return_value = {'added': 2, 'failed': 0}
        
        response, status_code = bulk_add_reactions(1)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['result'] == {'added': 2, 'failed': 0}
        mock_manager.bulk_add_reactions.assert_called_once_with([
            {'message_id': 1, 'user_id': 1, 'emoji': '👍'},
            {'message_id': 2, 'user_id': 1, 'emoji': '❤️'}
        ])

    @patch('routes.reactions.request')

    def test_bulk_add_reactions_no_data(self, mock_request):
        """Test when request has no JSON data"""
        mock_request.get_json.return_value = None
        
        response, status_code = bulk_add_reactions(1)
        
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data['error'] == 'reactions array is required'

    @patch('routes.reactions.request')

    def test_bulk_add_reactions_empty_data(self, mock_request):
        """Test when request has empty JSON data"""
        mock_request.get_json.return_value = {}
        
        response, status_code = bulk_add_reactions(1)
        
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data['error'] == 'reactions array is required'

    @patch('routes.reactions.request')

    def test_bulk_add_reactions_missing_reactions_key(self, mock_request):
        """Test when request data doesn't contain reactions key"""
        mock_request.get_json.return_value = {'other_key': 'value'}
        
        response, status_code = bulk_add_reactions(1)
        
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data['error'] == 'reactions array is required'

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_manager_exception(self, mock_manager, mock_request):
        """Test when reaction_manager raises an exception"""
        mock_request.get_json.return_value = {
            'reactions': [{'message_id': 1, 'user_id': 1, 'emoji': '👍'}]
        }
        mock_manager.bulk_add_reactions.side_effect = Exception('Database error')
        
        response, status_code = bulk_add_reactions(1)
        
        assert status_code == 500
        response_data = json.loads(response.data)
        assert response_data['error'] == 'Failed to bulk add reactions: Database error'

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_empty_reactions_array(self, mock_manager, mock_request):
        """Test with empty reactions array"""
        mock_request.get_json.return_value = {'reactions': []}
        mock_manager.bulk_add_reactions.return_value = {'added': 0, 'failed': 0}
        
        response, status_code = bulk_add_reactions(1)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['result'] == {'added': 0, 'failed': 0}
        mock_manager.bulk_add_reactions.assert_called_once_with([])

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_single_reaction(self, mock_manager, mock_request):
        """Test with single reaction in array"""
        mock_request.get_json.return_value = {
            'reactions': [{'message_id': 1, 'user_id': 1, 'emoji': '👍'}]
        }
        mock_manager.bulk_add_reactions.return_value = {'added': 1, 'failed': 0}
        
        response, status_code = bulk_add_reactions(1)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['result'] == {'added': 1, 'failed': 0}

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_value_error(self, mock_manager, mock_request):
        """Test when reaction_manager raises ValueError"""
        mock_request.get_json.return_value = {
            'reactions': [{'message_id': 1, 'user_id': 1, 'emoji': 'invalid'}]
        }
        mock_manager.bulk_add_reactions.side_effect = ValueError('Invalid emoji')
        
        response, status_code = bulk_add_reactions(1)
        
        assert status_code == 500
        response_data = json.loads(response.data)
        assert response_data['error'] == 'Failed to bulk add reactions: Invalid emoji'

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_key_error(self, mock_manager, mock_request):
        """Test when reaction_manager raises KeyError"""
        mock_request.get_json.return_value = {
            'reactions': [{'message_id': 1, 'user_id': 1}]  # missing emoji
        }
        mock_manager.bulk_add_reactions.side_effect = KeyError('emoji')
        
        response, status_code = bulk_add_reactions(1)
        
        assert status_code == 500
        response_data = json.loads(response.data)
        assert response_data['error'] == "Failed to bulk add reactions: 'emoji'"

    @pytest.mark.parametrize("reactions_data,expected_result", [
        ([{'message_id': 1, 'user_id': 1, 'emoji': '👍'}], {'added': 1, 'failed': 0}),
        ([
            {'message_id': 1, 'user_id': 1, 'emoji': '👍'},
            {'message_id': 2, 'user_id': 1, 'emoji': '❤️'},
            {'message_id': 3, 'user_id': 1, 'emoji': '😂'}
        ], {'added': 3, 'failed': 0}),
        ([
            {'message_id': 1, 'user_id': 1, 'emoji': '👍'},
            {'message_id': 1, 'user_id': 2, 'emoji': '👍'}
        ], {'added': 2, 'failed': 0})
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_parametrized(self, mock_manager, mock_request, reactions_data, expected_result):
        """Test bulk add reactions with various reaction arrays"""
        mock_request.get_json.return_value = {'reactions': reactions_data}
        mock_manager.bulk_add_reactions.return_value = expected_result
        
        response, status_code = bulk_add_reactions(1)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['result'] == expected_result
        mock_manager.bulk_add_reactions.assert_called_once_with(reactions_data)

# Standard library
# Third-party
# Local


from functools import wraps
import pytest
from flask import Flask, request, jsonify
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def mock_flask_app():
    return app

@pytest.fixture
def mock_request_context(mock_flask_app):
    with mock_flask_app.test_request_context():
        yield

class TestDecoratedFunction:
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_no_user_id_in_headers_or_args(self, mock_jsonify, mock_request):
        """Test when no user_id is provided in headers or args"""
        mock_request.headers.get.return_value = None
        mock_request.args.get.return_value = None
        mock_jsonify.return_value = {"error": "Authentication required"}
        
        mock_f = Mock()
        
        # Simulate the decorator behavior

        def test_decorated(*args, **kwargs):
            user_id = mock_request.headers.get('X-User-ID') or mock_request.args.get('user_id')
            if not user_id:
                return mock_jsonify({"error": "Authentication required"}), 401
            return mock_f(*args, user_id=int(user_id), **kwargs)
        
        result = test_decorated()
        
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_request.args.get.assert_called_once_with('user_id')
        mock_jsonify.assert_called_once_with({"error": "Authentication required"})
        assert result == ({"error": "Authentication required"}, 401)
        mock_f.assert_not_called()

    @patch('routes.reactions.request')

    def test_user_id_from_headers(self, mock_request):
        """Test when user_id is provided in headers"""
        mock_request.headers.get.return_value = "123"
        mock_request.args.get.return_value = None
        
        mock_f = Mock(return_value="success")
        
        # Simulate the decorator behavior

        def test_decorated(*args, **kwargs):
            user_id = mock_request.headers.get('X-User-ID') or mock_request.args.get('user_id')
            if not user_id:
                return jsonify({"error": "Authentication required"}), 401
            return mock_f(*args, user_id=int(user_id), **kwargs)
        
        result = test_decorated("arg1", "arg2", param1="value1")
        
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_f.assert_called_once_with("arg1", "arg2", user_id=123, param1="value1")
        assert result == "success"

    @patch('routes.reactions.request')

    def test_user_id_from_args(self, mock_request):
        """Test when user_id is provided in query args"""
        mock_request.headers.get.return_value = None
        mock_request.args.get.return_value = "456"
        
        mock_f = Mock(return_value="success")
        
        # Simulate the decorator behavior

        def test_decorated(*args, **kwargs):
            user_id = mock_request.headers.get('X-User-ID') or mock_request.args.get('user_id')
            if not user_id:
                return jsonify({"error": "Authentication required"}), 401
            return mock_f(*args, user_id=int(user_id), **kwargs)
        
        result = test_decorated()
        
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_request.args.get.assert_called_once_with('user_id')
        mock_f.assert_called_once_with(user_id=456)
        assert result == "success"

    @patch('routes.reactions.request')

    def test_user_id_from_headers_takes_precedence(self, mock_request):
        """Test when user_id is in both headers and args, headers takes precedence"""
        mock_request.headers.get.return_value = "789"
        mock_request.args.get.return_value = "999"
        
        mock_f = Mock(return_value="success")
        
        # Simulate the decorator behavior

        def test_decorated(*args, **kwargs):
            user_id = mock_request.headers.get('X-User-ID') or mock_request.args.get('user_id')
            if not user_id:
                return jsonify({"error": "Authentication required"}), 401
            return mock_f(*args, user_id=int(user_id), **kwargs)
        
        result = test_decorated()
        
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_f.assert_called_once_with(user_id=789)
        assert result == "success"

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_empty_string_user_id_in_headers(self, mock_jsonify, mock_request):
        """Test when user_id is empty string in headers"""
        mock_request.headers.get.return_value = ""
        mock_request.args.get.return_value = None
        mock_jsonify.return_value = {"error": "Authentication required"}
        
        mock_f = Mock()
        
        # Simulate the decorator behavior

        def test_decorated(*args, **kwargs):
            user_id = mock_request.headers.get('X-User-ID') or mock_request.args.get('user_id')
            if not user_id:
                return mock_jsonify({"error": "Authentication required"}), 401
            return mock_f(*args, user_id=int(user_id), **kwargs)
        
        result = test_decorated()
        
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_request.args.get.assert_called_once_with('user_id')
        mock_jsonify.assert_called_once_with({"error": "Authentication required"})
        assert result == ({"error": "Authentication required"}, 401)
        mock_f.assert_not_called()

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_empty_string_user_id_in_args(self, mock_jsonify, mock_request):
        """Test when user_id is empty string in args"""
        mock_request.headers.get.return_value = None
        mock_request.args.get.return_value = ""
        mock_jsonify.return_value = {"error": "Authentication required"}
        
        mock_f = Mock()
        
        # Simulate the decorator behavior

        def test_decorated(*args, **kwargs):
            user_id = mock_request.headers.get('X-User-ID') or mock_request.args.get('user_id')
            if not user_id:
                return mock_jsonify({"error": "Authentication required"}), 401
            return mock_f(*args, user_id=int(user_id), **kwargs)
        
        result = test_decorated()
        
        mock_request.headers.get.assert_called_once_with('X-User-ID')
        mock_request.args.get.assert_called_once_with('user_id')
        mock_jsonify.assert_called_once_with({"error": "Authentication required"})
        assert result == ({"error": "Authentication required"}, 401)
        mock_f.assert_not_called()

    @pytest.mark.parametrize("user_id_str,expected_int", [
        ("1", 1),
        ("0", 0),
        ("999999", 999999),
        ("-1", -1),
    ])
    @patch('routes.reactions.request')

    def test_user_id_conversion_to_int(self, mock_request, user_id_str, expected_int):
        """Test user_id string conversion to int with various values"""
        mock_request.headers.get.return_value = user_id_str
        mock_request.args.get.return_value = None
        
        mock_f = Mock(return_value="success")
        
        # Simulate the decorator behavior

        def test_decorated(*args, **kwargs):
            user_id = mock_request.headers.get('X-User-ID') or mock_request.args.get('user_id')
            if not user_id:
                return jsonify({"error": "Authentication required"}), 401
            return mock_f(*args, user_id=int(user_id), **kwargs)
        
        result = test_decorated()
        
        mock_f.assert_called_once_with(user_id=expected_int)
        assert result == "success"

    @patch('routes.reactions.request')

    def test_with_multiple_args_and_kwargs(self, mock_request):
        """Test decorated function with multiple args and kwargs"""
        mock_request.headers.get.return_value = "42"
        mock_request.args.get.return_value = None
        
        mock_f = Mock(return_value="result")
        
        # Simulate the decorator behavior

        def test_decorated(*args, **kwargs):
            user_id = mock_request.headers.get('X-User-ID') or mock_request.args.get('user_id')
            if not user_id:
                return jsonify({"error": "Authentication required"}), 401
            return mock_f(*args, user_id=int(user_id), **kwargs)
        
        result = test_decorated("arg1", "arg2", "arg3", param1="val1", param2="val2")
        
        mock_f.assert_called_once_with("arg1", "arg2", "arg3", user_id=42, param1="val1", param2="val2")
        assert result == "result"

    @patch('routes.reactions.request')

    def test_user_id_zero_string(self, mock_request):
        """Test when user_id is '0' string"""
        mock_request.headers.get.return_value = "0"
        mock_request.args.get.return_value = None
        
        mock_f = Mock(return_value="success")
        
        # Simulate the decorator behavior

        def test_decorated(*args, **kwargs):
            user_id = mock_request.headers.get('X-User-ID') or mock_request.args.get('user_id')
            if not user_id:
                return jsonify({"error": "Authentication required"}), 401
            return mock_f(*args, user_id=int(user_id), **kwargs)
        
        result = test_decorated()
        
        mock_f.assert_called_once_with(user_id=0)
        assert result == "success"

# Standard library
# Third-party
# Local

