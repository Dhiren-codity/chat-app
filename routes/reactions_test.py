import json
import pytest
from unittest.mock import patch
from flask import Flask

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
        response = client.get('/api/reactions/test', query_string={'user_id': user_id} if user_id is None else {})
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    def test_exception_handling(self, client):
        @require_auth
        def error_route(user_id):
            raise Exception("Unexpected error")

        response = client.get('/api/reactions/error', headers={'X-User-ID': '1'})
        assert response.status_code == 500

class TestAddReaction:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2, "emoji": "😊"}, 200, {"success": True}),
        ({"message_id": 0, "emoji": "👍"}, 400, {"error": "Failed to add reaction: Invalid message_id"}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "Failed to add reaction: Invalid message_id"}),
        ({"message_id": 1, "emoji": ""}, 400, {"error": "Failed to add reaction: Invalid emoji"}),
        ({"message_id": 1}, 400, {"error": "message_id and emoji are required"}),
        ({"emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        (None, 400, {"error": "message_id and emoji are required"}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_add_reaction(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        if input_data and 'message_id' in input_data and 'emoji' in input_data:
            mock_reaction_manager.add_reaction.return_value = {"success": True}
        else:
            mock_reaction_manager.add_reaction.side_effect = ValueError("Invalid message_id")

        response = client.post('/api/reactions/add', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.side_effect = Exception("Unexpected error")

        response = client.post('/api/reactions/add', data=json.dumps({"message_id": 1, "emoji": "👍"}), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to add reaction: Unexpected error"}

class TestRemoveReaction:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2, "emoji": "👎"}, 404, {"success": False}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.remove_reaction.return_value = expected_response
        response = client.post('/api/reactions/remove', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        (None, 400, {"error": "message_id and emoji are required"}),
        ({}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1}, 400, {"error": "message_id and emoji are required"}),
        ({"emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
    ])
    def test_empty_none_inputs(self, client, input_data, expected_status, expected_response):
        response = client.post('/api/reactions/remove', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": "not_an_int", "emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1, "emoji": 123}, 400, {"error": "message_id and emoji are required"}),
    ])
    def test_invalid_input_types(self, client, input_data, expected_status, expected_response):
        response = client.post('/api/reactions/remove', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 0, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": -1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2147483647, "emoji": "👍"}, 200, {"success": True}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_boundary_conditions(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.remove_reaction.return_value = expected_response
        response = client.post('/api/reactions/remove', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.remove_reaction.side_effect = Exception("Database error")
        input_data = {"message_id": 1, "emoji": "👍"}
        response = client.post('/api/reactions/remove', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to remove reaction: Database error"}

class TestToggleReaction:
    @pytest.mark.parametrize("data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": None, "emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1, "emoji": None}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": "not_an_int", "emoji": "👍"}, 400, {"error": "Failed to toggle reaction: invalid input"}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "Failed to toggle reaction: invalid input"}),
        ({"message_id": 0, "emoji": "👍"}, 400, {"error": "Failed to toggle reaction: invalid input"}),
    ])
    @patch('routes.reactions.reaction_manager.toggle_reaction')
    def test_toggle_reaction(self, mock_toggle_reaction, client, data, expected_status, expected_response):
        if expected_status == 200:
            mock_toggle_reaction.return_value = {"success": True}
        else:
            mock_toggle_reaction.side_effect = ValueError("invalid input") if "invalid input" in expected_response["error"] else Exception("Failed to toggle reaction")

        response = client.post('/api/reactions/toggle', data=json.dumps(data), content_type='application/json')
        
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
    ])
    @patch('routes.reactions.reaction_manager')
    def test_get_message_reactions(self, mock_reaction_manager, message_id, expected_reactions, expected_status):
        mock_reaction_manager.get_message_reactions.return_value = expected_reactions
        
        response = get_message_reactions(message_id)
        
        assert response[1] == expected_status
        if expected_status == 200:
            data = json.loads(response[0].data)
            assert data['success'] is True
            assert data['message_id'] == message_id
            assert data['reactions'] == expected_reactions
        else:
            data = json.loads(response[0].data)
            assert 'error' in data

    @patch('routes.reactions.reaction_manager')
    def test_get_message_reactions_exception(self, mock_reaction_manager):
        mock_reaction_manager.get_message_reactions.side_effect = Exception("Database error")
        
        response = get_message_reactions(1)
        
        assert response[1] == 500
        data = json.loads(response[0].data)
        assert 'error' in data
        assert data['error'] == "Failed to get reactions: Database error"

class TestGetUserReactions:
    @pytest.mark.parametrize("user_id, message_id, mock_reactions, expected_status, expected_json", [
        (1, None, ["like", "love"], 200, {"success": True, "user_id": 1, "reactions": ["like", "love"]}),
        (2, 5, ["laugh"], 200, {"success": True, "user_id": 2, "reactions": ["laugh"]}),
        (3, None, [], 200, {"success": True, "user_id": 3, "reactions": []}),
        (4, 10, None, 200, {"success": True, "user_id": 4, "reactions": []}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager, client, user_id, message_id, mock_reactions, expected_status, expected_json):
        mock_reaction_manager.get_user_reactions.return_value = mock_reactions
        
        response = client.get('/api/reactions/user', query_string={'message_id': message_id}, headers={'X-User-ID': user_id})
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_json

    @pytest.mark.parametrize("user_id, message_id", [
        (None, None),
        (1, "invalid"),
        ("invalid", 5),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_invalid_input_types(self, mock_reaction_manager, client, user_id, message_id):
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Invalid input")
        
        response = client.get('/api/reactions/user', query_string={'message_id': message_id}, headers={'X-User-ID': user_id})
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to get user reactions: Invalid input"}

    @pytest.mark.parametrize("user_id, message_id", [
        (0, None),
        (-1, 5),
        (999999, None),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_boundary_conditions(self, mock_reaction_manager, client, user_id, message_id):
        mock_reaction_manager.get_user_reactions.return_value = []
        
        response = client.get('/api/reactions/user', query_string={'message_id': message_id}, headers={'X-User-ID': user_id})
        
        assert response.status_code == 200
        assert response.get_json() == {"success": True, "user_id": user_id, "reactions": []}

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Database error")
        
        response = client.get('/api/reactions/user', query_string={'message_id': 1}, headers={'X-User-ID': 1})
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to get user reactions: Database error"}

class TestGetReactionCount:
    @pytest.mark.parametrize("message_id, mock_count, expected_response", [
        (1, 5, {"success": True, "message_id": 1, "count": 5}),
        (2, 0, {"success": True, "message_id": 2, "count": 0}),
        (3, -1, {"success": True, "message_id": 3, "count": -1}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager, message_id, mock_count, expected_response):
        mock_reaction_manager.get_reaction_count.return_value = mock_count
        
        response, status_code = get_reaction_count(message_id)
        
        assert status_code == 200
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("message_id", [
        None,
        "",
        "invalid_id"
    ])
    @patch('routes.reactions.reaction_manager')
    def test_invalid_input_types(self, mock_reaction_manager, message_id):
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Invalid message ID")
        
        response, status_code = get_reaction_count(message_id)
        
        assert status_code == 500
        assert response.get_json() == {"error": "Failed to get reaction count: Invalid message ID"}

    @pytest.mark.parametrize("message_id, mock_count", [
        (4, 0),
        (5, -1),
        (6, 1000)
    ])
    @patch('routes.reactions.reaction_manager')
    def test_boundary_conditions(self, mock_reaction_manager, message_id, mock_count):
        mock_reaction_manager.get_reaction_count.return_value = mock_count
        
        response, status_code = get_reaction_count(message_id)
        
        assert status_code == 200
        assert response.get_json() == {"success": True, "message_id": message_id, "count": mock_count}

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager):
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Database error")
        
        response, status_code = get_reaction_count(1)
        
        assert status_code == 500
        assert response.get_json() == {"error": "Failed to get reaction count: Database error"}

class TestGetMostPopular:
    @pytest.mark.parametrize("message_id,expected_emoji", [
        (1, "👍"),
        (2, "❤️"),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager, message_id, expected_emoji):
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        
        response, status_code = get_most_popular(message_id)
        
        assert status_code == 200
        assert response.get_json() == {
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": expected_emoji
        }

    @pytest.mark.parametrize("message_id", [
        None,
        "",
    ])
    @patch('routes.reactions.reaction_manager')
    def test_empty_none_inputs(self, mock_reaction_manager, message_id):
        response, status_code = get_most_popular(message_id)
        
        assert status_code == 500
        assert "error" in response.get_json()

    @pytest.mark.parametrize("message_id", [
        {},  
        [],  
        3.14,  
    ])
    @patch('routes.reactions.reaction_manager')
    def test_invalid_input_types(self, mock_reaction_manager, message_id):
        response, status_code = get_most_popular(message_id)
        
        assert status_code == 500
        assert "error" in response.get_json()

    @pytest.mark.parametrize("message_id", [
        0,
        -1,
        9999999999,
    ])
    @patch('routes.reactions.reaction_manager')
    def test_boundary_conditions(self, mock_reaction_manager, message_id):
        mock_reaction_manager.get_most_popular_emoji.return_value = "👍"
        
        response, status_code = get_most_popular(message_id)
        
        assert status_code == 200
        assert response.get_json()["most_popular_emoji"] == "👍"

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager):
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("Some error")
        
        response, status_code = get_most_popular(1)
        
        assert status_code == 500
        assert "error" in response.get_json()
        assert response.get_json()["error"] == "Failed to get popular emoji: Some error"

class TestGetAllowedEmojis:
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_happy_path(self, mock_get_allowed_emojis, client):
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
    def test_get_allowed_emojis_exception_handling(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.side_effect = Exception("Some error occurred")
        
        response = client.get('/api/reactions/allowed-emojis')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data

    @pytest.mark.parametrize("mock_return_value,expected_emojis", [
        (['😀'], ['😀']),
        (['😀', '😂'], ['😀', '😂']),
        ([], []),
    ])
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_parametrized(self, mock_get_allowed_emojis, client, mock_return_value, expected_emojis):
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
    @pytest.mark.parametrize("user_id,expected_status,expected_response", [
        (1, 200, {"user_id": 1}),
        (None, 401, {"error": "Authentication required"}),
        ("abc", 401, {"error": "Authentication required"}),
        (0, 200, {"user_id": 0}),
        (-1, 200, {"user_id": -1}),
        (2**31 - 1, 200, {"user_id": 2147483647}),
    ])
    @patch('routes.reactions.request')
    def test_decorated_function(self, mock_request, user_id, expected_status, expected_response, client):
        if user_id is not None:
            mock_request.headers = {'X-User-ID': str(user_id)}
            mock_request.args = {}
        else:
            mock_request.headers = {}
            mock_request.args = {}

        response = client.get('/api/reactions/test')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response