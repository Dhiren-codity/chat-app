"""
Auto-generated tests using LLM and RAG
"""

import pytest


# Standard library
from functools import wraps

# Third-party
import pytest
from flask import Flask, jsonify, request
from unittest.mock import patch, Mock

# Local - USE ACTUAL PATHS from source
from routes.reactions import require_auth

# Create a Flask app for testing

@require_auth


def test_route(user_id):
    return jsonify({"user_id": user_id}), 200

class TestRequireAuth:
    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    @pytest.mark.parametrize("user_id,expected_status,expected_response", [
        (1, 200, {"user_id": 1}),  # Happy path
        (None, 401, {"error": "Authentication required"}),  # No user_id
        ("not_a_number", 401, {"error": "Authentication required"}),  # Invalid user_id
        (0, 200, {"user_id": 0}),  # Boundary condition: zero
        (-1, 200, {"user_id": -1}),  # Boundary condition: negative
        (2**31 - 1, 200, {"user_id": 2147483647}),  # Boundary condition: max int
    ])
    

def test_require_auth(self, client, user_id, expected_status, expected_response):
        # Mock the request headers or args based on the user_id
        if user_id is not None:
            with patch('routes.reactions.request') as mock_request:
                mock_request.headers.get = Mock(return_value=user_id)
                response = client.get('/test')
        else:
            response = client.get('/test')

        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    

def test_exception_handling(self, client):
        with patch('routes.reactions.request') as mock_request:
            mock_request.headers.get = Mock(side_effect=Exception("Unexpected error"))
            response = client.get('/test')
            assert response.status_code == 401
            assert response.get_json() == {"error": "Authentication required"}


# Standard library
import json

# Third-party
import pytest
from flask import Flask, jsonify
from unittest.mock import patch, Mock

# Local - USE ACTUAL PATHS from source
from routes.reactions import add_reaction

@pytest.fixture
def client():
    app.add_url_rule('/add_reaction', 'add_reaction', add_reaction, methods=['POST'])
    with app.test_client() as client:
        yield client

class TestAddReaction:
    
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2, "emoji": "😊"}, 200, {"success": True}),
        ({"message_id": 3, "emoji": "😢"}, 200, {"success": True}),
    ])
    @patch('routes.reactions.reaction_manager')
    

def test_happy_path(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.add_reaction.return_value = expected_response
        response = client.post('/add_reaction', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        (None, 400, {"error": "message_id and emoji are required"}),
        ({}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1}, 400, {"error": "message_id and emoji are required"}),
        ({"emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
    ])
    

def test_empty_none_inputs(self, client, input_data, expected_status, expected_response):
        response = client.post('/add_reaction', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": "not_an_int", "emoji": "👍"}, 400, {"error": "Failed to add reaction: invalid literal for int() with base 10: 'not_an_int'"}),
        ({"message_id": 1, "emoji": 123}, 400, {"error": "Failed to add reaction: emoji must be a string"}),
    ])
    

def test_invalid_input_types(self, client, input_data, expected_status, expected_response):
        @patch('routes.reactions.reaction_manager')
        def inner(mock_reaction_manager):
            mock_reaction_manager.add_reaction.side_effect = ValueError("invalid literal for int() with base 10: 'not_an_int'")
            response = client.post('/add_reaction', data=json.dumps(input_data), content_type='application/json')
            assert response.status_code == expected_status
            assert response.get_json() == expected_response
        inner()

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 0, "emoji": "👍"}, 400, {"error": "Failed to add reaction: message_id must be positive"}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "Failed to add reaction: message_id must be positive"}),
    ])
    

def test_boundary_conditions(self, client, input_data, expected_status, expected_response):
        @patch('routes.reactions.reaction_manager')
        def inner(mock_reaction_manager):
            mock_reaction_manager.add_reaction.side_effect = ValueError("message_id must be positive")
            response = client.post('/add_reaction', data=json.dumps(input_data), content_type='application/json')
            assert response.status_code == expected_status
            assert response.get_json() == expected_response
        inner()

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 500, {"error": "Failed to add reaction: some error"}),
    ])
    

def test_exception_handling(self, client, input_data, expected_status, expected_response):
        @patch('routes.reactions.reaction_manager')
        def inner(mock_reaction_manager):
            mock_reaction_manager.add_reaction.side_effect = Exception("some error")
            response = client.post('/add_reaction', data=json.dumps(input_data), content_type='application/json')
            assert response.status_code == expected_status
            assert response.get_json() == expected_response
        inner()


# Standard library
import json

# Third-party
import pytest
from unittest.mock import patch, Mock
from flask import Flask, jsonify

# Local - USE ACTUAL PATHS from source
from routes.reactions import remove_reaction

@pytest.fixture
def client():
    app.add_url_rule('/remove_reaction', 'remove_reaction', remove_reaction, methods=['POST'])
    with app.test_client() as client:
        yield client

class TestRemoveReaction:
    
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2, "emoji": "👎"}, 404, {"success": False}),
        ({"message_id": 0, "emoji": "👍"}, 200, {"success": True}),  # Boundary case
        ({"message_id": -1, "emoji": "👍"}, 404, {"success": False}),  # Invalid message_id
        ({"message_id": 1, "emoji": ""}, 400, {"error": "message_id and emoji are required"}),  # Missing emoji
        ({"message_id": None, "emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),  # None message_id
        ({"message_id": 1}, 400, {"error": "message_id and emoji are required"}),  # Missing emoji
        ({"emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),  # Missing message_id
        ({"message_id": 1, "emoji": "👍"}, 500, {"error": "Failed to remove reaction: Some error"})  # Exception case
    ])
    @patch('routes.reactions.reaction_manager')
    

def test_remove_reaction(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        if expected_status == 200:
            mock_reaction_manager.remove_reaction.return_value = {"success": True}
        elif expected_status == 404:
            mock_reaction_manager.remove_reaction.return_value = {"success": False}
        elif expected_status == 500:
            mock_reaction_manager.remove_reaction.side_effect = Exception("Some error")
        
        response = client.post('/remove_reaction', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response


# Standard library
import json

# Third-party
import pytest
from unittest.mock import patch, Mock
from flask import Flask, jsonify

# Local - USE ACTUAL PATHS from source
from routes.reactions import toggle_reaction

@pytest.fixture
def client():
    app.add_url_rule('/toggle_reaction', 'toggle_reaction', toggle_reaction, methods=['POST'])
    with app.test_client() as client:
        yield client

class TestToggleReaction:
    
    @pytest.mark.parametrize("data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 0, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": -1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 1, "emoji": ""}, 400, {"error": "Failed to toggle reaction: emoji cannot be empty"}),
        ({"message_id": 1}, 400, {"error": "message_id and emoji are required"}),
        ({"emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        (None, 400, {"error": "message_id and emoji are required"}),
    ])
    @patch('routes.reactions.reaction_manager')
    

def test_toggle_reaction(self, mock_reaction_manager, client, data, expected_status, expected_response):
        if expected_status == 200:
            mock_reaction_manager.toggle_reaction.return_value = {"success": True}
        
        response = client.post('/toggle_reaction', data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager')
    

def test_toggle_reaction_value_error(self, mock_reaction_manager, client):
        mock_reaction_manager.toggle_reaction.side_effect = ValueError("Invalid emoji")
        
        response = client.post('/toggle_reaction', data=json.dumps({"message_id": 1, "emoji": "👍"}), content_type='application/json')
        
        assert response.status_code == 400
        assert response.get_json() == {"error": "Invalid emoji"}

    @patch('routes.reactions.reaction_manager')
    

def test_toggle_reaction_general_exception(self, mock_reaction_manager, client):
        mock_reaction_manager.toggle_reaction.side_effect = Exception("Some error occurred")
        
        response = client.post('/toggle_reaction', data=json.dumps({"message_id": 1, "emoji": "👍"}), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to toggle reaction: Some error occurred"}


# Standard library
import json

# Third-party
import pytest
from unittest.mock import patch, Mock
from flask import jsonify

# Local - USE ACTUAL PATHS from source
from routes.reactions import get_message_reactions

class TestGetMessageReactions:
    
    @pytest.mark.parametrize("message_id,expected_reactions,expected_status", [
        (1, [{"emoji": "👍", "count": 5}], 200),  # Happy path
        (2, [], 200),  # Empty reactions
        (None, [], 500),  # None input
        ("invalid_id", [], 500),  # Invalid input type
        (-1, [], 500),  # Negative ID
    ])
    @patch('routes.reactions.reaction_manager')
    

def test_get_message_reactions(self, mock_reaction_manager, message_id, expected_reactions, expected_status):
        # Arrange
        mock_reaction_manager.get_message_reactions.return_value = expected_reactions
        
        # Act
        response = get_message_reactions(message_id)
        
        # Assert
        assert response[1] == expected_status
        if expected_status == 200:
            data = json.loads(response[0].data)
            assert data["success"] is True
            assert data["message_id"] == message_id
            assert data["reactions"] == expected_reactions
        else:
            data = json.loads(response[0].data)
            assert "error" in data

    @patch('routes.reactions.reaction_manager')
    

def test_exception_handling(self, mock_reaction_manager):
        # Arrange
        mock_reaction_manager.get_message_reactions.side_effect = Exception("Database error")
        
        # Act
        response = get_message_reactions(1)
        
        # Assert
        assert response[1] == 500
        data = json.loads(response[0].data)
        assert "error" in data
        assert data["error"] == "Failed to get reactions: Database error"


# Standard library
import pytest

# Third-party
from flask import Flask, jsonify
from unittest.mock import patch, Mock

# Local - USE ACTUAL PATHS from source
from routes.reactions import get_user_reactions

# Create a Flask app for testing
@pytest.fixture
def client():
    app.add_url_rule('/user/reactions', 'get_user_reactions', get_user_reactions)
    with app.test_client() as client:
        yield client

class TestGetUserReactions:
    
    @pytest.mark.parametrize("user_id, message_id, expected_reactions, expected_status", [
        (1, None, [{"message_id": 1, "reaction": "like"}], 200),  # Happy path
        (1, 2, [], 200),  # No reactions for specific message
        (0, None, [], 200),  # Edge case: user_id is zero
        (-1, None, [], 200),  # Edge case: negative user_id
    ])
    @patch('routes.reactions.reaction_manager')
    

def test_get_user_reactions(self, mock_reaction_manager, client, user_id, message_id, expected_reactions, expected_status):
        # Setup mock return value
        mock_reaction_manager.get_user_reactions.return_value = expected_reactions
        
        # Make request
        response = client.get('/user/reactions', query_string={'message_id': message_id} if message_id is not None else {})
        
        # Assert response
        assert response.status_code == expected_status
        response_json = response.get_json()
        assert response_json['success'] == (expected_status == 200)
        if expected_status == 200:
            assert response_json['user_id'] == user_id
            assert response_json['reactions'] == expected_reactions

    @patch('routes.reactions.reaction_manager')
    

def test_get_user_reactions_exception(self, mock_reaction_manager, client):
        # Setup mock to raise an exception
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Database error")
        
        # Make request
        response = client.get('/user/reactions')
        
        # Assert response
        assert response.status_code == 500
        response_json = response.get_json()
        assert response_json['error'] == "Failed to get user reactions: Database error"


# Standard library
import pytest

# Third-party
from flask import jsonify
from unittest.mock import patch, Mock

# Local - USE ACTUAL PATHS from source
from routes.reactions import get_reaction_count

class TestGetReactionCount:
    
    @pytest.mark.parametrize("message_id,expected_count", [
        (1, 5),  # Happy path with a valid message_id
        (2, 0),  # Boundary condition with a message_id that has no reactions
        (3, 10), # Another valid case
    ])
    @patch('routes.reactions.reaction_manager')
    

def test_happy_path(self, mock_reaction_manager, message_id, expected_count):
        # Arrange
        mock_reaction_manager.get_reaction_count.return_value = expected_count
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        assert response.json == {
            "success": True,
            "message_id": message_id,
            "count": expected_count
        }

    @pytest.mark.parametrize("message_id", [
        None,  # Test with None
        "",    # Test with empty string
    ])
    @patch('routes.reactions.reaction_manager')
    

def test_empty_none_inputs(self, mock_reaction_manager, message_id):
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        assert "error" in response.json

    @pytest.mark.parametrize("message_id", [
        {},  # Invalid type: dict
        [],  # Invalid type: list
        3.14 # Invalid type: float
    ])
    @patch('routes.reactions.reaction_manager')
    

def test_invalid_input_types(self, mock_reaction_manager, message_id):
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 500
        assert "error" in response.json

    @pytest.mark.parametrize("message_id,expected_count", [
        (0, 0),   # Boundary condition: zero
        (-1, 0),  # Boundary condition: negative
    ])
    @patch('routes.reactions.reaction_manager')
    

def test_boundary_conditions(self, mock_reaction_manager, message_id, expected_count):
        # Arrange
        mock_reaction_manager.get_reaction_count.return_value = expected_count
        
        # Act
        response, status_code = get_reaction_count(message_id)
        
        # Assert
        assert status_code == 200
        assert response.json == {
            "success": True,
            "message_id": message_id,
            "count": expected_count
        }

    @patch('routes.reactions.reaction_manager')
    

def test_exception_handling(self, mock_reaction_manager):
        # Arrange
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Database error")
        
        # Act
        response, status_code = get_reaction_count(1)
        
        # Assert
        assert status_code == 500
        assert "error" in response.json
        assert "Failed to get reaction count" in response.json["error"]


# Standard library
import pytest

# Third-party
from flask import jsonify
from unittest.mock import patch, Mock

# Local - USE ACTUAL PATHS from source
from routes.reactions import get_most_popular

class TestGetMostPopular:
    
    @patch('routes.reactions.reaction_manager')
    

def test_get_most_popular_happy_path(self, mock_reaction_manager):
        # Arrange
        message_id = 123
        expected_emoji = "😊"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        assert response.json == {
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        }

    @pytest.mark.parametrize("message_id", [None, "", 0, -1])
    @patch('routes.reactions.reaction_manager')
    

def test_get_most_popular_empty_and_invalid_inputs(self, mock_reaction_manager, message_id):
        # Arrange
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("Invalid message ID")
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 500
        assert response.json == {"error": "Failed to get popular emoji: Invalid message ID"}

    @pytest.mark.parametrize("message_id", [1, 2, 3, 1000])
    @patch('routes.reactions.reaction_manager')
    

def test_get_most_popular_boundary_conditions(self, mock_reaction_manager, message_id):
        # Arrange
        expected_emoji = "👍"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 200
        assert response.json == {
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        }

    @patch('routes.reactions.reaction_manager')
    

def test_get_most_popular_exception_handling(self, mock_reaction_manager):
        # Arrange
        message_id = 456
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("Database error")
        
        # Act
        response, status_code = get_most_popular(message_id)
        
        # Assert
        assert status_code == 500
        assert response.json == {"error": "Failed to get popular emoji: Database error"}


# Standard library
import json

# Third-party
import pytest
from unittest.mock import patch, Mock
from flask import Flask, jsonify

# Local - USE ACTUAL PATHS from source
from routes.reactions import get_allowed_emojis

# Create a Flask app for testing
@pytest.fixture
def app():
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestGetAllowedEmojis:
    
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    

def test_get_allowed_emojis_success(self, mock_get_allowed_emojis, client):
        # Arrange
        mock_get_allowed_emojis.return_value = ['😀', '😂', '😍']
        
        # Act
        response = client.get('/get_allowed_emojis')  # Assuming the route is defined
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == ['😀', '😂', '😍']

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    

def test_get_allowed_emojis_empty(self, mock_get_allowed_emojis, client):
        # Arrange
        mock_get_allowed_emojis.return_value = []
        
        # Act
        response = client.get('/get_allowed_emojis')  # Assuming the route is defined
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == []

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    

def test_get_allowed_emojis_exception(self, mock_get_allowed_emojis, client):
        # Arrange
        mock_get_allowed_emojis.side_effect = Exception("Some error occurred")
        
        # Act
        response = client.get('/get_allowed_emojis')  # Assuming the route is defined
        
        # Assert
        assert response.status_code == 500  # Assuming the error handling returns a 500 status
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data  # Assuming the error message is included in the response

    @pytest.mark.parametrize("mock_return_value,expected_emojis", [
        (['😀', '😂'], ['😀', '😂']),
        (['😎'], ['😎']),
        ([], []),
    ])
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    

def test_get_allowed_emojis_various_cases(self, mock_get_allowed_emojis, client, mock_return_value, expected_emojis):
        # Arrange
        mock_get_allowed_emojis.return_value = mock_return_value
        
        # Act
        response = client.get('/get_allowed_emojis')  # Assuming the route is defined
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == expected_emojis


# Standard library
import json

# Third-party
import pytest
from flask import Flask, jsonify
from unittest.mock import patch, Mock

# Local - USE ACTUAL PATHS from source
from routes.reactions import bulk_add_reactions

# Create a Flask app for testing
@pytest.fixture
def client():
    app.add_url_rule('/bulk_add_reactions', 'bulk_add_reactions', bulk_add_reactions, methods=['POST'])
    with app.test_client() as client:
        yield client

class TestBulkAddReactions:
    
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
        ({"reactions": []}, 400, {"error": "reactions array is required"}),
        (None, 400, {"error": "reactions array is required"}),
        ({"reactions": [{"message_id": 0, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
        ({"reactions": [{"message_id": -1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
        ({"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
    ])
    @patch('routes.reactions.reaction_manager.bulk_add_reactions')
    

def test_bulk_add_reactions(self, mock_bulk_add_reactions, client, input_data, expected_status, expected_response):
        # Mock the return value of the bulk_add_reactions method
        if expected_status == 200:
            mock_bulk_add_reactions.return_value = "Reactions added"
        else:
            mock_bulk_add_reactions.side_effect = Exception("Invalid input")

        response = client.post('/bulk_add_reactions', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager.bulk_add_reactions')
    

def test_exception_handling(self, mock_bulk_add_reactions, client):
        mock_bulk_add_reactions.side_effect = Exception("Failed to add reactions")
        
        input_data = {"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}
        response = client.post('/bulk_add_reactions', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to bulk add reactions: Failed to add reactions"}


# Standard library
import pytest
from unittest.mock import patch, Mock
from flask import Flask, jsonify, request

# Local - USE ACTUAL PATHS from source
from routes.reactions import decorated_function

# Create a Flask app for testing
@pytest.fixture
def app():
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestDecoratedFunction:
    @pytest.mark.parametrize("user_id,expected_status,expected_response", [
        (1, 200, "Success"),  # Happy path
        (None, 401, {"error": "Authentication required"}),  # No user_id
        ("abc", 401, {"error": "Authentication required"}),  # Invalid user_id type
        (0, 200, "Success"),  # Boundary condition: zero
        (-1, 200, "Success"),  # Boundary condition: negative
        (2**31 - 1, 200, "Success"),  # Boundary condition: max int value
    ])
    @patch('routes.reactions.request')
    

def test_decorated_function(self, mock_request, user_id, expected_status, expected_response, client):
        # Mock the request headers or args based on the user_id
        if user_id is not None:
            mock_request.headers = {'X-User-ID': str(user_id)}
        else:
            mock_request.headers = {}

        # Mock the function f to return a success message
        f = Mock(return_value="Success")

        # Call the decorated function
        response = decorated_function(f)

        # Check the response
        assert response[1] == expected_status
        if expected_status == 200:
            assert response[0] == "Success"
        else:
            assert response[0] == expected_response

    

def test_exception_handling(self, client):
        # Mock the function f to raise an exception
        f = Mock(side_effect=Exception("Some error"))

        # Patch the request to provide a valid user_id
        with patch('routes.reactions.request.headers', {'X-User-ID': '1'}):
            with pytest.raises(Exception):
                decorated_function(f)

