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
        ("invalid", 401, {"error": "Authentication required"}),
        (0, 200, {"user_id": 0}),
        (-1, 200, {"user_id": -1}),
        (2**31 - 1, 200, {"user_id": 2147483647}),
    ])
    def test_require_auth(self, client, user_id, expected_status, expected_response):
        if user_id is not None:
            with client.session_transaction() as sess:
                sess['X-User-ID'] = user_id
        response = client.get('/test', query_string={'user_id': user_id} if user_id is not None else {})
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    def test_error_handling(self, client):
        response = client.get('/test')
        assert response.status_code == 401
        assert response.get_json() == {"error": "Authentication required"}

    @pytest.mark.parametrize("user_id", [
        (None),
        ("invalid"),
        (3.14),
        (object()),
    ])
    def test_invalid_input_types(self, client, user_id):
        if user_id is not None:
            with client.session_transaction() as sess:
                sess['X-User-ID'] = user_id
        response = client.get('/test', query_string={'user_id': user_id} if user_id is not None else {})
        assert response.status_code == 401
        assert response.get_json() == {"error": "Authentication required"}

class TestAddReaction:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2, "emoji": "😊"}, 200, {"success": True}),
        ({"message_id": 0, "emoji": "👍"}, 400, {"error": "Failed to add reaction: Invalid message_id"}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "Failed to add reaction: Invalid message_id"}),
        ({"message_id": 1, "emoji": ""}, 400, {"error": "Failed to add reaction: Invalid emoji"}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_add_reaction(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.add_reaction.return_value = expected_response
        response = client.post('/add', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_error", [
        (None, {"error": "message_id and emoji are required"}),
        ({}, {"error": "message_id and emoji are required"}),
        ({"message_id": 1}, {"error": "message_id and emoji are required"}),
        ({"emoji": "👍"}, {"error": "message_id and emoji are required"}),
    ])
    def test_add_reaction_missing_fields(self, client, input_data, expected_error):
        response = client.post('/add', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == 400
        assert response.get_json() == expected_error

    @patch('routes.reactions.reaction_manager')
    def test_add_reaction_value_error(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.side_effect = ValueError("Invalid input")
        input_data = {"message_id": 1, "emoji": "👍"}
        response = client.post('/add', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == 400
        assert response.get_json() == {"error": "Invalid input"}

    @patch('routes.reactions.reaction_manager')
    def test_add_reaction_exception(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.side_effect = Exception("Some error occurred")
        input_data = {"message_id": 1, "emoji": "👍"}
        response = client.post('/add', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to add reaction: Some error occurred"}

class TestRemoveReaction:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2, "emoji": "👎"}, 404, {"success": False}),
        ({"message_id": 0, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": -1, "emoji": "👍"}, 404, {"success": False}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction_happy_path(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.remove_reaction.return_value = expected_response
        response = client.post('/remove', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_error", [
        (None, 400, {"error": "message_id and emoji are required"}),
        ({}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1}, 400, {"error": "message_id and emoji are required"}),
        ({"emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
    ])
    def test_remove_reaction_empty_none_inputs(self, client, input_data, expected_status, expected_error):
        response = client.post('/remove', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_error

    @pytest.mark.parametrize("input_data,expected_status,expected_error", [
        ({"message_id": "string", "emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1, "emoji": 123}, 400, {"error": "message_id and emoji are required"}),
    ])
    def test_remove_reaction_invalid_input_types(self, client, input_data, expected_status, expected_error):
        response = client.post('/remove', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_error

    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.remove_reaction.side_effect = Exception("Database error")
        input_data = {"message_id": 1, "emoji": "👍"}
        response = client.post('/remove', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to remove reaction: Database error"}

class TestToggleReaction:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": None, "emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1, "emoji": None}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": "not_an_int", "emoji": "👍"}, 400, {"error": "Failed to toggle reaction: invalid literal for int() with base 10: 'not_an_int'"}),
        ({"message_id": -1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 0, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 9999999999, "emoji": "👍"}, 200, {"success": True}),
    ])
    @patch('routes.reactions.reaction_manager.toggle_reaction')
    def test_toggle_reaction(self, mock_toggle_reaction, client, input_data, expected_status, expected_response):
        mock_toggle_reaction.return_value = {"success": True}
        response = client.post('/toggle', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager.toggle_reaction')
    def test_toggle_reaction_value_error(self, mock_toggle_reaction, client):
        mock_toggle_reaction.side_effect = ValueError("Invalid emoji")
        response = client.post('/toggle', data=json.dumps({"message_id": 1, "emoji": "👍"}), content_type='application/json')
        assert response.status_code == 400
        assert response.get_json() == {"error": "Invalid emoji"}

    @patch('routes.reactions.reaction_manager.toggle_reaction')
    def test_toggle_reaction_general_exception(self, mock_toggle_reaction, client):
        mock_toggle_reaction.side_effect = Exception("Some error occurred")
        response = client.post('/toggle', data=json.dumps({"message_id": 1, "emoji": "👍"}), content_type='application/json')
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to toggle reaction: Some error occurred"}

class TestGetMessageReactions:
    @pytest.mark.parametrize("message_id,expected_reactions,expected_status", [
        (1, [{"emoji": "👍", "count": 5}], 200),
        (2, [], 200),
        (None, None, 500),
        ("invalid_id", None, 500),
        (-1, None, 500),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_get_message_reactions(self, mock_reaction_manager, message_id, expected_reactions, expected_status):
        if expected_status == 200:
            mock_reaction_manager.get_message_reactions.return_value = expected_reactions
        else:
            mock_reaction_manager.get_message_reactions.side_effect = Exception("Mocked exception")

        response = get_message_reactions(message_id)

        assert response[1] == expected_status
        if expected_status == 200:
            response_data = json.loads(response[0])
            assert response_data["success"] is True
            assert response_data["message_id"] == message_id
            assert response_data["reactions"] == expected_reactions
        else:
            response_data = json.loads(response[0])
            assert "error" in response_data
            assert response_data["error"] == "Failed to get reactions: Mocked exception"

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
        response = client.get('/user', query_string={'message_id': message_id}, headers={'X-User-ID': str(user_id)})
        assert response.status_code == expected_status
        assert response.get_json() == {
            "success": True,
            "user_id": user_id,
            "reactions": expected_reactions
        }

    @patch('routes.reactions.reaction_manager')
    def test_get_user_reactions_exception(self, mock_reaction_manager, client):
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Database error")
        response = client.get('/user', query_string={'message_id': 1}, headers={'X-User-ID': '1'})
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to get user reactions: Database error"}

    @pytest.mark.parametrize("user_id, message_id", [
        (None, None),
        ("string", None),
        (1, "string"),
    ])
    def test_invalid_inputs(self, client, user_id, message_id):
        response = client.get('/user', query_string={'message_id': message_id}, headers={'X-User-ID': str(user_id)})
        assert response.status_code == 500

class TestGetReactionCount:
    @pytest.mark.parametrize("message_id, mock_count, expected_response", [
        (1, 5, {"success": True, "message_id": 1, "count": 5}),
        (2, 0, {"success": True, "message_id": 2, "count": 0}),
        (3, -1, {"success": True, "message_id": 3, "count": -1}),
        (4, 1000000, {"success": True, "message_id": 4, "count": 1000000}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager, message_id, mock_count, expected_response):
        mock_reaction_manager.get_reaction_count.return_value = mock_count
        response, status_code = get_reaction_count(message_id)
        assert status_code == 200
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("message_id", [None, "", "invalid_id"])
    @patch('routes.reactions.reaction_manager')
    def test_invalid_inputs(self, mock_reaction_manager, message_id):
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Invalid message ID")
        response, status_code = get_reaction_count(message_id)
        assert status_code == 500
        assert response.get_json() == {"error": "Failed to get reaction count: Invalid message ID"}

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager):
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Database error")
        response, status_code = get_reaction_count(1)
        assert status_code == 500
        assert response.get_json() == {"error": "Failed to get reaction count: Database error"}

class TestGetMostPopular:
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager):
        message_id = 123
        expected_emoji = "😊"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        response, status_code = get_most_popular(message_id)
        assert status_code == 200
        assert response.get_json() == {
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
        assert response.get_json() == {"error": "Failed to get popular emoji: Invalid input"}

    @pytest.mark.parametrize("message_id", [1, 2, 3, 1000])
    @patch('routes.reactions.reaction_manager')
    def test_boundary_conditions(self, mock_reaction_manager, message_id):
        expected_emoji = "👍"
        mock_reaction_manager.get_most_popular_emoji.return_value = expected_emoji
        response, status_code = get_most_popular(message_id)
        assert status_code == 200
        assert response.get_json() == {
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
        assert response.get_json() == {"error": "Failed to get popular emoji: Database error"}

class TestGetAllowedEmojis:
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_happy_path(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.return_value = ['😀', '😂', '😍']
        response = client.get('/allowed-emojis')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['emojis'] == ['😀', '😂', '😍']

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_empty_list(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.return_value = []
        response = client.get('/allowed-emojis')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['emojis'] == []

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_exception_handling(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.side_effect = Exception("Some error occurred")
        response = client.get('/allowed-emojis')
        assert response.status_code == 500
        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data

    @pytest.mark.parametrize("mock_return_value,expected_emojis", [
        (['😀', '😂', '😍'], ['😀', '😂', '😍']),
        ([], []),
        (None, []),
    ])
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_various_cases(self, mock_get_allowed_emojis, mock_return_value, expected_emojis, client):
        mock_get_allowed_emojis.return_value = mock_return_value
        response = client.get('/allowed-emojis')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['emojis'] == expected_emojis

class TestBulkAddReactions:
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager, client):
        mock_reaction_manager.bulk_add_reactions.return_value = {"added": 3}
        payload = {
            "reactions": [
                {"message_id": 1, "user_id": 1, "emoji": "👍"},
                {"message_id": 2, "user_id": 1, "emoji": "❤️"},
                {"message_id": 3, "user_id": 1, "emoji": "😂"}
            ]
        }
        response = client.post('/bulk', data=json.dumps(payload), content_type='application/json')
        assert response.status_code == 200
        assert response.get_json() == {
            "success": True,
            "result": {"added": 3}
        }

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        (None, 400, {"error": "reactions array is required"}),
        ({}, 400, {"error": "reactions array is required"}),
        ({"reactions": []}, 400, {"error": "reactions array is required"}),
    ])
    def test_empty_or_none_inputs(self, client, input_data, expected_status, expected_response):
        response = client.post('/bulk', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"reactions": [{"message_id": "not_an_int", "user_id": 1, "emoji": "👍"}]}, 400, {"error": "reactions array is required"}),
        ({"reactions": [{"message_id": 1, "user_id": "not_an_int", "emoji": "👍"}]}, 400, {"error": "reactions array is required"}),
        ({"reactions": [{"message_id": 1, "user_id": 1, "emoji": 123}]}, 400, {"error": "reactions array is required"}),
    ])
    def test_invalid_input_types(self, client, input_data, expected_status, expected_response):
        response = client.post('/bulk', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"reactions": [{"message_id": 0, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": {"added": 1}}),
        ({"reactions": [{"message_id": -1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": {"added": 1}}),
        ({"reactions": [{"message_id": 2147483647, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": {"added": 1}}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_boundary_conditions(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.bulk_add_reactions.return_value = {"added": 1}
        response = client.post('/bulk', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.bulk_add_reactions.side_effect = Exception("Database error")
        payload = {
            "reactions": [
                {"message_id": 1, "user_id": 1, "emoji": "👍"}
            ]
        }
        response = client.post('/bulk', data=json.dumps(payload), content_type='application/json')
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

        response = client.get('/test')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    def test_exception_handling(self, client):
        with patch('routes.reactions.request', side_effect=Exception("Unexpected error")):
            response = client.get('/test')
            assert response.status_code == 500