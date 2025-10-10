import json
import pytest
from unittest.mock import patch, Mock
from flask import Flask, jsonify

from routes.reactions import require_auth, add_reaction, remove_reaction, toggle_reaction, get_message_reactions, get_user_reactions, get_reaction_count, get_most_popular, get_allowed_emojis, bulk_add_reactions

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    app.add_url_rule('/add_reaction', 'add_reaction', add_reaction, methods=['POST'])
    app.add_url_rule('/remove_reaction', 'remove_reaction', remove_reaction, methods=['POST'])
    app.add_url_rule('/toggle_reaction', 'toggle_reaction', toggle_reaction, methods=['POST'])
    app.add_url_rule('/message/<int:message_id>', 'get_message_reactions', get_message_reactions, methods=['GET'])
    app.add_url_rule('/user', 'get_user_reactions', get_user_reactions, methods=['GET'])
    app.add_url_rule('/count/<int:message_id>', 'get_reaction_count', get_reaction_count, methods=['GET'])
    app.add_url_rule('/popular/<int:message_id>', 'get_most_popular', get_most_popular, methods=['GET'])
    app.add_url_rule('/allowed-emojis', 'get_allowed_emojis', get_allowed_emojis, methods=['GET'])
    app.add_url_rule('/bulk', 'bulk_add_reactions', bulk_add_reactions, methods=['POST'])
    with app.test_client() as client:
        yield client

class TestRequireAuth:
    @pytest.mark.parametrize("user_id,expected_status,expected_response", [
        (1, 200, {"user_id": 1}),
        (2, 200, {"user_id": 2}),
        (0, 200, {"user_id": 0}),
        (-1, 200, {"user_id": -1}),
        (None, 401, {"error": "Authentication required"}),
        ("", 401, {"error": "Authentication required"}),
    ])
    def test_require_auth(self, client, user_id, expected_status, expected_response):
        headers = {}
        if user_id is not None:
            headers['X-User-ID'] = str(user_id)
        
        response = client.get('/add_reaction', headers=headers)
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    def test_missing_user_id_in_query(self, client):
        response = client.get('/add_reaction?user_id=')
        assert response.status_code == 401
        assert response.get_json() == {"error": "Authentication required"}

    def test_invalid_user_id_type(self, client):
        response = client.get('/add_reaction?user_id=invalid')
        assert response.status_code == 401
        assert response.get_json() == {"error": "Authentication required"}

    def test_user_id_as_string(self, client):
        response = client.get('/add_reaction?user_id=123')
        assert response.status_code == 200
        assert response.get_json() == {"user_id": 123}

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
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "Failed to add reaction: message_id must be a positive integer"}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_invalid_input_types(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.add_reaction.side_effect = ValueError("invalid literal for int() with base 10: 'not_an_int'")
        response = client.post('/add_reaction', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 0, "emoji": "👍"}, 400, {"error": "Failed to add reaction: message_id must be a positive integer"}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "Failed to add reaction: message_id must be a positive integer"}),
    ])
    def test_boundary_conditions(self, client, input_data, expected_status, expected_response):
        response = client.post('/add_reaction', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 500, {"error": "Failed to add reaction: some error"}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        mock_reaction_manager.add_reaction.side_effect = Exception("some error")
        response = client.post('/add_reaction', data=json.dumps(input_data), content_type='application/json')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

class TestRemoveReaction:
    @pytest.fixture
    def client(self, app):
        app.add_url_rule('/remove_reaction', 'remove_reaction', remove_reaction, methods=['POST'])
        with app.test_client() as client:
            yield client

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2, "emoji": "👎"}, 404, {"success": False}),
        ({"message_id": 0, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1, "emoji": ""}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1}, 400, {"error": "message_id and emoji are required"}),
        ({"emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        (None, 400, {"error": "message_id and emoji are required"})
    ])
    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        if input_data and 'message_id' in input_data and 'emoji' in input_data:
            if input_data['message_id'] == 2:
                mock_reaction_manager.remove_reaction.return_value = {"success": False}
            else:
                mock_reaction_manager.remove_reaction.return_value = {"success": True}
        
        response = client.post('/remove_reaction', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.remove_reaction.side_effect = Exception("Database error")
        
        input_data = {"message_id": 1, "emoji": "👍"}
        response = client.post('/remove_reaction', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to remove reaction: Database error"}

class TestToggleReaction:
    @pytest.fixture
    def client(self, app):
        app.add_url_rule('/toggle_reaction', 'toggle_reaction', toggle_reaction, methods=['POST'])
        with app.test_client() as client:
            yield client

    @pytest.mark.parametrize("data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 0, "emoji": "👍"}, 400, {"error": "Failed to toggle reaction: Invalid message_id"}),
        ({"message_id": -1, "emoji": "👍"}, 400, {"error": "Failed to toggle reaction: Invalid message_id"}),
        ({"message_id": 1, "emoji": ""}, 400, {"error": "Failed to toggle reaction: Invalid emoji"}),
        ({"message_id": 1}, 400, {"error": "message_id and emoji are required"}),
        ({"emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        (None, 400, {"error": "message_id and emoji are required"}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_toggle_reaction(self, mock_reaction_manager, client, data, expected_status, expected_response):
        if expected_status == 200:
            mock_reaction_manager.toggle_reaction.return_value = {"success": True}
        else:
            mock_reaction_manager.toggle_reaction.side_effect = ValueError("Invalid message_id") if "Invalid message_id" in expected_response["error"] else ValueError("Invalid emoji")

        response = client.post('/toggle_reaction', data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.toggle_reaction.side_effect = Exception("Unexpected error")
        
        response = client.post('/toggle_reaction', data=json.dumps({"message_id": 1, "emoji": "👍"}), content_type='application/json')
        
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
    @pytest.fixture
    def client(self, app):
        app.add_url_rule('/user/reactions', 'get_user_reactions', get_user_reactions)
        with app.test_client() as client:
            yield client

    @pytest.mark.parametrize("user_id, message_id, expected_reactions, expected_status", [
        (1, None, [{"message_id": 1, "reaction": "like"}], 200),
        (1, 2, [], 200),
        (0, None, [], 200),
        (-1, None, [], 200),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_get_user_reactions(self, mock_reaction_manager, client, user_id, message_id, expected_reactions, expected_status):
        mock_reaction_manager.get_user_reactions.return_value = expected_reactions
        
        response = client.get('/user/reactions', query_string={'message_id': message_id}, headers={'X-User-ID': str(user_id)})
        
        assert response.status_code == expected_status
        assert response.json == {
            "success": True,
            "user_id": user_id,
            "reactions": expected_reactions
        }

    @patch('routes.reactions.reaction_manager')
    def test_get_user_reactions_exception(self, mock_reaction_manager, client):
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Database error")
        
        response = client.get('/user/reactions', query_string={'message_id': 1}, headers={'X-User-ID': '1'})
        
        assert response.status_code == 500
        assert response.json == {"error": "Failed to get user reactions: Database error"}

    @pytest.mark.parametrize("user_id, message_id", [
        (None, None),
        ("string", None),
        (1, "string"),
    ])
    def test_invalid_inputs(self, client, user_id, message_id):
        response = client.get('/user/reactions', query_string={'message_id': message_id}, headers={'X-User-ID': str(user_id) if user_id is not None else ''})
        
        assert response.status_code == 500

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
        {},
        [],
    ])
    @patch('routes.reactions.reaction_manager')
    def test_empty_none_inputs(self, mock_reaction_manager, message_id):
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Invalid message ID")
        
        response, status_code = get_reaction_count(message_id)
        
        assert status_code == 500
        assert response.get_json() == {"error": "Failed to get reaction count: Invalid message ID"}

    @pytest.mark.parametrize("message_id", [
        "string",
        3.14,
        object(),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_invalid_input_types(self, mock_reaction_manager, message_id):
        mock_reaction_manager.get_reaction_count.side_effect = Exception("Invalid message ID")
        
        response, status_code = get_reaction_count(message_id)
        
        assert status_code == 500
        assert response.get_json() == {"error": "Failed to get reaction count: Invalid message ID"}

    @pytest.mark.parametrize("message_id, mock_count", [
        (4, 0),
        (5, 1),
        (6, 1000),
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
    def test_empty_or_invalid_inputs(self, mock_reaction_manager, message_id):
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
    def test_get_allowed_emojis_happy_path(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.return_value = ['😀', '😂', '😍']
        
        response = client.get('/allowed-emojis')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == ['😀', '😂', '😍']

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_empty_list(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.return_value = []
        
        response = client.get('/allowed-emojis')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == []

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_exception_handling(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.side_effect = Exception("Some error occurred")
        
        response = client.get('/allowed-emojis')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data

    @pytest.mark.parametrize("mock_return_value,expected_emojis", [
        (['😀', '😂', '😍'], ['😀', '😂', '😍']),
        ([], []),
        (None, []),
    ])
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_various_cases(self, mock_get_allowed_emojis, client, mock_return_value, expected_emojis):
        mock_get_allowed_emojis.return_value = mock_return_value
        
        response = client.get('/allowed-emojis')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == expected_emojis

class TestBulkAddReactions:
    @pytest.fixture
    def client(self, app):
        app.add_url_rule('/bulk', 'bulk_add_reactions', bulk_add_reactions, methods=['POST'])
        with app.test_client() as client:
            yield client

    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
        ({"reactions": []}, 400, {"error": "reactions array is required"}),
        (None, 400, {"error": "reactions array is required"}),
        ({"reactions": [{"message_id": 0, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
        ({"reactions": [{"message_id": -1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
        ({"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
    ])
    @patch('routes.reactions.reaction_manager.bulk_add_reactions')
    def test_bulk_add_reactions(self, mock_bulk_add, client, input_data, expected_status, expected_response):
        if expected_status == 200:
            mock_bulk_add.return_value = "Reactions added"
        else:
            mock_bulk_add.side_effect = Exception("Failed to add reactions")

        response = client.post('/bulk', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager.bulk_add_reactions')
    def test_exception_handling(self, mock_bulk_add, client):
        mock_bulk_add.side_effect = Exception("Failed to bulk add reactions")
        
        response = client.post('/bulk', data=json.dumps({"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to bulk add reactions: Failed to bulk add reactions"}

class TestDecoratedFunction:
    @pytest.mark.parametrize("user_id,expected_status,expected_response", [
        (1, 200, "Success"),
        (None, 401, {"error": "Authentication required"}),
        ("abc", 401, {"error": "Authentication required"}),
        (0, 200, "Success"),
        (-1, 200, "Success"),
        (2**31 - 1, 200, "Success"),
    ])
    @patch('routes.reactions.request')
    def test_decorated_function(self, mock_request, user_id, expected_status, expected_response, client):
        if user_id is not None:
            mock_request.headers = {'X-User-ID': str(user_id)}
        else:
            mock_request.headers = {}
        
        mock_function = Mock(return_value="Success")
        
        response = decorated_function(mock_function)
        
        assert response[1] == expected_status
        
        if isinstance(expected_response, dict):
            assert response[0].get_json() == expected_response
        else:
            assert response[0] == expected_response