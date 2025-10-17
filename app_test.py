"""
Auto-generated tests using LLM and RAG
"""

from unittest.mock import MagicMock, patch, Mock
import pytest


@pytest.fixture
def client():
    """Flask test client with app context."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


import pytest
from unittest.mock import patch, Mock
from app import login
from app import app

class TestLogin:
    @patch('app.User')

    def test_login_success(self, mock_user, client):
        # Setup mock user
        mock_user.query.filter_by.return_value.first.return_value = Mock(
            id=1,
            username='testuser',
            check_password=Mock(return_value=True),
            create_session=Mock(return_value='session_token')
        )

        # Make request
        response = client.post('/api/users/login', json={'username': 'testuser', 'password': 'correctpassword'})

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['token'] == 'session_token'
        assert data['user_id'] == 1

    @patch('app.User')

    def test_login_invalid_credentials(self, mock_user, client):
        # Setup mock user
        mock_user.query.filter_by.return_value.first.return_value = Mock(
            id=1,
            username='testuser',
            check_password=Mock(return_value=False)
        )

        # Make request
        response = client.post('/api/users/login', json={'username': 'testuser', 'password': 'wrongpassword'})

        # Assert
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'Invalid credentials'

    @patch('app.User')

    def test_login_user_not_found(self, mock_user, client):
        # Setup mock user
        mock_user.query.filter_by.return_value.first.return_value = None

        # Make request
        response = client.post('/api/users/login', json={'username': 'nonexistent', 'password': 'password'})

        # Assert
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'Invalid credentials'

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from app import get_messages
from app import app

class TestGetMessages:
    @patch('app.Message')

    def test_get_messages_happy_path(self, mock_message, client):
        # Setup mock responses
        mock_message.query.filter_by.return_value.order_by.return_value.all.return_value = [
            Mock(id=1, user_id=1, content='Hello', created_at=Mock(isoformat=lambda: '2023-10-01T12:00:00')),
            Mock(id=2, user_id=2, content='Hi', created_at=Mock(isoformat=lambda: '2023-10-01T12:01:00'))
        ]

        # Make request
        response = client.get('/api/messages?room_id=1')

        # Assert
        assert response.status_code == 200
        assert response.get_json() == [
            {'id': 1, 'user_id': 1, 'content': 'Hello', 'created_at': '2023-10-01T12:00:00'},
            {'id': 2, 'user_id': 2, 'content': 'Hi', 'created_at': '2023-10-01T12:01:00'}
        ]

    @patch('app.Message')

    def test_get_messages_no_messages(self, mock_message, client):
        # Setup mock responses
        mock_message.query.filter_by.return_value.order_by.return_value.all.return_value = []

        # Make request
        response = client.get('/api/messages?room_id=1')

        # Assert
        assert response.status_code == 200
        assert response.get_json() == []

    @patch('app.Message')

    def test_get_messages_invalid_room_id(self, mock_message, client):
        # Setup mock responses
        mock_message.query.filter_by.return_value.order_by.return_value.all.return_value = []

        # Make request
        response = client.get('/api/messages?room_id=invalid')

        # Assert
        assert response.status_code == 200
        assert response.get_json() == []

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import update_status

class TestUpdateStatus:
    @patch('app.status_manager')

    def test_update_status_success(self, mock_status_manager, client):
        response = client.post('/api/status/update', json={'user_id': 1, 'is_online': True})
        assert response.status_code == 200
        assert response.get_json() == {'success': True}
        mock_status_manager.update_user_status.assert_called_once_with(1, True)

    @patch('app.status_manager')

    def test_update_status_missing_user_id(self, mock_status_manager, client):
        response = client.post('/api/status/update', json={'is_online': True})
        assert response.status_code == 400
        mock_status_manager.update_user_status.assert_not_called()

    @patch('app.status_manager')

    def test_update_status_missing_is_online(self, mock_status_manager, client):
        response = client.post('/api/status/update', json={'user_id': 1})
        assert response.status_code == 400
        mock_status_manager.update_user_status.assert_not_called()

    @pytest.mark.parametrize("user_id, is_online", [
        (None, True),
        (1, None),
        (None, None),
    ])
    @patch('app.status_manager')

    def test_update_status_invalid_inputs(self, mock_status_manager, client, user_id, is_online):
        response = client.post('/api/status/update', json={'user_id': user_id, 'is_online': is_online})
        assert response.status_code == 400
        mock_status_manager.update_user_status.assert_not_called()

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import get_status

class TestGetStatus:
    @patch('app.status_manager')

    def test_get_status_happy_path(self, mock_status_manager, client):
        mock_status_manager.get_user_status.return_value = {'status': 'online'}
        
        response = client.get('/api/status/1')
        
        assert response.status_code == 200
        assert response.get_json() == {'status': 'online'}

    @patch('app.status_manager')

    def test_get_status_user_not_found(self, mock_status_manager, client):
        mock_status_manager.get_user_status.return_value = None
        
        response = client.get('/api/status/999')
        
        assert response.status_code == 404

    @pytest.mark.parametrize("user_id, expected_status", [
        (1, {'status': 'online'}),
        (2, {'status': 'offline'}),
        (3, {'status': 'busy'}),
    ])
    @patch('app.status_manager')

    def test_get_status_various_users(self, mock_status_manager, client, user_id, expected_status):
        mock_status_manager.get_user_status.return_value = expected_status
        
        response = client.get(f'/api/status/{user_id}')
        
        assert response.status_code == 200
        assert response.get_json() == expected_status

# Third-party
# Local


import pytest
from unittest.mock import patch, Mock
from app import start_typing
from flask import Flask  # app removed - use "from app import app"

class TestStartTyping:
    @patch('app.typing_indicator')

    def test_start_typing_success(self, mock_typing_indicator, client):
        response = client.post('/api/typing/start', json={
            'room_id': '123',
            'user_id': '456',
            'username': 'testuser'
        })
        assert response.status_code == 200
        assert response.get_json() == {'success': True}
        mock_typing_indicator.user_started_typing.assert_called_once_with('123', '456', 'testuser')

    @pytest.mark.parametrize("json_data", [
        {'room_id': '123', 'user_id': '456'},  # Missing username
        {'room_id': '123', 'username': 'testuser'},  # Missing user_id
        {'user_id': '456', 'username': 'testuser'},  # Missing room_id
        {}  # Missing all
    ])

    def test_start_typing_missing_data(self, client, json_data):
        response = client.post('/api/typing/start', json=json_data)
        assert response.status_code == 400  # Assuming the function should return 400 for bad requests

    @patch('app.typing_indicator')

    def test_start_typing_typing_indicator_error(self, mock_typing_indicator, client):
        mock_typing_indicator.user_started_typing.side_effect = Exception("Indicator error")
        response = client.post('/api/typing/start', json={
            'room_id': '123',
            'user_id': '456',
            'username': 'testuser'
        })
        assert response.status_code == 500  # Assuming the function should return 500 for internal errors

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import stop_typing

class TestStopTyping:
    @patch('app.typing_indicator')

    def test_stop_typing_success(self, mock_typing_indicator, client):
        # Mock the typing_indicator method
        mock_typing_indicator.user_stopped_typing.return_value = None

        # Make request
        response = client.post('/api/typing/stop', json={'room_id': '123', 'user_id': '456'})

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        mock_typing_indicator.user_stopped_typing.assert_called_once_with('123', '456')

    @pytest.mark.parametrize("payload, expected_status", [
        ({'room_id': '123'}, 400),  # Missing user_id
        ({'user_id': '456'}, 400),  # Missing room_id
        ({}, 400),  # Missing both
    ])

    def test_stop_typing_missing_parameters(self, client, payload, expected_status):
        response = client.post('/api/typing/stop', json=payload)
        assert response.status_code == expected_status

    @patch('app.typing_indicator')

    def test_stop_typing_typing_indicator_error(self, mock_typing_indicator, client):
        # Simulate an error in the typing_indicator method
        mock_typing_indicator.user_stopped_typing.side_effect = Exception("Error")

        # Make request
        response = client.post('/api/typing/stop', json={'room_id': '123', 'user_id': '456'})

        # Assert
        assert response.status_code == 500

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from app import get_typing_users
from flask import Flask  # app removed - use "from app import app"

class TestGetTypingUsers:
    @patch('app.typing_indicator.get_typing_users')

    def test_get_typing_users_happy_path(self, mock_get_typing_users, client):
        mock_get_typing_users.return_value = ['user1', 'user2']
        
        response = client.get('/api/typing/1')
        
        assert response.status_code == 200
        assert response.get_json() == ['user1', 'user2']
        mock_get_typing_users.assert_called_once_with(1)

    @patch('app.typing_indicator.get_typing_users')

    def test_get_typing_users_no_typers(self, mock_get_typing_users, client):
        mock_get_typing_users.return_value = []
        
        response = client.get('/api/typing/1')
        
        assert response.status_code == 200
        assert response.get_json() == []
        mock_get_typing_users.assert_called_once_with(1)

    @patch('app.typing_indicator.get_typing_users')

    def test_get_typing_users_invalid_room_id(self, mock_get_typing_users, client):
        mock_get_typing_users.side_effect = ValueError("Invalid room ID")
        
        response = client.get('/api/typing/invalid')
        
        assert response.status_code == 404

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import create_group

class TestCreateGroup:
    @patch('app.group_manager.create_group')

    def test_create_group_happy_path(self, mock_create_group, client):
        mock_create_group.return_value = {'id': 1, 'name': 'Test Group', 'creator_id': 1, 'member_ids': [2, 3]}
        
        response = client.post('/api/groups/create', json={
            'name': 'Test Group',
            'creator_id': 1,
            'member_ids': [2, 3]
        })
        
        assert response.status_code == 200
        assert response.get_json() == {'id': 1, 'name': 'Test Group', 'creator_id': 1, 'member_ids': [2, 3]}
        mock_create_group.assert_called_once_with('Test Group', 1, [2, 3])

    @patch('app.group_manager.create_group')

    def test_create_group_missing_name(self, mock_create_group, client):
        response = client.post('/api/groups/create', json={
            'creator_id': 1,
            'member_ids': [2, 3]
        })
        
        assert response.status_code == 400
        mock_create_group.assert_not_called()

    @patch('app.group_manager.create_group')

    def test_create_group_empty_member_ids(self, mock_create_group, client):
        mock_create_group.return_value = {'id': 2, 'name': 'Another Group', 'creator_id': 1, 'member_ids': []}
        
        response = client.post('/api/groups/create', json={
            'name': 'Another Group',
            'creator_id': 1
        })
        
        assert response.status_code == 200
        assert response.get_json() == {'id': 2, 'name': 'Another Group', 'creator_id': 1, 'member_ids': []}
        mock_create_group.assert_called_once_with('Another Group', 1, [])

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import rename_group

class TestRenameGroup:
    @patch('app.group_manager.update_group_name')

    def test_rename_group_success(self, mock_update_group_name, client):
        mock_update_group_name.return_value = {'success': True}

        response = client.post('/api/groups/1/rename', json={'new_name': 'New Group Name', 'user_id': 1})
        
        assert response.status_code == 200
        assert response.get_json() == {'success': True}
        mock_update_group_name.assert_called_once_with(1, 'New Group Name', 1)

    @patch('app.group_manager.update_group_name')

    def test_rename_group_missing_new_name(self, mock_update_group_name, client):
        response = client.post('/api/groups/1/rename', json={'user_id': 1})
        
        assert response.status_code == 400
        mock_update_group_name.assert_not_called()

    @patch('app.group_manager.update_group_name')

    def test_rename_group_missing_user_id(self, mock_update_group_name, client):
        response = client.post('/api/groups/1/rename', json={'new_name': 'New Group Name'})
        
        assert response.status_code == 400
        mock_update_group_name.assert_not_called()

    @pytest.mark.parametrize("group_id,new_name,user_id,expected_status", [
        (1, 'New Group Name', 1, 200),
        (1, '', 1, 400),
        (1, 'New Group Name', None, 400),
    ])
    @patch('app.group_manager.update_group_name')

    def test_rename_group_various_inputs(self, mock_update_group_name, client, group_id, new_name, user_id, expected_status):
        mock_update_group_name.return_value = {'success': True}

        response = client.post(f'/api/groups/{group_id}/rename', json={'new_name': new_name, 'user_id': user_id})
        
        assert response.status_code == expected_status
        if expected_status == 200:
            mock_update_group_name.assert_called_once_with(group_id, new_name, user_id)
        else:
            mock_update_group_name.assert_not_called()

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import customize_group_title

class TestCustomizeGroupTitle:
    @patch('app.group_manager.customize_room_title')

    def test_customize_group_title_success(self, mock_customize_room_title, client):
        mock_customize_room_title.return_value = {'success': True}
        response = client.post('/api/groups/1/customize', json={'custom_title': 'New Title', 'user_id': 1})
        assert response.status_code == 200
        assert response.get_json() == {'success': True}

    @patch('app.group_manager.customize_room_title')

    def test_customize_group_title_missing_custom_title(self, mock_customize_room_title, client):
        response = client.post('/api/groups/1/customize', json={'user_id': 1})
        assert response.status_code == 400  # Assuming the function should return 400 for missing data
        mock_customize_room_title.assert_not_called()

    @patch('app.group_manager.customize_room_title')

    def test_customize_group_title_invalid_user_id(self, mock_customize_room_title, client):
        response = client.post('/api/groups/1/customize', json={'custom_title': 'New Title', 'user_id': None})
        assert response.status_code == 400  # Assuming the function should return 400 for invalid user_id
        mock_customize_room_title.assert_not_called()

    @pytest.mark.parametrize("group_id, custom_title, user_id, expected_status", [
        (1, 'New Title', 1, 200),
        (1, '', 1, 400),  # Assuming empty title is invalid
        (1, 'New Title', None, 400),  # Invalid user_id
    ])
    @patch('app.group_manager.customize_room_title')

    def test_customize_group_title_various_inputs(self, mock_customize_room_title, client, group_id, custom_title, user_id, expected_status):
        mock_customize_room_title.return_value = {'success': True}
        response = client.post(f'/api/groups/{group_id}/customize', json={'custom_title': custom_title, 'user_id': user_id})
        assert response.status_code == expected_status
        if expected_status == 200:
            assert response.get_json() == {'success': True}
        else:
            mock_customize_room_title.assert_not_called()

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import mark_message_delivered

class TestMarkMessageDelivered:
    @patch('app.message_status_manager')

    def test_mark_message_delivered_success(self, mock_message_status_manager, client):
        mock_message_status_manager.mark_as_delivered.return_value = {'status': 'delivered'}
        
        response = client.post('/api/messages/1/delivered', json={'user_id': 1})
        
        assert response.status_code == 200
        assert response.get_json() == {'status': 'delivered'}

    @patch('app.message_status_manager')

    def test_mark_message_delivered_failure(self, mock_message_status_manager, client):
        mock_message_status_manager.mark_as_delivered.return_value = None
        
        response = client.post('/api/messages/1/delivered', json={'user_id': 1})
        
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Failed to update status'}

    @pytest.mark.parametrize("user_id", [None, '', 0])
    @patch('app.message_status_manager')

    def test_mark_message_delivered_invalid_user_id(self, mock_message_status_manager, client, user_id):
        mock_message_status_manager.mark_as_delivered.return_value = None
        
        response = client.post('/api/messages/1/delivered', json={'user_id': user_id})
        
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Failed to update status'}

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from app import mark_message_read
from app import app

class TestMarkMessageRead:
    @patch('app.message_status_manager')

    def test_mark_message_read_success(self, mock_message_status_manager, client):
        # Setup mock
        mock_message_status_manager.mark_as_read.return_value = {'status': 'read'}

        # Make request
        response = client.post('/api/messages/1/read', json={'user_id': 1})

        # Assert
        assert response.status_code == 200
        assert response.get_json() == {'status': 'read'}

    @patch('app.message_status_manager')

    def test_mark_message_read_failure(self, mock_message_status_manager, client):
        # Setup mock
        mock_message_status_manager.mark_as_read.return_value = None

        # Make request
        response = client.post('/api/messages/1/read', json={'user_id': 1})

        # Assert
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Failed to update status'}

    @pytest.mark.parametrize("user_id, expected_status_code, expected_response", [
        (1, 200, {'status': 'read'}),
        (None, 400, {'error': 'Failed to update status'}),
    ])
    @patch('app.message_status_manager')

    def test_mark_message_read_various_inputs(self, mock_message_status_manager, client, user_id, expected_status_code, expected_response):
        # Setup mock
        if user_id is not None:
            mock_message_status_manager.mark_as_read.return_value = {'status': 'read'}
        else:
            mock_message_status_manager.mark_as_read.return_value = None

        # Make request
        response = client.post('/api/messages/1/read', json={'user_id': user_id})

        # Assert
        assert response.status_code == expected_status_code
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import get_message_status

class TestGetMessageStatus:
    @patch('app.message_status_manager.get_message_status')

    def test_get_message_status_found(self, mock_get_message_status, client):
        # Setup mock response
        mock_get_message_status.return_value = {'status': 'delivered'}

        # Make request
        response = client.get('/api/messages/1/status')

        # Assert
        assert response.status_code == 200
        assert response.get_json() == {'status': 'delivered'}

    @patch('app.message_status_manager.get_message_status')

    def test_get_message_status_not_found(self, mock_get_message_status, client):
        # Setup mock response
        mock_get_message_status.return_value = None

        # Make request
        response = client.get('/api/messages/999/status')

        # Assert
        assert response.status_code == 404
        assert response.get_json() == {'error': 'Message not found'}

    @pytest.mark.parametrize("message_id, mock_return_value, expected_status, expected_response", [
        (1, {'status': 'read'}, 200, {'status': 'read'}),
        (2, None, 404, {'error': 'Message not found'}),
    ])
    @patch('app.message_status_manager.get_message_status')

    def test_get_message_status_various_cases(self, mock_get_message_status, client, message_id, mock_return_value, expected_status, expected_response):
        # Setup mock response
        mock_get_message_status.return_value = mock_return_value

        # Make request
        response = client.get(f'/api/messages/{message_id}/status')

        # Assert
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from app import get_room_message_statuses
from app import app

class TestGetRoomMessageStatuses:
    @patch('app.message_status_manager.get_room_message_statuses')

    def test_get_room_message_statuses_happy_path(self, mock_get_statuses, client):
        mock_get_statuses.return_value = [{'message_id': 1, 'status': 'read'}]
        
        response = client.get('/api/rooms/1/message-statuses?user_id=1')
        
        assert response.status_code == 200
        assert response.get_json() == [{'message_id': 1, 'status': 'read'}]
        mock_get_statuses.assert_called_once_with(1, 1)

    @patch('app.message_status_manager.get_room_message_statuses')

    def test_get_room_message_statuses_no_user_id(self, mock_get_statuses, client):
        mock_get_statuses.return_value = [{'message_id': 1, 'status': 'read'}]
        
        response = client.get('/api/rooms/1/message-statuses')
        
        assert response.status_code == 200
        assert response.get_json() == [{'message_id': 1, 'status': 'read'}]
        mock_get_statuses.assert_called_once_with(1, None)

    @patch('app.message_status_manager.get_room_message_statuses')

    def test_get_room_message_statuses_empty_response(self, mock_get_statuses, client):
        mock_get_statuses.return_value = []
        
        response = client.get('/api/rooms/1/message-statuses?user_id=1')
        
        assert response.status_code == 200
        assert response.get_json() == []
        mock_get_statuses.assert_called_once_with(1, 1)

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from app import get_user_profile
from app import app

class TestGetUserProfile:
    @patch('app.profile_manager.get_profile')

    def test_get_user_profile_success(self, mock_get_profile, client):
        # Setup mock response
        mock_get_profile.return_value = {'id': 1, 'name': 'John Doe'}

        # Make request
        response = client.get('/api/profile/1')

        # Assert
        assert response.status_code == 200
        assert response.get_json() == {'id': 1, 'name': 'John Doe'}

    @patch('app.profile_manager.get_profile')

    def test_get_user_profile_not_found(self, mock_get_profile, client):
        # Setup mock response
        mock_get_profile.return_value = None

        # Make request
        response = client.get('/api/profile/999')

        # Assert
        assert response.status_code == 404
        assert response.get_json() == {'error': 'User not found'}

    @pytest.mark.parametrize("user_id, expected_status, expected_response", [
        (1, 200, {'id': 1, 'name': 'John Doe'}),
        (999, 404, {'error': 'User not found'}),
    ])
    @patch('app.profile_manager.get_profile')

    def test_get_user_profile_various_cases(self, mock_get_profile, client, user_id, expected_status, expected_response):
        # Setup mock response
        if user_id == 1:
            mock_get_profile.return_value = {'id': 1, 'name': 'John Doe'}
        else:
            mock_get_profile.return_value = None

        # Make request
        response = client.get(f'/api/profile/{user_id}')

        # Assert
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import upload_profile_picture

class TestUploadProfilePicture:
    @patch('app.profile_manager.upload_profile_picture')

    def test_happy_path(self, mock_upload, client):
        mock_upload.return_value = {'success': True}
        response = client.post('/api/profile/1/picture', json={'image_data': 'fake_image_data', 'filename': 'profile.jpg'})
        assert response.status_code == 200
        assert response.get_json() == {'success': True}

    @patch('app.profile_manager.upload_profile_picture')

    def test_upload_failure(self, mock_upload, client):
        mock_upload.return_value = None
        response = client.post('/api/profile/1/picture', json={'image_data': 'fake_image_data', 'filename': 'profile.jpg'})
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Upload failed'}

    @pytest.mark.parametrize("image_data, filename, expected_status", [
        ('valid_image_data', 'profile.jpg', 200),
        (None, 'profile.jpg', 400),
        ('valid_image_data', None, 200),
    ])
    @patch('app.profile_manager.upload_profile_picture')

    def test_edge_cases(self, mock_upload, client, image_data, filename, expected_status):
        mock_upload.return_value = {'success': True} if image_data else None
        response = client.post('/api/profile/1/picture', json={'image_data': image_data, 'filename': filename})
        assert response.status_code == expected_status

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import update_display_name

class TestUpdateDisplayName:
    @patch('app.profile_manager.update_display_name')

    def test_update_display_name_success(self, mock_update_display_name, client):
        mock_update_display_name.return_value = {'display_name': 'New Name'}
        
        response = client.put('/api/profile/1/display-name', json={'display_name': 'New Name'})
        
        assert response.status_code == 200
        assert response.get_json() == {'display_name': 'New Name'}

    @patch('app.profile_manager.update_display_name')

    def test_update_display_name_failure(self, mock_update_display_name, client):
        mock_update_display_name.return_value = None
        
        response = client.put('/api/profile/1/display-name', json={'display_name': 'New Name'})
        
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Update failed'}

    @pytest.mark.parametrize("user_id, display_name, expected_status, expected_response", [
        (1, 'Valid Name', 200, {'display_name': 'Valid Name'}),
        (1, '', 400, {'error': 'Update failed'}),
        (1, None, 400, {'error': 'Update failed'}),
    ])
    @patch('app.profile_manager.update_display_name')

    def test_update_display_name_various_inputs(self, mock_update_display_name, client, user_id, display_name, expected_status, expected_response):
        if display_name:
            mock_update_display_name.return_value = {'display_name': display_name}
        else:
            mock_update_display_name.return_value = None
        
        response = client.put(f'/api/profile/{user_id}/display-name', json={'display_name': display_name})
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

# Third-party
# Local


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import update_status_message

class TestUpdateStatusMessage:
    @patch('app.profile_manager.update_status_message')

    def test_update_status_message_success(self, mock_update_status_message, client):
        mock_update_status_message.return_value = {'status': 'success'}
        response = client.put('/api/profile/1/status', json={'status_message': 'New status'})
        assert response.status_code == 200
        assert response.get_json() == {'status': 'success'}

    @patch('app.profile_manager.update_status_message')

    def test_update_status_message_failure(self, mock_update_status_message, client):
        mock_update_status_message.return_value = None
        response = client.put('/api/profile/1/status', json={'status_message': 'New status'})
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Update failed'}

    @pytest.mark.parametrize("user_id, status_message, expected_status", [
        (1, 'Hello World', 200),
        (2, '', 400),
        (3, None, 400),
    ])
    @patch('app.profile_manager.update_status_message')

    def test_update_status_message_various_inputs(self, mock_update_status_message, client, user_id, status_message, expected_status):
        mock_update_status_message.return_value = {'status': 'success'} if status_message else None
        response = client.put(f'/api/profile/{user_id}/status', json={'status_message': status_message})
        assert response.status_code == expected_status

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import update_bio

class TestUpdateBio:
    @patch('app.profile_manager')

    def test_update_bio_success(self, mock_profile_manager, client):
        mock_profile_manager.update_bio.return_value = {'success': True}
        
        response = client.put('/api/profile/1/bio', json={'bio': 'New bio'})
        
        assert response.status_code == 200
        assert response.get_json() == {'success': True}

    @patch('app.profile_manager')

    def test_update_bio_failure(self, mock_profile_manager, client):
        mock_profile_manager.update_bio.return_value = None
        
        response = client.put('/api/profile/1/bio', json={'bio': 'New bio'})
        
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Update failed'}

    @pytest.mark.parametrize("user_id, bio, expected_status, expected_response", [
        (1, 'Bio with special characters!@#$', 200, {'success': True}),
        (2, '', 400, {'error': 'Update failed'}),
        (3, None, 400, {'error': 'Update failed'}),
    ])
    @patch('app.profile_manager')

    def test_update_bio_various_inputs(self, mock_profile_manager, client, user_id, bio, expected_status, expected_response):
        mock_profile_manager.update_bio.return_value = expected_response if expected_status == 200 else None
        
        response = client.put(f'/api/profile/{user_id}/bio', json={'bio': bio})
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source

