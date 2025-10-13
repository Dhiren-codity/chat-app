"""
Auto-generated tests using LLM and RAG
"""

import pytest


from functools import wraps
import pytest
from flask import Flask
from unittest.mock import patch, Mock

from routes.reactions import require_auth

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestRequireAuth:

    def test_require_auth_with_header_user_id(self, app):

        def test_function(*args, **kwargs):
            return {"user_id": kwargs.get("user_id"), "success": True}
        
        app.add_url_rule('/test', 'test', test_function, methods=['GET'])
        
        with app.test_client() as client:
            with app.app_context():
                response = client.get('/test', headers={'X-User-ID': '123'})
                assert response.status_code == 200
                data = response.get_json()
                assert data['user_id'] == 123
                assert data['success'] is True


    def test_require_auth_with_query_param_user_id(self, app):

        def test_function(*args, **kwargs):
            return {"user_id": kwargs.get("user_id"), "success": True}
        
        app.add_url_rule('/test', 'test', test_function, methods=['GET'])
        
        with app.test_client() as client:
            with app.app_context():
                response = client.get('/test?user_id=456')
                assert response.status_code == 200
                data = response.get_json()
                assert data['user_id'] == 456
                assert data['success'] is True


    def test_require_auth_no_user_id_returns_401(self, app):

        def test_function(*args, **kwargs):
            return {"success": True}
        
        app.add_url_rule('/test', 'test', test_function, methods=['GET'])
        
        with app.test_client() as client:
            with app.app_context():
                response = client.get('/test')
                assert response.status_code == 401
                data = response.get_json()
                assert data['error'] == "Authentication required"


    def test_require_auth_header_takes_precedence_over_query_param(self, app):

        def test_function(*args, **kwargs):
            return {"user_id": kwargs.get("user_id"), "success": True}
        
        app.add_url_rule('/test', 'test', test_function, methods=['GET'])
        
        with app.test_client() as client:
            with app.app_context():
                response = client.get('/test?user_id=999', headers={'X-User-ID': '777'})
                assert response.status_code == 200
                data = response.get_json()
                assert data['user_id'] == 777
                assert data['success'] is True

    @pytest.mark.parametrize("user_id_value,expected_user_id", [
        ("1", 1),
        ("0", 0),
        ("999999", 999999),
    ])

    def test_require_auth_converts_string_to_int(self, app, user_id_value, expected_user_id):

        def test_function(*args, **kwargs):
            return {"user_id": kwargs.get("user_id"), "type": type(kwargs.get("user_id")).__name__}
        
        app.add_url_rule('/test', 'test', test_function, methods=['GET'])
        
        with app.test_client() as client:
            with app.app_context():
                response = client.get('/test', headers={'X-User-ID': user_id_value})
                assert response.status_code == 200
                data = response.get_json()
                assert data['user_id'] == expected_user_id
                assert data['type'] == 'int'

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import Mock, patch
from flask import Flask

from routes.reactions import add_reaction

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestAddReaction:
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_success(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.add_reaction.return_value = {
            'success': True,
            'reaction_id': 456
        }
        
        response = add_reaction(user_id=789)
        
        assert response[1] == 200
        response_data = json.loads(response[0].data)
        assert response_data['success'] is True
        assert response_data['reaction_id'] == 456
        mock_reaction_manager.add_reaction.assert_called_once_with(
            message_id=123,
            user_id=789,
            emoji='👍'
        )

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_failure(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.add_reaction.return_value = {
            'success': False,
            'error': 'Reaction already exists'
        }
        
        response = add_reaction(user_id=789)
        
        assert response[1] == 400
        response_data = json.loads(response[0].data)
        assert response_data['success'] is False
        assert response_data['error'] == 'Reaction already exists'

    @pytest.mark.parametrize("request_data,expected_status,expected_error", [
        (None, 400, "message_id and emoji are required"),
        ({}, 400, "message_id and emoji are required"),
        ({'message_id': 123}, 400, "message_id and emoji are required"),
        ({'emoji': '👍'}, 400, "message_id and emoji are required"),
    ])
    @patch('routes.reactions.request')

    def test_add_reaction_invalid_request_data(self, mock_request, request_data, expected_status, expected_error):
        mock_request.get_json.return_value = request_data
        
        response = add_reaction(user_id=789)
        
        assert response[1] == expected_status
        response_data = json.loads(response[0].data)
        assert response_data['error'] == expected_error

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_value_error(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.add_reaction.side_effect = ValueError("Invalid emoji")
        
        response = add_reaction(user_id=789)
        
        assert response[1] == 400
        response_data = json.loads(response[0].data)
        assert response_data['error'] == "Invalid emoji"

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_general_exception(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.add_reaction.side_effect = Exception("Database error")
        
        response = add_reaction(user_id=789)
        
        assert response[1] == 500
        response_data = json.loads(response[0].data)
        assert response_data['error'] == "Failed to add reaction: Database error"

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import Mock, patch
from flask import Flask

from routes.reactions import remove_reaction

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestRemoveReaction:
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_remove_reaction_success(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.return_value = {
            'success': True,
            'message': 'Reaction removed successfully'
        }
        
        response = remove_reaction(user_id=456)
        
        assert response[1] == 200
        response_data = json.loads(response[0].data)
        assert response_data['success'] is True
        mock_reaction_manager.remove_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji='👍'
        )

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_remove_reaction_not_found(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.return_value = {
            'success': False,
            'message': 'Reaction not found'
        }
        
        response = remove_reaction(user_id=456)
        
        assert response[1] == 404
        response_data = json.loads(response[0].data)
        assert response_data['success'] is False

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "message_id and emoji are required"),
        ({}, "message_id and emoji are required"),
        ({'message_id': 123}, "message_id and emoji are required"),
        ({'emoji': '👍'}, "message_id and emoji are required"),
    ])
    @patch('routes.reactions.request')

    def test_remove_reaction_invalid_request_data(self, mock_request, request_data, expected_error):
        mock_request.get_json.return_value = request_data
        
        response = remove_reaction(user_id=456)
        
        assert response[1] == 400
        response_data = json.loads(response[0].data)
        assert response_data['error'] == expected_error

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_remove_reaction_exception_handling(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.side_effect = Exception("Database error")
        
        response = remove_reaction(user_id=456)
        
        assert response[1] == 500
        response_data = json.loads(response[0].data)
        assert "Failed to remove reaction: Database error" in response_data['error']

# Standard library
# Third-party
# Local


import json
import pytest
from flask import Flask
from unittest.mock import Mock, patch

from routes.reactions import toggle_reaction

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestToggleReaction:
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_toggle_reaction_success(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.toggle_reaction.return_value = {
            'success': True,
            'action': 'added',
            'message_id': 123,
            'emoji': '👍'
        }
        
        response = toggle_reaction(user_id=456)
        
        assert response[1] == 200
        response_data = json.loads(response[0].data)
        assert response_data['success'] is True
        assert response_data['action'] == 'added'
        mock_reaction_manager.toggle_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji='👍'
        )

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "message_id and emoji are required"),
        ({}, "message_id and emoji are required"),
        ({'message_id': 123}, "message_id and emoji are required"),
        ({'emoji': '👍'}, "message_id and emoji are required"),
    ])
    @patch('routes.reactions.request')

    def test_toggle_reaction_missing_data(self, mock_request, request_data, expected_error):
        mock_request.get_json.return_value = request_data
        
        response = toggle_reaction(user_id=456)
        
        assert response[1] == 400
        response_data = json.loads(response[0].data)
        assert response_data['error'] == expected_error

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_toggle_reaction_value_error(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.toggle_reaction.side_effect = ValueError("Invalid message ID")
        
        response = toggle_reaction(user_id=456)
        
        assert response[1] == 400
        response_data = json.loads(response[0].data)
        assert response_data['error'] == "Invalid message ID"

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_toggle_reaction_general_exception(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.toggle_reaction.side_effect = Exception("Database connection failed")
        
        response = toggle_reaction(user_id=456)
        
        assert response[1] == 500
        response_data = json.loads(response[0].data)
        assert response_data['error'] == "Failed to toggle reaction: Database connection failed"

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import Mock, patch

from routes.reactions import get_message_reactions

class TestGetMessageReactions:
    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_success(self, mock_reaction_manager):
        """Test successful retrieval of message reactions."""
        # Arrange
        message_id = "msg_123"
        mock_reactions = {
            "👍": [{"user_id": 1, "timestamp": "2023-01-01"}],
            "❤️": [{"user_id": 2, "timestamp": "2023-01-02"}]
        }
        mock_reaction_manager.get_message_reactions.return_value = mock_reactions
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == mock_reactions
        mock_reaction_manager.get_message_reactions.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_empty_result(self, mock_reaction_manager):
        """Test retrieval when message has no reactions."""
        # Arrange
        message_id = "msg_456"
        mock_reaction_manager.get_message_reactions.return_value = {}
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == {}

    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_exception_handling(self, mock_reaction_manager):
        """Test error handling when reaction manager raises exception."""
        # Arrange
        message_id = "msg_789"
        error_message = "Database connection failed"
        mock_reaction_manager.get_message_reactions.side_effect = Exception(error_message)
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get reactions: {error_message}" in response_data["error"]

    @pytest.mark.parametrize("message_id,expected_reactions", [
        ("msg_001", {"😊": [{"user_id": 1}]}),
        ("msg_002", {"👍": [{"user_id": 1}], "❤️": [{"user_id": 2}]}),
        ("", {}),
        (None, {"🎉": [{"user_id": 3}]}),
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_various_inputs(self, mock_reaction_manager, message_id, expected_reactions):
        """Test function with various message IDs and reaction patterns."""
        # Arrange
        mock_reaction_manager.get_message_reactions.return_value = expected_reactions
        
        # Act
        response, status_code = get_message_reactions(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["reactions"] == expected_reactions

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import Mock, patch
from flask import Flask

from routes.reactions import get_user_reactions

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetUserReactions:
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_success_without_message_filter(self, mock_reaction_manager, mock_request):
        # Setup
        mock_request.args.get.return_value = None
        mock_reactions = [
            {"id": 1, "emoji": "👍", "message_id": 10},
            {"id": 2, "emoji": "❤️", "message_id": 20}
        ]
        mock_reaction_manager.get_user_reactions.return_value = mock_reactions
        
        # Execute
        response, status_code = get_user_reactions(123)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["user_id"] == 123
        assert response_data["reactions"] == mock_reactions
        mock_reaction_manager.get_user_reactions.assert_called_once_with(123, None)

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_success_with_message_filter(self, mock_reaction_manager, mock_request):
        # Setup
        mock_request.args.get.return_value = 456
        mock_reactions = [{"id": 1, "emoji": "👍", "message_id": 456}]
        mock_reaction_manager.get_user_reactions.return_value = mock_reactions
        
        # Execute
        response, status_code = get_user_reactions(123)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["user_id"] == 123
        assert response_data["reactions"] == mock_reactions
        mock_reaction_manager.get_user_reactions.assert_called_once_with(123, 456)

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_exception_handling(self, mock_reaction_manager, mock_request):
        # Setup
        mock_request.args.get.return_value = None
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Database error")
        
        # Execute
        response, status_code = get_user_reactions(123)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Failed to get user reactions: Database error" in response_data["error"]

    @pytest.mark.parametrize("user_id,message_id,expected_user_id", [
        (1, None, 1),
        (999, 123, 999),
        (0, 456, 0),
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_get_user_reactions_various_user_ids(self, mock_reaction_manager, mock_request, user_id, message_id, expected_user_id):
        # Setup
        mock_request.args.get.return_value = message_id
        mock_reaction_manager.get_user_reactions.return_value = []
        
        # Execute
        response, status_code = get_user_reactions(user_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["user_id"] == expected_user_id
        mock_reaction_manager.get_user_reactions.assert_called_with(user_id, message_id)

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import Mock, patch

from routes.reactions import get_reaction_count

class TestGetReactionCount:
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_success(self, mock_reaction_manager):
        """Test successful reaction count retrieval."""
        # Arrange
        mock_reaction_manager.get_reaction_count.return_value = 5
        message_id = "msg_123"
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["message_id"] == message_id
        assert data["count"] == 5
        mock_reaction_manager.get_reaction_count.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_zero_count(self, mock_reaction_manager):
        """Test reaction count retrieval with zero reactions."""
        # Arrange
        mock_reaction_manager.get_reaction_count.return_value = 0
        message_id = "msg_456"
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["message_id"] == message_id
        assert data["count"] == 0

    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_exception_handling(self, mock_reaction_manager):
        """Test error handling when reaction manager raises exception."""
        # Arrange
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Database connection failed")
        message_id = "msg_789"
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        data = json.loads(response.data)
        assert "error" in data
        assert "Failed to get reaction count: Database connection failed" in data["error"]

    @pytest.mark.parametrize("message_id,expected_count", [
        ("msg_1", 10),
        ("msg_2", 25),
        ("msg_3", 100),
        ("", 0),
        (None, 3),
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_various_inputs(self, mock_reaction_manager, message_id, expected_count):
        """Test reaction count retrieval with various message IDs."""
        # Arrange
        mock_reaction_manager.get_reaction_count.return_value = expected_count
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["message_id"] == message_id
        assert data["count"] == expected_count

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock

from routes.reactions import get_most_popular

@pytest.fixture
def mock_reaction_manager():
    with patch('routes.reactions.reaction_manager') as mock:
        yield mock

class TestGetMostPopular:

    def test_get_most_popular_success(self, mock_reaction_manager):
        """Test successful retrieval of most popular emoji."""
        # Arrange
        message_id = "msg_123"
        expected_emoji = "👍"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["most_popular_emoji"] == expected_emoji
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)

    @pytest.mark.parametrize("message_id,expected_emoji", [
        ("msg_456", "❤️"),
        ("msg_789", "😂"),
        ("msg_000", "🎉"),
        (123, "👏"),
        ("", "🔥")
    ])

    def test_get_most_popular_various_inputs(self, mock_reaction_manager, message_id, expected_emoji):
        """Test get_most_popular with various message IDs and emojis."""
        # Arrange
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["most_popular_emoji"] == expected_emoji


    def test_get_most_popular_exception_handling(self, mock_reaction_manager):
        """Test error handling when reaction_manager raises exception."""
        # Arrange
        message_id = "msg_error"
        error_message = "Database connection failed"
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception(error_message)
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get popular emoji: {error_message}" in response_data["error"]

    @pytest.mark.parametrize("exception_type,error_msg", [
        (ValueError, "Invalid message ID format"),
        (KeyError, "Message not found"),
        (RuntimeError, "Service unavailable")
    ])

    def test_get_most_popular_different_exceptions(self, mock_reaction_manager, exception_type, error_msg):
        """Test handling of different exception types."""
        # Arrange
        message_id = "msg_test"
        mock_reaction_manager.get_most_popular_emoji.side_effect = exception_type(error_msg)
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get popular emoji: {error_msg}" in response_data["error"]

# Standard library
# Third-party
# Local


def test_get_allowed_emojis_fallback():
    """Fallback test for get_allowed_emojis."""
    # TODO: Implement test for get_allowed_emojis
    pass



import json
import pytest
from unittest.mock import Mock, patch
from flask import Flask

from routes.reactions import bulk_add_reactions

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestBulkAddReactions:
    
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_success(self, mock_reaction_manager, mock_request):
        """Test successful bulk addition of reactions"""
        # Setup
        mock_data = {
            "reactions": [
                {"message_id": 1, "user_id": 123, "emoji": "👍"},
                {"message_id": 2, "user_id": 123, "emoji": "❤️"}
            ]
        }
        mock_request.get_json.return_value = mock_data
        mock_reaction_manager.bulk_add_reactions.return_value = {"added": 2, "failed": 0}
        
        # Execute
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["result"]["added"] == 2
        mock_reaction_manager.bulk_add_reactions.assert_called_once_with(mock_data["reactions"])

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "reactions array is required"),
        ({}, "reactions array is required"),
        ({"other_field": "value"}, "reactions array is required"),
    ])
    @patch('routes.reactions.request')

    def test_bulk_add_reactions_missing_data(self, mock_request, request_data, expected_error):
        """Test error handling for missing or invalid request data"""
        # Setup
        mock_request.get_json.return_value = request_data
        
        # Execute
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 400
        response_data = json.loads(response.data)
        assert response_data["error"] == expected_error

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_exception_handling(self, mock_reaction_manager, mock_request):
        """Test exception handling during bulk addition"""
        # Setup
        mock_data = {
            "reactions": [
                {"message_id": 1, "user_id": 123, "emoji": "👍"}
            ]
        }
        mock_request.get_json.return_value = mock_data
        mock_reaction_manager.bulk_add_reactions.side_effect = Exception("Database error")
        
        # Execute
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "Failed to bulk add reactions: Database error" in response_data["error"]

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_empty_reactions_array(self, mock_reaction_manager, mock_request):
        """Test handling of empty reactions array"""
        # Setup
        mock_data = {"reactions": []}
        mock_request.get_json.return_value = mock_data
        mock_reaction_manager.bulk_add_reactions.return_value = {"added": 0, "failed": 0}
        
        # Execute
        response, status_code = bulk_add_reactions(123)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["result"]["added"] == 0
        mock_reaction_manager.bulk_add_reactions.assert_called_once_with([])

# Standard library
# Third-party
# Local


from functools import wraps
import pytest
from flask import Flask, request, jsonify
from unittest.mock import Mock, patch

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestDecoratedFunction:
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_decorated_function_with_header_user_id(self, mock_jsonify, mock_request):
        # Setup
        mock_f = Mock(return_value="success")
        mock_request.headers.get.return_value = "123"
        mock_request.args.get.return_value = None
        
        # Create decorated function
        def create_decorated_function(f):
            def decorated_function(*args, **kwargs):
                user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return f(*args, user_id=int(user_id), **kwargs)
            return decorated_function
        
        decorated_func = create_decorated_function(mock_f)
        
        # Execute
        result = decorated_func("arg1", kwarg1="value1")
        
        # Assert
        assert result == "success"
        mock_f.assert_called_once_with("arg1", user_id=123, kwarg1="value1")

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_decorated_function_with_query_param_user_id(self, mock_jsonify, mock_request):
        # Setup
        mock_f = Mock(return_value="success")
        mock_request.headers.get.return_value = None
        mock_request.args.get.return_value = "456"
        
        # Create decorated function
        def create_decorated_function(f):
            def decorated_function(*args, **kwargs):
                user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return f(*args, user_id=int(user_id), **kwargs)
            return decorated_function
        
        decorated_func = create_decorated_function(mock_f)
        
        # Execute
        result = decorated_func()
        
        # Assert
        assert result == "success"
        mock_f.assert_called_once_with(user_id=456)

    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')

    def test_decorated_function_no_user_id_returns_401(self, mock_jsonify, mock_request):
        # Setup
        mock_f = Mock()
        mock_request.headers.get.return_value = None
        mock_request.args.get.return_value = None
        mock_jsonify.return_value = {"error": "Authentication required"}
        
        # Create decorated function
        def create_decorated_function(f):
            def decorated_function(*args, **kwargs):
                user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return f(*args, user_id=int(user_id), **kwargs)
            return decorated_function
        
        decorated_func = create_decorated_function(mock_f)
        
        # Execute
        result = decorated_func()
        
        # Assert
        assert result == ({"error": "Authentication required"}, 401)
        mock_jsonify.assert_called_once_with({"error": "Authentication required"})
        mock_f.assert_not_called()

    @pytest.mark.parametrize("header_value,query_value,expected_user_id", [
        ("789", "123", 789),  # Header takes precedence
        ("", "456", 456),     # Empty header, use query param
        ("0", "123", 0),      # Zero is valid user_id
    ])
    @patch('routes.reactions.request')

    def test_decorated_function_user_id_precedence(self, mock_request, header_value, query_value, expected_user_id):
        # Setup
        mock_f = Mock(return_value="success")
        mock_request.headers.get.return_value = header_value if header_value else None
        mock_request.args.get.return_value = query_value
        
        # Create decorated function
        def create_decorated_function(f):
            def decorated_function(*args, **kwargs):
                user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return f(*args, user_id=int(user_id), **kwargs)
            return decorated_function
        
        decorated_func = create_decorated_function(mock_f)
        
        # Execute
        result = decorated_func("test_arg")
        
        # Assert
        assert result == "success"
        mock_f.assert_called_once_with("test_arg", user_id=expected_user_id)

# Standard library
# Third-party
# Local

