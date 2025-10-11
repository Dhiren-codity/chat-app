import json
import pytest
from unittest.mock import patch, Mock
from flask import Flask

from routes.reactions import require_auth, add_reaction, remove_reaction, toggle_reaction, get_message_reactions, get_user_reactions, get_reaction_count, get_most_popular, get_allowed_emojis, bulk_add_reactions

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(require_auth)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

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
        headers = {'X-User-ID': str(user_id)} if user_id is not None else {}
        response = client.get('/test', headers=headers)
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    def test_require_auth_no_user_id(self, client):
        response = client.get('/test')
        assert response.status_code == 401
        assert response.get_json() == {"error": "Authentication required"}

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

        response = client.post('/add_reaction', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.add_reaction.side_effect = Exception("Unexpected error")

        response = client.post('/add_reaction', data=json.dumps({"message_id": 1, "emoji": "👍"}), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to add reaction: Unexpected error"}

class TestRemoveReaction:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 2, "emoji": "👎"}, 404, {"success": False}),
        ({"message_id": 0, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": -1, "emoji": "👍"}, 404, {"success": False}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_remove_reaction_happy_path(self, mock_reaction_manager, client, input_data, expected_status, expected_response):
        user_id = 123
        mock_reaction_manager.remove_reaction.return_value = expected_response
        
        response = client.post('/remove_reaction', data=json.dumps(input_data), content_type='application/json', headers={'user_id': str(user_id)})
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    def test_empty_input(self, client):
        user_id = 123
        response = client.post('/remove_reaction', data=json.dumps({}), content_type='application/json', headers={'user_id': str(user_id)})
        
        assert response.status_code == 400
        assert response.get_json() == {"error": "message_id and emoji are required"}

    @pytest.mark.parametrize("input_data", [
        {"message_id": "not_an_int", "emoji": "👍"},
        {"message_id": 1, "emoji": 123},
        {"message_id": None, "emoji": "👍"},
        {"message_id": 1, "emoji": None},
    ])
    def test_invalid_input_types(self, client, input_data):
        user_id = 123
        response = client.post('/remove_reaction', data=json.dumps(input_data), content_type='application/json', headers={'user_id': str(user_id)})
        
        assert response.status_code == 400
        assert response.get_json() == {"error": "message_id and emoji are required"}

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client):
        user_id = 123
        mock_reaction_manager.remove_reaction.side_effect = Exception("Database error")
        
        input_data = {"message_id": 1, "emoji": "👍"}
        response = client.post('/remove_reaction', data=json.dumps(input_data), content_type='application/json', headers={'user_id': str(user_id)})
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to remove reaction: Database error"}

class TestToggleReaction:
    @pytest.mark.parametrize("data,expected_status,expected_response", [
        ({"message_id": 1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": None, "emoji": "👍"}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": 1, "emoji": None}, 400, {"error": "message_id and emoji are required"}),
        ({"message_id": "not_an_int", "emoji": "👍"}, 400, {"error": "Failed to toggle reaction: invalid literal for int() with base 10: 'not_an_int'"}),
        ({"message_id": -1, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 0, "emoji": "👍"}, 200, {"success": True}),
        ({"message_id": 9999999999, "emoji": "👍"}, 200, {"success": True}),
    ])
    @patch('routes.reactions.reaction_manager.toggle_reaction')
    def test_toggle_reaction(self, mock_toggle_reaction, client, data, expected_status, expected_response):
        mock_toggle_reaction.return_value = {"success": True}
        
        response = client.post('/toggle_reaction', data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager.toggle_reaction')
    def test_toggle_reaction_value_error(self, mock_toggle_reaction, client):
        mock_toggle_reaction.side_effect = ValueError("Invalid emoji")
        
        response = client.post('/toggle_reaction', data=json.dumps({"message_id": 1, "emoji": "👍"}), content_type='application/json')
        
        assert response.status_code == 400
        assert response.get_json() == {"error": "Invalid emoji"}

    @patch('routes.reactions.reaction_manager.toggle_reaction')
    def test_toggle_reaction_general_exception(self, mock_toggle_reaction, client):
        mock_toggle_reaction.side_effect = Exception("Some unexpected error")
        
        response = client.post('/toggle_reaction', data=json.dumps({"message_id": 1, "emoji": "👍"}), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to toggle reaction: Some unexpected error"}

class TestGetMessageReactions:
    @pytest.mark.parametrize("message_id, reactions, expected_status, expected_response", [
        (1, [{"emoji": "👍", "count": 5}], 200, {"success": True, "message_id": 1, "reactions": [{"emoji": "👍", "count": 5}]}),
        (2, [], 200, {"success": True, "message_id": 2, "reactions": []}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_get_message_reactions(self, mock_reaction_manager, message_id, reactions, expected_status, expected_response):
        mock_reaction_manager.get_message_reactions.return_value = reactions
        
        response = get_message_reactions(message_id)
        
        assert response[1] == expected_status
        assert json.loads(response[0].data) == expected_response

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager):
        mock_reaction_manager.get_message_reactions.side_effect = Exception("Database error")
        
        response = get_message_reactions(1)
        
        assert response[1] == 500
        assert json.loads(response[0].data) == {"error": "Failed to get reactions: Database error"}

class TestGetUserReactions:
    @pytest.mark.parametrize("user_id, message_id, mock_reactions, expected_status, expected_json", [
        (1, None, ["like", "love"], 200, {"success": True, "user_id": 1, "reactions": ["like", "love"]}),
        (2, 5, [], 200, {"success": True, "user_id": 2, "reactions": []}),
        (3, 10, ["laugh"], 200, {"success": True, "user_id": 3, "reactions": ["laugh"]}),
        (4, None, ["angry", "sad"], 200, {"success": True, "user_id": 4, "reactions": ["angry", "sad"]}),
    ])
    @patch('routes.reactions.reaction_manager')
    def test_happy_path(self, mock_reaction_manager, client, user_id, message_id, mock_reactions, expected_status, expected_json):
        mock_reaction_manager.get_user_reactions.return_value = mock_reactions
        
        response = client.get('/user/reactions', query_string={'message_id': message_id}, headers={'user_id': str(user_id)})
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_json

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager, client):
        mock_reaction_manager.get_user_reactions.side_effect = Exception("Database error")
        
        response = client.get('/user/reactions', query_string={'message_id': 1}, headers={'user_id': '1'})
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to get user reactions: Database error"}

class TestGetReactionCount:
    @pytest.mark.parametrize("message_id, mock_count, expected_response", [
        (1, 5, {"success": True, "message_id": 1, "count": 5}),
        (2, 0, {"success": True, "message_id": 2, "count": 0}),
    ])
    def test_happy_path(self, message_id, mock_count, expected_response):
        with patch('routes.reactions.reaction_manager') as mock_reaction_manager:
            mock_reaction_manager.get_reaction_count.return_value = mock_count
            
            response, status_code = get_reaction_count(message_id)
            
            assert status_code == 200
            assert response.get_json() == expected_response

    def test_exception_handling(self):
        with patch('routes.reactions.reaction_manager') as mock_reaction_manager:
            mock_reaction_manager.get_reaction_count.side_effect = Exception("Database error")
            
            response, status_code = get_reaction_count(1)
            
            assert status_code == 500
            assert "error" in response.get_json()
            assert "Failed to get reaction count" in response.get_json()["error"]

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

    @patch('routes.reactions.reaction_manager')
    def test_exception_handling(self, mock_reaction_manager):
        message_id = 123
        mock_reaction_manager.get_most_popular_emoji.side_effect = Exception("Some error occurred")
        
        response, status_code = get_most_popular(message_id)
        
        assert status_code == 500
        assert response.json == {"error": "Failed to get popular emoji: Some error occurred"}

class TestGetAllowedEmojis:
    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_success(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.return_value = ['😀', '😂', '😍']
        
        response = client.get('/get_allowed_emojis')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == ['😀', '😂', '😍']

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_empty(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.return_value = []
        
        response = client.get('/get_allowed_emojis')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['emojis'] == []

    @patch('routes.reactions.ReactionManager.get_allowed_emojis')
    def test_get_allowed_emojis_exception(self, mock_get_allowed_emojis, client):
        mock_get_allowed_emojis.side_effect = Exception("Some error occurred")
        
        response = client.get('/get_allowed_emojis')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data

class TestBulkAddReactions:
    @pytest.mark.parametrize("input_data,expected_status,expected_response", [
        ({"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}, 200, {"success": True, "result": "Reactions added"}),
        ({"reactions": []}, 400, {"error": "reactions array is required"}),
        (None, 400, {"error": "reactions array is required"}),
    ])
    @patch('routes.reactions.reaction_manager.bulk_add_reactions')
    def test_bulk_add_reactions(self, mock_bulk_add_reactions, client, input_data, expected_status, expected_response):
        mock_bulk_add_reactions.return_value = "Reactions added"
        
        response = client.post('/bulk_add_reactions', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

    @patch('routes.reactions.reaction_manager.bulk_add_reactions')
    def test_bulk_add_reactions_exception(self, mock_bulk_add_reactions, client):
        mock_bulk_add_reactions.side_effect = Exception("Database error")
        
        input_data = {"reactions": [{"message_id": 1, "user_id": 1, "emoji": "👍"}]}
        response = client.post('/bulk_add_reactions', data=json.dumps(input_data), content_type='application/json')
        
        assert response.status_code == 500
        assert response.get_json() == {"error": "Failed to bulk add reactions: Database error"}