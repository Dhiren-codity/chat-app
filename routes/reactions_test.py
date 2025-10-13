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
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestRequireAuth:

    def test_require_auth_with_header_user_id(self, app):

        def test_function(*args, **kwargs):
            return jsonify({"user_id": kwargs.get("user_id")})
        
        with app.test_request_context(headers={'X-User-ID': '123'}):
            response = test_function()
            assert response[0].json == {"user_id": 123}


    def test_require_auth_with_query_param_user_id(self, app):

        def test_function(*args, **kwargs):
            return jsonify({"user_id": kwargs.get("user_id")})
        
        with app.test_request_context('/?user_id=456'):
            response = test_function()
            assert response[0].json == {"user_id": 456}


    def test_require_auth_no_user_id_returns_401(self, app):

        def test_function(*args, **kwargs):
            return jsonify({"success": True})
        
        with app.test_request_context():
            response, status_code = test_function()
            assert status_code == 401
            assert response.json == {"error": "Authentication required"}


    def test_require_auth_header_takes_precedence_over_query(self, app):

        def test_function(*args, **kwargs):
            return jsonify({"user_id": kwargs.get("user_id")})
        
        with app.test_request_context('/?user_id=999', headers={'X-User-ID': '777'}):
            response = test_function()
            assert response[0].json == {"user_id": 777}

    @pytest.mark.parametrize("user_id_value,expected_int", [
        ("1", 1),
        ("0", 0),
        ("999", 999),
    ])

    def test_require_auth_converts_string_to_int(self, app, user_id_value, expected_int):

        def test_function(*args, **kwargs):
            return jsonify({"user_id": kwargs.get("user_id"), "type": type(kwargs.get("user_id")).__name__})
        
        with app.test_request_context(headers={'X-User-ID': user_id_value}):
            response = test_function()
            assert response[0].json["user_id"] == expected_int
            assert response[0].json["type"] == "int"

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
        
        response = add_reaction(user_id=1)
        
        assert response[1] == 200
        mock_reaction_manager.add_reaction.assert_called_once_with(
            message_id=123,
            user_id=1,
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
        
        response = add_reaction(user_id=1)
        
        assert response[1] == 400

    @pytest.mark.parametrize("request_data,expected_status", [
        (None, 400),
        ({}, 400),
        ({'message_id': 123}, 400),
        ({'emoji': '👍'}, 400),
        ({'message_id': 'invalid', 'emoji': '👍'}, 400),
    ])
    @patch('routes.reactions.request')

    def test_add_reaction_invalid_input(self, mock_request, request_data, expected_status):
        mock_request.get_json.return_value = request_data
        
        response = add_reaction(user_id=1)
        
        assert response[1] == expected_status

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_value_error(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.add_reaction.side_effect = ValueError("Invalid emoji")
        
        response = add_reaction(user_id=1)
        
        assert response[1] == 400

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_add_reaction_general_exception(self, mock_reaction_manager, mock_request):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.add_reaction.side_effect = Exception("Database error")
        
        response = add_reaction(user_id=1)
        
        assert response[1] == 500

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
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestRemoveReaction:
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_success(self, mock_request, mock_reaction_manager, app):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.return_value = {'success': True}
        
        with app.app_context():
            response, status_code = remove_reaction(user_id=456)
        
        assert status_code == 200
        assert response.json == {'success': True}
        mock_reaction_manager.remove_reaction.assert_called_once_with(
            message_id=123,
            user_id=456,
            emoji='👍'
        )

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_not_found(self, mock_request, mock_reaction_manager, app):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.return_value = {'success': False}
        
        with app.app_context():
            response, status_code = remove_reaction(user_id=456)
        
        assert status_code == 404
        assert response.json == {'success': False}

    @pytest.mark.parametrize("request_data,expected_error", [
        (None, "message_id and emoji are required"),
        ({}, "message_id and emoji are required"),
        ({'message_id': 123}, "message_id and emoji are required"),
        ({'emoji': '👍'}, "message_id and emoji are required"),
    ])
    @patch('routes.reactions.request')

    def test_remove_reaction_invalid_request(self, mock_request, request_data, expected_error, app):
        mock_request.get_json.return_value = request_data
        
        with app.app_context():
            response, status_code = remove_reaction(user_id=456)
        
        assert status_code == 400
        assert response.json == {"error": expected_error}

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_remove_reaction_exception(self, mock_request, mock_reaction_manager, app):
        mock_request.get_json.return_value = {
            'message_id': 123,
            'emoji': '👍'
        }
        mock_reaction_manager.remove_reaction.side_effect = Exception("Database error")
        
        with app.app_context():
            response, status_code = remove_reaction(user_id=456)
        
        assert status_code == 500
        assert response.json == {"error": "Failed to remove reaction: Database error"}

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
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestToggleReaction:
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_toggle_reaction_success(self, mock_request, mock_reaction_manager, app):
        with app.app_context():
            mock_request.get_json.return_value = {
                'message_id': 123,
                'emoji': '👍'
            }
            mock_reaction_manager.toggle_reaction.return_value = {
                'success': True,
                'action': 'added'
            }
            
            response, status_code = toggle_reaction(user_id=456)
            
            assert status_code == 200
            assert response.json['success'] is True
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

    def test_toggle_reaction_missing_data(self, mock_request, request_data, expected_error, app):
        with app.app_context():
            mock_request.get_json.return_value = request_data
            
            response, status_code = toggle_reaction(user_id=456)
            
            assert status_code == 400
            assert response.json['error'] == expected_error

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_toggle_reaction_value_error(self, mock_request, mock_reaction_manager, app):
        with app.app_context():
            mock_request.get_json.return_value = {
                'message_id': 123,
                'emoji': '👍'
            }
            mock_reaction_manager.toggle_reaction.side_effect = ValueError("Invalid message ID")
            
            response, status_code = toggle_reaction(user_id=456)
            
            assert status_code == 400
            assert response.json['error'] == "Invalid message ID"

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_toggle_reaction_general_exception(self, mock_request, mock_reaction_manager, app):
        with app.app_context():
            mock_request.get_json.return_value = {
                'message_id': 123,
                'emoji': '👍'
            }
            mock_reaction_manager.toggle_reaction.side_effect = Exception("Database error")
            
            response, status_code = toggle_reaction(user_id=456)
            
            assert status_code == 500
            assert response.json['error'] == "Failed to toggle reaction: Database error"

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock
from flask import Flask

from routes.reactions import get_message_reactions

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetMessageReactions:
    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_success(self, mock_reaction_manager):
        # Arrange
        message_id = "msg123"
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

    def test_get_message_reactions_exception(self, mock_reaction_manager):
        # Arrange
        message_id = "msg123"
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
        ("empty_msg", {}),
        ("single_reaction", {"👍": [{"user_id": 1}]}),
        ("multiple_reactions", {"👍": [{"user_id": 1}], "❤️": [{"user_id": 2}], "😊": [{"user_id": 3}]}),
        (None, {"warning": "No message ID provided"}),
        ("", {"info": "Empty message ID"})
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_message_reactions_various_inputs(self, mock_reaction_manager, message_id, expected_reactions):
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
from flask import Flask
from unittest.mock import patch, Mock

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
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_get_user_reactions_success_without_message_filter(self, mock_request, mock_reaction_manager):
        mock_request.args.get.return_value = None
        mock_reaction_manager.get_user_reactions.return_value = [
            {"id": 1, "emoji": "👍", "message_id": 100},
            {"id": 2, "emoji": "❤️", "message_id": 101}
        ]
        
        response, status_code = get_user_reactions(123)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["user_id"] == 123
        assert len(response_data["reactions"]) == 2
        mock_reaction_manager.get_user_reactions.assert_called_once_with(123, None)

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_get_user_reactions_success_with_message_filter(self, mock_request, mock_reaction_manager):
        mock_request.args.get.return_value = 100
        mock_reaction_manager.get_user_reactions.return_value = [
            {"id": 1, "emoji": "👍", "message_id": 100}
        ]
        
        response, status_code = get_user_reactions(123)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["user_id"] == 123
        assert len(response_data["reactions"]) == 1
        mock_reaction_manager.get_user_reactions.assert_called_once_with(123, 100)

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_get_user_reactions_empty_results(self, mock_request, mock_reaction_manager):
        mock_request.args.get.return_value = None
        mock_reaction_manager.get_user_reactions.return_value = []
        
        response, status_code = get_user_reactions(456)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["user_id"] == 456
        assert response_data["reactions"] == []

    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_get_user_reactions_exception_handling(self, mock_request, mock_reaction_manager):
        mock_request.args.get.return_value = None
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Database connection failed")
        
        response, status_code = get_user_reactions(789)
        
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Failed to get user reactions: Database connection failed" in response_data["error"]

    @pytest.mark.parametrize("user_id,message_id,expected_user_id", [
        (1, None, 1),
        (999, 50, 999),
        (0, 1, 0),
    ])
    @patch('routes.reactions.reaction_manager')
    @patch('routes.reactions.request')

    def test_get_user_reactions_various_inputs(self, mock_request, mock_reaction_manager, user_id, message_id, expected_user_id):
        mock_request.args.get.return_value = message_id
        mock_reaction_manager.get_user_reactions.return_value = []
        
        response, status_code = get_user_reactions(user_id)
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["user_id"] == expected_user_id
        mock_reaction_manager.get_user_reactions.assert_called_once_with(user_id, message_id)

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock
from flask import Flask

from routes.reactions import get_reaction_count

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetReactionCount:
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_success(self, mock_reaction_manager):
        mock_reaction_manager.get_reaction_count.return_value = 5
        
        response, status_code = get_reaction_count("msg123")
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == "msg123"
        assert response_data["count"] == 5
        mock_reaction_manager.get_reaction_count.assert_called_once_with("msg123")

    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_exception(self, mock_reaction_manager):
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Database error")
        
        response, status_code = get_reaction_count("msg123")
        
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Failed to get reaction count: Database error" in response_data["error"]

    @pytest.mark.parametrize("message_id,expected_count", [
        ("msg1", 0),
        ("msg2", 10),
        ("msg3", 999),
        ("", 0),
        (None, 0),
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_reaction_count_various_inputs(self, mock_reaction_manager, message_id, expected_count):
        mock_reaction_manager.get_reaction_count.return_value = expected_count
        
        response, status_code = get_reaction_count(message_id)
        
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

    def test_get_most_popular_success(self, mock_reaction_manager):
        # Arrange
        mock_reaction_manager.get_most_popular_emoji.return_value = "👍"
        message_id = "msg_123"
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["most_popular_emoji"] == "👍"
        mock_reaction_manager.get_most_popular_emoji.assert_called_once_with(message_id)

    @patch('routes.reactions.reaction_manager')

    def test_get_most_popular_exception_handling(self, mock_reaction_manager):
        # Arrange
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("Database error")
        message_id = "msg_456"
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Failed to get popular emoji: Database error" in response_data["error"]

    @pytest.mark.parametrize("message_id,emoji,expected_emoji", [
        ("msg_1", "❤️", "❤️"),
        ("msg_2", "😂", "😂"),
        ("msg_3", None, None),
        ("", "🔥", "🔥"),
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_most_popular_various_inputs(self, mock_reaction_manager, message_id, emoji, expected_emoji):
        # Arrange
        mock_reaction_manager.get_most_popular_emoji.return_value = emoji
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data["success"] is True
        assert response_data["message_id"] == message_id
        assert response_data["most_popular_emoji"] == expected_emoji

    @pytest.mark.parametrize("exception_type,error_message", [
        (ValueError, "Invalid message ID"),
        (KeyError, "Message not found"),
        (RuntimeError, "Service unavailable"),
    ])
    @patch('routes.reactions.reaction_manager')

    def test_get_most_popular_different_exceptions(self, mock_reaction_manager, exception_type, error_message):
        # Arrange
        mock_reaction_manager.get_most_popular_emoji.side_effect = exception_type(error_message)
        message_id = "msg_error"
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert f"Failed to get popular emoji: {error_message}" in response_data["error"]

# Standard library
# Third-party
# Local


import json
import pytest
from unittest.mock import patch, Mock
from flask import Flask

from routes.reactions import get_allowed_emojis

@pytest.fixture
def app():
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetAllowedEmojis:
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')

    def test_get_allowed_emojis_success(self, mock_get_emojis):
        mock_get_emojis.return_value = ['👍', '❤️', '😊', '🎉']
        
        response, status_code = get_allowed_emojis()
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['emojis'] == ['👍', '❤️', '😊', '🎉']
        mock_get_emojis.assert_called_once()

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')

    def test_get_allowed_emojis_empty_list(self, mock_get_emojis):
        mock_get_emojis.return_value = []
        
        response, status_code = get_allowed_emojis()
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['emojis'] == []

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')

    def test_get_allowed_emojis_exception_handling(self, mock_get_emojis):
        mock_get_emojis.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            get_allowed_emojis()

    @pytest.mark.parametrize("emoji_list,expected_count", [
        (['👍'], 1),
        (['👍', '❤️', '😊'], 3),
        (['🎉', '🔥', '💯', '✨', '🚀'], 5),
    ])
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')

    def test_get_allowed_emojis_various_counts(self, mock_get_emojis, emoji_list, expected_count):
        mock_get_emojis.return_value = emoji_list
        
        response, status_code = get_allowed_emojis()
        
        assert status_code == 200
        response_data = json.loads(response.data)
        assert len(response_data['emojis']) == expected_count
        assert response_data['emojis'] == emoji_list

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
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestBulkAddReactions:
    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_success(self, mock_reaction_manager, mock_request, app):
        # Arrange
        mock_data = {
            "reactions": [
                {"message_id": 1, "user_id": 123, "emoji": "👍"},
                {"message_id": 2, "user_id": 123, "emoji": "❤️"}
            ]
        }
        mock_request.get_json.return_value = mock_data
        mock_reaction_manager.bulk_add_reactions.return_value = {"added": 2, "failed": 0}
        
        with app.app_context():
            # Act
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

    def test_bulk_add_reactions_missing_data(self, mock_request, request_data, expected_error, app):
        # Arrange
        mock_request.get_json.return_value = request_data
        
        with app.app_context():
            # Act
            response, status_code = bulk_add_reactions(123)
            
            # Assert
            assert status_code == 400
            response_data = json.loads(response.data)
            assert response_data["error"] == expected_error

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_exception_handling(self, mock_reaction_manager, mock_request, app):
        # Arrange
        mock_data = {
            "reactions": [
                {"message_id": 1, "user_id": 123, "emoji": "👍"}
            ]
        }
        mock_request.get_json.return_value = mock_data
        mock_reaction_manager.bulk_add_reactions.side_effect = Exception("Database error")
        
        with app.app_context():
            # Act
            response, status_code = bulk_add_reactions(123)
            
            # Assert
            assert status_code == 500
            response_data = json.loads(response.data)
            assert "Failed to bulk add reactions: Database error" in response_data["error"]

    @patch('routes.reactions.request')
    @patch('routes.reactions.reaction_manager')

    def test_bulk_add_reactions_empty_reactions_array(self, mock_reaction_manager, mock_request, app):
        # Arrange
        mock_data = {"reactions": []}
        mock_request.get_json.return_value = mock_data
        mock_reaction_manager.bulk_add_reactions.return_value = {"added": 0, "failed": 0}
        
        with app.app_context():
            # Act
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
from unittest.mock import patch, Mock

@pytest.fixture
def app():
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
        
        # Create decorated function with mock f
        def create_decorated():
            f = mock_f
            def decorated_function(*args, **kwargs):
                user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return f(*args, user_id=int(user_id), **kwargs)
            return decorated_function
        
        decorated = create_decorated()
        
        # Execute
        result = decorated("arg1", kwarg1="value1")
        
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
        
        # Create decorated function with mock f
        def create_decorated():
            f = mock_f
            def decorated_function(*args, **kwargs):
                user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return f(*args, user_id=int(user_id), **kwargs)
            return decorated_function
        
        decorated = create_decorated()
        
        # Execute
        result = decorated()
        
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
        
        # Create decorated function with mock f
        def create_decorated():
            f = mock_f
            def decorated_function(*args, **kwargs):
                user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return f(*args, user_id=int(user_id), **kwargs)
            return decorated_function
        
        decorated = create_decorated()
        
        # Execute
        result = decorated()
        
        # Assert
        assert result == ({"error": "Authentication required"}, 401)
        mock_jsonify.assert_called_once_with({"error": "Authentication required"})
        mock_f.assert_not_called()

    @pytest.mark.parametrize("header_value,query_value,expected_user_id", [
        ("789", "123", 789),  # Header takes precedence
        ("", "456", 456),     # Empty header, use query
        ("0", "123", 0),      # Zero is valid user_id
    ])
    @patch('routes.reactions.request')
    @patch('routes.reactions.jsonify')
    def test_decorated_function_user_id_precedence(self, mock_jsonify, mock_request, 
                                                   header_value, query_value, expected_user_id):
        # Setup
        mock_f = Mock(return_value="success")
        mock_request.headers.get.return_value = header_value if header_value else None
        mock_request.args.get.return_value = query_value
        
        # Create decorated function with mock f
        def create_decorated():
            f = mock_f
            def decorated_function(*args, **kwargs):
                user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return f(*args, user_id=int(user_id), **kwargs)
            return decorated_function
        
        decorated = create_decorated()
        
        # Execute
        result = decorated()
        
        # Assert
        assert result == "success"
        mock_f.assert_called_once_with(user_id=expected_user_id)

# Standard library
# Third-party
# Local

