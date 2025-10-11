import json
import pytest
from unittest.mock import patch
from flask import Flask, jsonify

from routes.reactions import require_auth, add_reaction, remove_reaction, toggle_reaction, get_message_reactions, get_user_reactions, get_reaction_count, get_most_popular, get_allowed_emojis, bulk_add_reactions

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(routes.reactions.reactions_bp)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestRequireAuth:
    @pytest.mark.parametrize("user_id,expected_status,expected_response", [
        (1, 200, {"user_id": 1}),
        (None, 401, {"error": "Authentication required"}),
        ("not_a_number", 401, {"error": "Authentication required"}),
        (0, 200, {"user_id": 0}),
        (-1, 200, {"user_id": -1}),
        (2**31 - 1, 200, {"user_id": 2147483647}),
    ])
    def test_require_auth(self, client, user_id, expected_status, expected_response):
        if user_id is not None:
            with client.session_transaction() as sess:
                sess['X-User-ID'] = user_id
        response = client.get('/api/reactions/test', query_string={'user_id': user_id} if user_id is not None else {})
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    def test_exception_handling(self, client):
        @require_auth
        def error_route(user_id):
            raise Exception("Unexpected error")

        response = client.get('/api/reactions/error', query_string={'user_id': 1})
        assert response.status_code == 500
        assert response.get_json() == {"error": "Unexpected error"}

class TestAddReaction:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2, "emoji": "😊"}, 200, {"success": True}),
        ({"message_id": 3, "emoji": "😢"}, 200, {"success": True}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.add_reaction.return_value = expected_response
        response = client.post('/api/reactions/add', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        (None, 400, {"error": "message_id and emoji are required"}),
        ({}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1}, 400, {"error": "message_id and emoji are required"}),
        ({"emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
    ])
    def test_empty_none_inputs(self, client, input_data, expected_status, expected_response):
        response = client.post('/api/reactions/add', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": "not_an_int", "emoji": "👍"}, 400, {"error": "Failed to add reaction: invalid literal for int() with base 10: 'not_an_int'"}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "Failed to add reaction: message_id must be a positive integer"}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_invalid_input_types(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.add_reaction.side_effect = ValueError("invalid literal for int() with base 10: 'not_an_int'")
        response = client.post('/api/reactions/add', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 0, "emoji": "👍"}, 400, {"error": "Failed to add reaction: message_id must be a positive integer"}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "Failed to add reaction: message_id must be a positive integer"}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_boundary_conditions(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.add_reaction.side_effect = ValueError("message_id must be a positive integer")
        response = client.post('/api/reactions/add', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 500, {"error": "Failed to add reaction: Some unexpected error"}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.add_reaction.side_effect = Exception("Some unexpected error")
        response = client.post('/api/reactions/add', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

class TestRemoveReaction:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2, "emoji": "👎"}, 404, {"success": False}),
        ({"message_id": 0, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1, "emoji": ""}, 400, {"error": "message_id and emoji are required"}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        if expected_status == 200:
            mock_reaction_manager.remove_reaction.return_value = {"success": True}
        elif expected_status == 404:
            mock_reaction_manager.remove_reaction.return_value = {"success": False}
        
        response = client.post('/api/reactions/remove', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        (None, 400, {"error": "message_id and emoji are required"}),
        ({}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1}, 400, {"error": "message_id and emoji are required"}),
        ({"emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
    ])
    def test_remove_reaction_invalid_inputs(self, client, input_data, expected_status, expected_response):
        response = client.post('/api/reactions/remove', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.remove_reaction.side_effect = Exception("Database error")
        
        input_data = {"message_id": 1, "emoji": "👍"}
        response = client.post('/api/reactions/remove', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to remove reaction: Database error"}

class TestToggleReaction:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": None, "emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1, "emoji": None}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": "not_an_int", "emoji": "👍"}, 400, {"error": "Failed to toggle reaction: invalid literal for int() with base 10: 'not_an_int'"}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "Failed to toggle reaction: message_id must be a positive integer"}),
        ({"message_id": 0, "emoji": "👍"}, 400, {"error": "Failed to toggle reaction: message_id must be a positive integer"}),
    ])
    @patch('routes.reactions.reaction_manager.toggle_reaction')
    def test_toggle_reaction(self, mock_toggle_reaction, client, input_data, expected_status, expected_response):
        if expected_status == 200:
            mock_toggle_reaction.return_value = {"success": True}
        else:
            mock_toggle_reaction.side_effect = ValueError(expected_response["error"]) if expected_status == 400 else Exception(expected_response["error"])

        response = client.post('/api/reactions/toggle', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager.toggle_reaction')
    def test_exception_handling(self, mock_toggle_reaction, client):
        mock_toggle_reaction.side_effect = Exception("Unexpected error")
        
        response = client.post('/api/reactions/toggle', data=json.dumps({"message_id": 1, "emoji": "👍"}), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to toggle reaction: Unexpected error"}

class TestGetMessageReactions:
    @pytest.mark.parametrize("message_id,expected_reactions,expected_status", [
        (1, [{"emoji": "👍", "count": 5}], 200),
        (2, [], 200),
        (None, [], 500),
        ("invalid_id", [], 500),
        (-1, [], 500),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_get_message_reactions(self, mock_reaction_manager, message_id, expected_reactions, expected_status):
        mock_reaction_manager.get_message_reactions.return_value = expected_reactions
        
        response = get_message_reactions(message_id)
        
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
        mock_reaction_manager.get_message_reactions.side_effect = Exception("Database error")
        
        response = get_message_reactions(1)
        
        assert response[1] == 500
        data = json.loads(response[0].data)
        assert "error" in data
        assert data["error"] == "Failed to get reactions: Database error"

class TestGetUserReactions:
    @pytest.mark.parametrize("user_id, message_id, expected_reactions, expected_status", [
        (1, None, [{"message_id": 1, "reaction": "like"}], 200),
        (1, 2, [], 200),
        (0, None, [], 200),
        (-1, None, [], 200),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_get_user_reactions(self, mock_reaction_manager, client, user_id, message_id, expected_reactions, expected_status):
        mock_reaction_manager.get_user_reactions.return_value = expected_reactions
        
        response = client.get('/api/reactions/user', query_string={'message_id': message_id} if message_id is not None else {})
        
        assert response.status_code == expected_status
        response_json = response.get_json()
        assert response_json['success'] == (expected_status == 200)
        assert response_json['user_id'] == user_id
        assert response_json['reactions'] == expected_reactions

    @patch('routes.reactions.reaction_manager')
    def test_get_user_reactions_exception(self, mock_reaction_manager, client):
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Database error")
        
        response = client.get('/api/reactions/user', query_string={'message_id': 1})
        
        assert response.status_code == 500
        response_json = response.get_json()
        assert response_json['error'] == "Failed to get user reactions: Database error"

class TestGetReactionCount:
    @pytest.mark.parametrize("message_id,expected_count", [
        (1, 5),
        (2, 0),
        (3, 10),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager, message_id, expected_count):
        mock_reaction_manager.get_reaction_count.return_value = expected_count
        
        response, status_code = get_reaction_count(message_id)
        
        assert status_code == 200
        assert response.json == {
            "success": True,
            "message_id": message_id,
            "count": expected_count
        }

    @pytest.mark.parametrize("message_id", [
        None,
        "",
        "abc"
    ])
    @patch('routes.reactions.reaction_manager')
    def test_invalid_inputs(self, mock_reaction_manager, message_id):
        response, status_code = get_reaction_count(message_id)
        
        assert status_code == 500
        assert "error" in response.json

    @pytest.mark.parametrize("message_id", [
        0,
        -1,
        99999
    ])
    @patch('routes.reactions.reaction_manager')
    def test_boundary_conditions(self, mock_reaction_manager, message_id):
        if message_id < 0:
            mock_reaction_manager.get_reaction_count.side_effect = ValueError("Invalid message_id")
        else:
            mock_reaction_manager.get_reaction_count.return_value = 0
        
        response, status_code = get_reaction_count(message_id)
        
        if message_id < 0:
            assert status_code == 500
            assert "error" in response.json
        else:
            assert status_code == 200
            assert response.json == {
                "success": True,
                "message_id": message_id,
                "count": 0
            }

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager):
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Some error occurred")
        
        response, status_code = get_reaction_count(1)
        
        assert status_code == 500
        assert "error" in response.json
        assert response.json["error"] == "Failed to get reaction count: Some error occurred"

class TestGetMostPopular:
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager):
        message_id = 123
        expected_emoji = "😊"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        response, status_code = get_most_popular(message_id)
        
        assert status_code == 200
        assert response.json == {
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        }

    @pytest.mark.parametrize("message_id", [None, "", 0, -1])
    @patch('routes.reactions.reaction_manager')
    def test_empty_and_invalid_inputs(self, mock_reaction_manager, message_id):
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("Invalid input")
        
        response, status_code = get_most_popular(message_id)
        
        assert status_code == 500
        assert response.json == {"error": "Failed to get popular emoji: Invalid input"}

    @pytest.mark.parametrize("message_id", [1, 2, 3, 1000])
    @patch('routes.reactions.reaction_manager')
    def test_boundary_conditions(self, mock_reaction_manager, message_id):
        expected_emoji = "👍"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        response, status_code = get_most_popular(message_id)
        
        assert status_code == 200
        assert response.json == {
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        }

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager):
        message_id = 456
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("Database error")
        
        response, status_code = get_most_popular(message_id)
        
        assert status_code == 500
        assert response.json == {"error": "Failed to get popular emoji: Database error"}

class TestGetAllowedEmojis:
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_success(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.return_value = ['😀', '😂', '😍']
        
        response = client.get('/api/reactions/allowed-emojis')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == ['😀', '😂', '😍']

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_empty_list(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.return_value = []
        
        response = client.get('/api/reactions/allowed-emojis')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == []

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_exception(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.side_effect = Exception("Some error occurred")
        
        response = client.get('/api/reactions/allowed-emojis')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data

    @pytest.mark.parametrize("mock_return_value,expected_emojis", [
        (['😀', '😂'], ['😀', '😂']),
        (['😎'], ['😎']),
        ([], []),
    ])
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_various_cases(self, mock_get_allowed_emojis, client, mock_return_value, expected_emojis):
        mock_get_allowed_emojis.return_value = mock_return_value
        
        response = client.get('/api/reactions/allowed-emojis')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == expected_emojis

class TestBulkAddReactions:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
        ({"reactions": []}, 400, {"error": "reactions array is required"}),
        (None, 400, {"error": "reactions array is required"}),
        ({"reactions": [{"message_id": 0, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
        ({"reactions": [{"message_id": -1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
        ({"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_bulk_add_reactions(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.bulk_add_reactions.return_value = "Reactions added"
        
        response = client.post('/api/reactions/bulk', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.bulk_add_reactions.side_effect = Exception("Database error")
        
        input_data = {"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}
        response = client.post('/api/reactions/bulk', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to bulk add reactions: Database error"}

class TestDecoratedFunction:
    @pytest.mark.parametrize("user_id, expected_status, expected_response", [
        (1, 200, "success"),
        (None, 401, {"error": "Authentication required"}),
        ("invalid", 500, None),
        (0, 200, "success"),
        (-1, 200, "success"),
        (2**31 - 1, 200, "success"),
    ])
    @patch('routes.reactions.request')
    def test_decorated_function(self, mock_request, user_id, expected_status, expected_response, client):
        if user_id is not None:
            mock_request.headers = {'X-User-ID': str(user_id)}
        else:
            mock_request.headers = {}
        
        def mock_function(*args, **kwargs):
            return jsonify({"result": "success"}), 200
        
        if expected_status == 200:
            response = decorated_function(mock_function)
            assert response[1] == expected_status
            assert response[0].json == expected_response
        else:
            with pytest.raises(Exception):
                decorated_function(mock_function)