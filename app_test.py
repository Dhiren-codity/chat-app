"""
Auto-generated tests using LLM and RAG
"""

from unittest.mock import MagicMock, patch, Mock
import pytest


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import login
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestLogin:
    @patch('app.User')

    def test_login_success(self, mock_user, client):
        mock_user.query.filter_by.return_value.first.return_value = Mock(
            id=1, check_password=Mock(return_value=True), create_session=Mock(return_value='session_token')
        )
        response = client.post('/login', json={'username': 'testuser', 'password': 'correctpassword'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['token'] == 'session_token'
        assert data['user_id'] == 1

    @patch('app.User')

    def test_login_invalid_credentials(self, mock_user, client):
        mock_user.query.filter_by.return_value.first.return_value = Mock(
            check_password=Mock(return_value=False)
        )
        response = client.post('/login', json={'username': 'testuser', 'password': 'wrongpassword'})
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'Invalid credentials'

    @pytest.mark.parametrize("username,password", [
        ('', 'password'),
        ('username', ''),
        ('', ''),
        (None, 'password'),
        ('username', None),
    ])
    @patch('app.User')

    def test_login_edge_cases(self, mock_user, client, username, password):
        mock_user.query.filter_by.return_value.first.return_value = None
        response = client.post('/login', json={'username': username, 'password': password})
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'Invalid credentials'

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import app
from app import get_messages

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetMessages:
    @patch('app.Message.query')

    def test_get_messages_happy_path(self, mock_query, client):
        # Mock the database query
        mock_message = Mock(id=1, user_id=1, content="Hello", created_at=Mock(isoformat=lambda: "2023-10-01T12:00:00"))
        mock_query.filter_by.return_value.order_by.return_value.all.return_value = [mock_message]

        response = client.get('/get_messages?room_id=1')
        assert response.status_code == 200
        data = response.get_json()
        assert data == [{
            'id': 1,
            'user_id': 1,
            'content': "Hello",
            'created_at': "2023-10-01T12:00:00"
        }]

    @patch('app.Message.query')

    def test_get_messages_no_messages(self, mock_query, client):
        # Mock the database query to return no messages
        mock_query.filter_by.return_value.order_by.return_value.all.return_value = []

        response = client.get('/get_messages?room_id=1')
        assert response.status_code == 200
        data = response.get_json()
        assert data == []

    @pytest.mark.parametrize("room_id, expected_status", [
        (None, 400),
        ("", 400),
        ("nonexistent", 200)  # Assuming no error for non-existent room_id
    ])
    @patch('app.Message.query')

    def test_get_messages_edge_cases(self, mock_query, client, room_id, expected_status):
        # Mock the database query
        mock_query.filter_by.return_value.order_by.return_value.all.return_value = []

        response = client.get(f'/get_messages?room_id={room_id}')
        assert response.status_code == expected_status

# Third-party
# Local


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import update_status
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestUpdateStatus:
    @patch('app.status_manager')

    def test_update_status_happy_path(self, mock_status_manager, client):
        mock_status_manager.update_user_status.return_value = None
        response = client.post('/update_status', json={'user_id': 1, 'is_online': True})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    @patch('app.status_manager')

    def test_update_status_missing_user_id(self, mock_status_manager, client):
        response = client.post('/update_status', json={'is_online': True})
        assert response.status_code == 400

    @patch('app.status_manager')

    def test_update_status_missing_is_online(self, mock_status_manager, client):
        response = client.post('/update_status', json={'user_id': 1})
        assert response.status_code == 400

    @pytest.mark.parametrize("user_id,is_online,expected_status", [
        (None, True, 400),
        (1, None, 400),
        (1, True, 200),
        (1, False, 200),
    ])
    @patch('app.status_manager')

    def test_update_status_various_inputs(self, mock_status_manager, client, user_id, is_online, expected_status):
        response = client.post('/update_status', json={'user_id': user_id, 'is_online': is_online})
        assert response.status_code == expected_status

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import get_status
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetStatus:
    @patch('app.status_manager')

    def test_get_status_happy_path(self, mock_status_manager, client):
        mock_status_manager.get_user_status.return_value = {'status': 'active'}
        response = client.get('/get_status?user_id=1')
        assert response.status_code == 200
        assert response.get_json() == {'status': 'active'}

    @patch('app.status_manager')

    def test_get_status_user_not_found(self, mock_status_manager, client):
        mock_status_manager.get_user_status.return_value = None
        response = client.get('/get_status?user_id=999')
        assert response.status_code == 404

    @pytest.mark.parametrize("user_id,expected_status", [
        (1, {'status': 'active'}),
        (2, {'status': 'inactive'}),
        (3, {'status': 'busy'}),
    ])
    @patch('app.status_manager')

    def test_get_status_various_users(self, mock_status_manager, client, user_id, expected_status):
        mock_status_manager.get_user_status.return_value = expected_status
        response = client.get(f'/get_status?user_id={user_id}')
        assert response.status_code == 200
        assert response.get_json() == expected_status

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import start_typing
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestStartTyping:
    @patch('app.typing_indicator')

    def test_happy_path(self, mock_typing_indicator, client):
        mock_typing_indicator.user_started_typing = Mock()
        response = client.post('/start_typing', json={
            'room_id': 'room123',
            'user_id': 'user456',
            'username': 'testuser'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        mock_typing_indicator.user_started_typing.assert_called_once_with('room123', 'user456', 'testuser')

    @patch('app.typing_indicator')

    def test_missing_room_id(self, mock_typing_indicator, client):
        response = client.post('/start_typing', json={
            'user_id': 'user456',
            'username': 'testuser'
        })
        assert response.status_code == 400  # Assuming 400 for bad request
        mock_typing_indicator.user_started_typing.assert_not_called()

    @pytest.mark.parametrize("json_data", [
        {'room_id': 'room123', 'username': 'testuser'},  # Missing user_id
        {'room_id': 'room123', 'user_id': 'user456'},    # Missing username
        {}                                               # Missing all
    ])
    @patch('app.typing_indicator')

    def test_missing_parameters(self, mock_typing_indicator, client, json_data):
        response = client.post('/start_typing', json=json_data)
        assert response.status_code == 400  # Assuming 400 for bad request
        mock_typing_indicator.user_started_typing.assert_not_called()

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import app
from app import stop_typing

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestStopTyping:
    @patch('app.typing_indicator')

    def test_stop_typing_happy_path(self, mock_typing_indicator, client):
        mock_typing_indicator.user_stopped_typing = Mock()
        response = client.post('/stop_typing', json={'room_id': '123', 'user_id': '456'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        mock_typing_indicator.user_stopped_typing.assert_called_once_with('123', '456')

    @pytest.mark.parametrize("json_data", [
        {'room_id': None, 'user_id': '456'},
        {'room_id': '123', 'user_id': None},
        {'room_id': '', 'user_id': '456'},
        {'room_id': '123', 'user_id': ''},
    ])
    @patch('app.typing_indicator')

    def test_stop_typing_edge_cases(self, mock_typing_indicator, client, json_data):
        mock_typing_indicator.user_stopped_typing = Mock()
        response = client.post('/stop_typing', json=json_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        mock_typing_indicator.user_stopped_typing.assert_called_once_with(
            json_data['room_id'], json_data['user_id']
        )

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import get_typing_users
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetTypingUsers:
    @patch('app.typing_indicator.get_typing_users')

    def test_happy_path(self, mock_get_typing_users, client):
        mock_get_typing_users.return_value = ['user1', 'user2']
        response = client.get('/get_typing_users?room_id=123')
        assert response.status_code == 200
        assert response.get_json() == ['user1', 'user2']

    @patch('app.typing_indicator.get_typing_users')

    def test_no_typing_users(self, mock_get_typing_users, client):
        mock_get_typing_users.return_value = []
        response = client.get('/get_typing_users?room_id=123')
        assert response.status_code == 200
        assert response.get_json() == []

    @patch('app.typing_indicator.get_typing_users')

    def test_typing_users_error(self, mock_get_typing_users, client):
        mock_get_typing_users.side_effect = Exception("Database error")
        response = client.get('/get_typing_users?room_id=123')
        assert response.status_code == 500
        assert 'error' in response.get_json()

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import create_group
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestCreateGroup:
    @patch('app.group_manager.create_group')

    def test_create_group_happy_path(self, mock_create_group, client):
        mock_create_group.return_value = {'id': 1, 'name': 'Test Group', 'creator_id': 1, 'members': [2, 3]}
        
        response = client.post('/create_group', json={
            'name': 'Test Group',
            'creator_id': 1,
            'member_ids': [2, 3]
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1
        assert data['name'] == 'Test Group'
        assert data['creator_id'] == 1
        assert data['members'] == [2, 3]

    @patch('app.group_manager.create_group')

    def test_create_group_missing_name(self, mock_create_group, client):
        response = client.post('/create_group', json={
            'creator_id': 1,
            'member_ids': [2, 3]
        })
        
        assert response.status_code == 400  # Assuming 400 for bad request

    @pytest.mark.parametrize("name,creator_id,member_ids,expected_status", [
        ('', 1, [2, 3], 400),  # Empty name
        ('Test Group', None, [2, 3], 400),  # Missing creator_id
        ('Test Group', 1, None, 200),  # No members
    ])
    @patch('app.group_manager.create_group')

    def test_create_group_edge_cases(self, mock_create_group, client, name, creator_id, member_ids, expected_status):
        mock_create_group.return_value = {'id': 1, 'name': name, 'creator_id': creator_id, 'members': member_ids or []}
        
        response = client.post('/create_group', json={
            'name': name,
            'creator_id': creator_id,
            'member_ids': member_ids
        })
        
        assert response.status_code == expected_status

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import rename_group
from flask import app  # ✅ CRITICAL: Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestRenameGroup:
    @patch('app.group_manager.update_group_name')

    def test_rename_group_happy_path(self, mock_update_group_name, client):
        mock_update_group_name.return_value = {'success': True}
        response = client.post('/rename_group/1', json={'new_name': 'New Group Name', 'user_id': 123})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    @patch('app.group_manager.update_group_name')

    def test_rename_group_missing_new_name(self, mock_update_group_name, client):
        response = client.post('/rename_group/1', json={'user_id': 123})
        assert response.status_code == 400

    @patch('app.group_manager.update_group_name')

    def test_rename_group_missing_user_id(self, mock_update_group_name, client):
        response = client.post('/rename_group/1', json={'new_name': 'New Group Name'})
        assert response.status_code == 400

    @pytest.mark.parametrize("new_name,user_id,expected_status", [
        ('', 123, 400),  # Empty new name
        ('Valid Name', None, 400),  # Missing user_id
        (None, 123, 400),  # Missing new_name
    ])
    @patch('app.group_manager.update_group_name')

    def test_rename_group_edge_cases(self, mock_update_group_name, client, new_name, user_id, expected_status):
        response = client.post('/rename_group/1', json={'new_name': new_name, 'user_id': user_id})
        assert response.status_code == expected_status

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import customize_group_title
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestCustomizeGroupTitle:
    @patch('app.group_manager.customize_room_title')

    def test_happy_path(self, mock_customize_room_title, client):
        mock_customize_room_title.return_value = {'success': True}
        response = client.post('/customize_group_title', json={
            'custom_title': 'New Group Title',
            'user_id': 1
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    @patch('app.group_manager.customize_room_title')

    def test_missing_custom_title(self, mock_customize_room_title, client):
        mock_customize_room_title.return_value = {'success': False, 'error': 'Missing custom title'}
        response = client.post('/customize_group_title', json={
            'user_id': 1
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is False
        assert data['error'] == 'Missing custom title'

    @pytest.mark.parametrize("custom_title,user_id,expected_success", [
        ('', 1, False),
        ('Valid Title', None, False),
        ('Valid Title', 1, True),
    ])
    @patch('app.group_manager.customize_room_title')

    def test_edge_cases(self, mock_customize_room_title, client, custom_title, user_id, expected_success):
        mock_customize_room_title.return_value = {'success': expected_success}
        response = client.post('/customize_group_title', json={
            'custom_title': custom_title,
            'user_id': user_id
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == expected_success

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import mark_message_delivered
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestMarkMessageDelivered:
    @patch('app.request')
    @patch('app.message_status_manager')

    def test_happy_path(self, mock_message_status_manager, mock_request, client):
        mock_request.json = {'user_id': 1}
        mock_message_status_manager.mark_as_delivered.return_value = {'status': 'delivered'}

        response = client.post('/mark_message_delivered/123')
        assert response.status_code == 200
        assert response.get_json() == {'status': 'delivered'}

    @patch('app.request')
    @patch('app.message_status_manager')

    def test_error_handling(self, mock_message_status_manager, mock_request, client):
        mock_request.json = {'user_id': 1}
        mock_message_status_manager.mark_as_delivered.return_value = None

        response = client.post('/mark_message_delivered/123')
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Failed to update status'}

    @pytest.mark.parametrize("user_id,expected_status,expected_response", [
        (None, 400, {'error': 'Failed to update status'}),
        (2, 200, {'status': 'delivered'}),
    ])
    @patch('app.request')
    @patch('app.message_status_manager')

    def test_edge_cases(self, mock_message_status_manager, mock_request, client, user_id, expected_status, expected_response):
        mock_request.json = {'user_id': user_id}
        mock_message_status_manager.mark_as_delivered.return_value = {'status': 'delivered'} if user_id else None

        response = client.post('/mark_message_delivered/123')
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import mark_message_read
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestMarkMessageRead:
    @patch('app.request')
    @patch('app.message_status_manager')

    def test_mark_message_read_success(self, mock_message_status_manager, mock_request, client):
        mock_request.json = {'user_id': 1}
        mock_message_status_manager.mark_as_read.return_value = {'status': 'read'}

        response = client.post('/mark_message_read/123')
        assert response.status_code == 200
        assert response.get_json() == {'status': 'read'}

    @patch('app.request')
    @patch('app.message_status_manager')

    def test_mark_message_read_failure(self, mock_message_status_manager, mock_request, client):
        mock_request.json = {'user_id': 1}
        mock_message_status_manager.mark_as_read.return_value = None

        response = client.post('/mark_message_read/123')
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Failed to update status'}

    @pytest.mark.parametrize("user_id, expected_status_code, expected_response", [
        (1, 200, {'status': 'read'}),
        (None, 400, {'error': 'Failed to update status'}),
    ])
    @patch('app.request')
    @patch('app.message_status_manager')

    def test_mark_message_read_various_inputs(self, mock_message_status_manager, mock_request, client, user_id, expected_status_code, expected_response):
        mock_request.json = {'user_id': user_id}
        mock_message_status_manager.mark_as_read.return_value = {'status': 'read'} if user_id else None

        response = client.post('/mark_message_read/123')
        assert response.status_code == expected_status_code
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import get_message_status
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetMessageStatus:
    @patch('app.message_status_manager.get_message_status')

    def test_get_message_status_happy_path(self, mock_get_message_status, client):
        mock_get_message_status.return_value = {'status': 'delivered'}
        
        response = client.get('/message_status/1')
        assert response.status_code == 200
        assert response.get_json() == {'status': 'delivered'}

    @patch('app.message_status_manager.get_message_status')

    def test_get_message_status_not_found(self, mock_get_message_status, client):
        mock_get_message_status.return_value = None
        
        response = client.get('/message_status/999')
        assert response.status_code == 404
        assert response.get_json() == {'error': 'Message not found'}

    @pytest.mark.parametrize("message_id,expected_status_code,expected_response", [
        (1, 200, {'status': 'delivered'}),
        (999, 404, {'error': 'Message not found'}),
        (None, 404, {'error': 'Message not found'}),
    ])
    @patch('app.message_status_manager.get_message_status')

    def test_get_message_status_various_cases(self, mock_get_message_status, client, message_id, expected_status_code, expected_response):
        if message_id == 1:
            mock_get_message_status.return_value = {'status': 'delivered'}
        else:
            mock_get_message_status.return_value = None
        
        response = client.get(f'/message_status/{message_id}')
        assert response.status_code == expected_status_code
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import app
from app import get_room_message_statuses

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetRoomMessageStatuses:
    @patch('app.message_status_manager.get_room_message_statuses')

    def test_happy_path(self, mock_get_statuses, client):
        mock_get_statuses.return_value = [{'message_id': 1, 'status': 'read'}]
        response = client.get('/get_room_message_statuses?room_id=1&user_id=123')
        assert response.status_code == 200
        data = response.get_json()
        assert data == [{'message_id': 1, 'status': 'read'}]

    @patch('app.message_status_manager.get_room_message_statuses')

    def test_no_user_id(self, mock_get_statuses, client):
        mock_get_statuses.return_value = [{'message_id': 1, 'status': 'read'}]
        response = client.get('/get_room_message_statuses?room_id=1')
        assert response.status_code == 200
        data = response.get_json()
        assert data == [{'message_id': 1, 'status': 'read'}]

    @patch('app.message_status_manager.get_room_message_statuses')

    def test_empty_statuses(self, mock_get_statuses, client):
        mock_get_statuses.return_value = []
        response = client.get('/get_room_message_statuses?room_id=1&user_id=123')
        assert response.status_code == 200
        data = response.get_json()
        assert data == []

    @patch('app.message_status_manager.get_room_message_statuses')

    def test_invalid_room_id(self, mock_get_statuses, client):
        mock_get_statuses.side_effect = ValueError("Invalid room ID")
        response = client.get('/get_room_message_statuses?room_id=invalid&user_id=123')
        assert response.status_code == 500

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import app
from app import get_user_profile

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetUserProfile:
    @patch('app.profile_manager.get_profile')

    def test_get_user_profile_happy_path(self, mock_get_profile, client):
        mock_get_profile.return_value = {'id': 1, 'name': 'John Doe'}
        
        response = client.get('/user-profile?user_id=1')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1
        assert data['name'] == 'John Doe'

    @patch('app.profile_manager.get_profile')

    def test_get_user_profile_user_not_found(self, mock_get_profile, client):
        mock_get_profile.return_value = None
        
        response = client.get('/user-profile?user_id=999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'User not found'

    @pytest.mark.parametrize("user_id,expected_status,expected_response", [
        (1, 200, {'id': 1, 'name': 'John Doe'}),
        (999, 404, {'error': 'User not found'}),
        (None, 404, {'error': 'User not found'}),
    ])
    @patch('app.profile_manager.get_profile')

    def test_get_user_profile_various_cases(self, mock_get_profile, client, user_id, expected_status, expected_response):
        if user_id == 1:
            mock_get_profile.return_value = {'id': 1, 'name': 'John Doe'}
        else:
            mock_get_profile.return_value = None
        
        response = client.get(f'/user-profile?user_id={user_id}')
        
        assert response.status_code == expected_status
        data = response.get_json()
        assert data == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import upload_profile_picture
from flask import app  # ✅ CRITICAL: Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestUploadProfilePicture:
    @patch('app.profile_manager.upload_profile_picture')

    def test_happy_path(self, mock_upload, client):
        mock_upload.return_value = {'success': True}
        response = client.post('/upload_profile_picture', json={
            'user_id': 1,
            'image_data': 'fake_image_data',
            'filename': 'profile.jpg'
        })
        assert response.status_code == 200
        assert response.get_json() == {'success': True}

    @patch('app.profile_manager.upload_profile_picture')

    def test_upload_failure(self, mock_upload, client):
        mock_upload.return_value = None
        response = client.post('/upload_profile_picture', json={
            'user_id': 1,
            'image_data': 'fake_image_data',
            'filename': 'profile.jpg'
        })
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Upload failed'}

    @pytest.mark.parametrize("image_data, filename, expected_status", [
        ('fake_image_data', 'profile.jpg', 200),
        (None, 'profile.jpg', 400),
        ('fake_image_data', None, 200),
    ])
    @patch('app.profile_manager.upload_profile_picture')

    def test_edge_cases(self, mock_upload, client, image_data, filename, expected_status):
        mock_upload.return_value = {'success': True} if image_data else None
        response = client.post('/upload_profile_picture', json={
            'user_id': 1,
            'image_data': image_data,
            'filename': filename
        })
        assert response.status_code == expected_status

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import update_display_name
from flask import app  # ✅ CRITICAL: Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestUpdateDisplayName:
    @patch('app.request')
    @patch('app.profile_manager')

    def test_happy_path(self, mock_profile_manager, mock_request, client):
        mock_request.json = {'display_name': 'New Name'}
        mock_profile_manager.update_display_name.return_value = {'success': True}

        response = client.post('/update_display_name/1', json={'display_name': 'New Name'})
        assert response.status_code == 200
        assert response.get_json() == {'success': True}

    @patch('app.request')
    @patch('app.profile_manager')

    def test_update_failed(self, mock_profile_manager, mock_request, client):
        mock_request.json = {'display_name': 'New Name'}
        mock_profile_manager.update_display_name.return_value = None

        response = client.post('/update_display_name/1', json={'display_name': 'New Name'})
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Update failed'}

    @pytest.mark.parametrize("display_name, expected_status, expected_response", [
        ('', 400, {'error': 'Update failed'}),
        (None, 400, {'error': 'Update failed'}),
        ('Valid Name', 200, {'success': True}),
    ])
    @patch('app.request')
    @patch('app.profile_manager')

    def test_edge_cases(self, mock_profile_manager, mock_request, client, display_name, expected_status, expected_response):
        mock_request.json = {'display_name': display_name}
        mock_profile_manager.update_display_name.return_value = expected_response if expected_status == 200 else None

        response = client.post('/update_display_name/1', json={'display_name': display_name})
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import update_status_message
from flask import app  # Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestUpdateStatusMessage:
    @patch('app.profile_manager.update_status_message')

    def test_happy_path(self, mock_update_status_message, client):
        mock_update_status_message.return_value = {'success': True}
        response = client.post('/update_status_message/1', json={'status_message': 'New status'})
        assert response.status_code == 200
        assert response.get_json() == {'success': True}

    @patch('app.profile_manager.update_status_message')

    def test_update_failure(self, mock_update_status_message, client):
        mock_update_status_message.return_value = None
        response = client.post('/update_status_message/1', json={'status_message': 'New status'})
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Update failed'}

    @pytest.mark.parametrize("user_id,status_message,expected_status,expected_response", [
        (1, 'Hello World', 200, {'success': True}),
        (1, '', 400, {'error': 'Update failed'}),
        (1, None, 400, {'error': 'Update failed'}),
    ])
    @patch('app.profile_manager.update_status_message')

    def test_edge_cases(self, mock_update_status_message, client, user_id, status_message, expected_status, expected_response):
        mock_update_status_message.return_value = expected_response if expected_status == 200 else None
        response = client.post(f'/update_status_message/{user_id}', json={'status_message': status_message})
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import update_bio
from flask import app  # ✅ CRITICAL: Import Flask app for client fixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestUpdateBio:
    @patch('app.profile_manager.update_bio')

    def test_happy_path(self, mock_update_bio, client):
        mock_update_bio.return_value = {'success': True}
        response = client.post('/update_bio', json={'bio': 'New bio'})
        assert response.status_code == 200
        assert response.get_json() == {'success': True}

    @patch('app.profile_manager.update_bio')

    def test_update_failed(self, mock_update_bio, client):
        mock_update_bio.return_value = None
        response = client.post('/update_bio', json={'bio': 'New bio'})
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Update failed'}

    @pytest.mark.parametrize("bio_input, expected_status, expected_response", [
        ('', 400, {'error': 'Update failed'}),
        (None, 400, {'error': 'Update failed'}),
        ('A' * 1001, 400, {'error': 'Update failed'})  # Assuming bio length limit
    ])
    @patch('app.profile_manager.update_bio')

    def test_edge_cases(self, mock_update_bio, client, bio_input, expected_status, expected_response):
        mock_update_bio.return_value = None
        response = client.post('/update_bio', json={'bio': bio_input})
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source

