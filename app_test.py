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

        # Make request with invalid room_id
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

    @pytest.mark.parametrize("user_id, is_online", [
        (None, True),
        (1, None),
        (None, None),
    ])
    @patch('app.status_manager')

    def test_update_status_missing_data(self, mock_status_manager, client, user_id, is_online):
        response = client.post('/api/status/update', json={'user_id': user_id, 'is_online': is_online})
        assert response.status_code == 200
        assert response.get_json() == {'success': True}
        mock_status_manager.update_user_status.assert_called_once_with(user_id, is_online)

    @patch('app.status_manager')

    def test_update_status_invalid_method(self, mock_status_manager, client):
        response = client.get('/api/status/update')
        assert response.status_code == 405  # Method Not Allowed
        mock_status_manager.update_user_status.assert_not_called()


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import get_status

class TestGetStatus:
    @patch('app.status_manager')

    def test_get_status_happy_path(self, mock_status_manager, client):
        mock_status_manager.get_user_status.return_value = {'status': 'active'}
        
        response = client.get('/api/status/1')
        
        assert response.status_code == 200
        assert response.get_json() == {'status': 'active'}

    @patch('app.status_manager')

    def test_get_status_user_not_found(self, mock_status_manager, client):
        mock_status_manager.get_user_status.return_value = None
        
        response = client.get('/api/status/999')
        
        assert response.status_code == 404

    @pytest.mark.parametrize("user_id, expected_status", [
        (1, {'status': 'active'}),
        (2, {'status': 'inactive'}),
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
from flask import Flask  # app removed - use "from app import app"
from app import start_typing

class TestStartTyping:
    @patch('app.typing_indicator')

    def test_start_typing_success(self, mock_typing_indicator, client):
        response = client.post('/api/typing/start', json={
            'room_id': '123',
            'user_id': '456',
            'username': 'testuser'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        mock_typing_indicator.user_started_typing.assert_called_once_with('123', '456', 'testuser')

    @pytest.mark.parametrize("json_data, expected_status", [
        ({'room_id': '123', 'user_id': '456'}, 400),
        ({'room_id': '123', 'username': 'testuser'}, 400),
        ({'user_id': '456', 'username': 'testuser'}, 400),
        ({}, 400),
    ])

    def test_start_typing_missing_fields(self, client, json_data, expected_status):
        response = client.post('/api/typing/start', json=json_data)
        assert response.status_code == expected_status

    @patch('app.typing_indicator')

    def test_start_typing_typing_indicator_error(self, mock_typing_indicator, client):
        mock_typing_indicator.user_started_typing.side_effect = Exception("Error")
        response = client.post('/api/typing/start', json={
            'room_id': '123',
            'user_id': '456',
            'username': 'testuser'
        })
        assert response.status_code == 500

# Third-party
# Local


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import stop_typing

class TestStopTyping:
    @patch('app.typing_indicator')

    def test_stop_typing_success(self, mock_typing_indicator, client):
        # Mock the typing_indicator method
        mock_typing_indicator.user_stopped_typing.return_value = None

        # Make the POST request
        response = client.post('/api/typing/stop', json={'room_id': '123', 'user_id': '456'})

        # Assert the response
        assert response.status_code == 200
        assert response.get_json() == {'success': True}
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

        # Make the POST request
        response = client.post('/api/typing/stop', json={'room_id': '123', 'user_id': '456'})

        # Assert the response
        assert response.status_code == 500

# Third-party
# Local


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

    def test_get_typing_users_no_users_typing(self, mock_get_typing_users, client):
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
        mock_get_typing_users.assert_not_called()

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import create_group

class TestCreateGroup:
    @patch('app.group_manager')

    def test_create_group_happy_path(self, mock_group_manager, client):
        mock_group_manager.create_group.return_value = {'id': 1, 'name': 'Test Group'}

        response = client.post('/api/groups/create', json={
            'name': 'Test Group',
            'creator_id': 1,
            'member_ids': [2, 3]
        })

        assert response.status_code == 200
        assert response.get_json() == {'id': 1, 'name': 'Test Group'}
        mock_group_manager.create_group.assert_called_once_with('Test Group', 1, [2, 3])

    @patch('app.group_manager')

    def test_create_group_missing_name(self, mock_group_manager, client):
        response = client.post('/api/groups/create', json={
            'creator_id': 1,
            'member_ids': [2, 3]
        })

        assert response.status_code == 400
        mock_group_manager.create_group.assert_not_called()

    @patch('app.group_manager')

    def test_create_group_empty_member_ids(self, mock_group_manager, client):
        mock_group_manager.create_group.return_value = {'id': 2, 'name': 'Empty Members Group'}

        response = client.post('/api/groups/create', json={
            'name': 'Empty Members Group',
            'creator_id': 1,
            'member_ids': []
        })

        assert response.status_code == 200
        assert response.get_json() == {'id': 2, 'name': 'Empty Members Group'}
        mock_group_manager.create_group.assert_called_once_with('Empty Members Group', 1, [])

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

    @patch('app.group_manager.update_group_name')

    def test_rename_group_missing_new_name(self, mock_update_group_name, client):
        response = client.post('/api/groups/1/rename', json={'user_id': 1})
        assert response.status_code == 400

    @patch('app.group_manager.update_group_name')

    def test_rename_group_missing_user_id(self, mock_update_group_name, client):
        response = client.post('/api/groups/1/rename', json={'new_name': 'New Group Name'})
        assert response.status_code == 400

    @patch('app.group_manager.update_group_name')

    def test_rename_group_update_failure(self, mock_update_group_name, client):
        mock_update_group_name.return_value = {'success': False, 'error': 'Update failed'}
        response = client.post('/api/groups/1/rename', json={'new_name': 'New Group Name', 'user_id': 1})
        assert response.status_code == 200
        assert response.get_json() == {'success': False, 'error': 'Update failed'}

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
        assert response.status_code == 400  # Assuming the function returns 400 for missing data

    @patch('app.group_manager.customize_room_title')

    def test_customize_group_title_missing_user_id(self, mock_customize_room_title, client):
        response = client.post('/api/groups/1/customize', json={'custom_title': 'New Title'})
        assert response.status_code == 400  # Assuming the function returns 400 for missing data

    @patch('app.group_manager.customize_room_title')

    def test_customize_group_title_invalid_group_id(self, mock_customize_room_title, client):
        mock_customize_room_title.side_effect = Exception("Invalid group ID")
        response = client.post('/api/groups/999/customize', json={'custom_title': 'New Title', 'user_id': 1})
        assert response.status_code == 500  # Assuming the function returns 500 for server errors

# Third-party
# Local


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

    @pytest.mark.parametrize("user_id, expected_status_code, expected_response", [
        (1, 200, {'status': 'delivered'}),
        (None, 400, {'error': 'Failed to update status'}),
    ])
    @patch('app.message_status_manager')

    def test_mark_message_delivered_various_inputs(self, mock_message_status_manager, client, user_id, expected_status_code, expected_response):
        mock_message_status_manager.mark_as_delivered.return_value = {'status': 'delivered'} if user_id else None
        
        response = client.post('/api/messages/1/delivered', json={'user_id': user_id})
        
        assert response.status_code == expected_status_code
        assert response.get_json() == expected_response

# Third-party
# Local


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import mark_message_read

class TestMarkMessageRead:
    @patch('app.message_status_manager')

    def test_mark_message_read_success(self, mock_message_status_manager, client):
        mock_message_status_manager.mark_as_read.return_value = {'status': 'read'}

        response = client.post('/api/messages/1/read', json={'user_id': 1})
        assert response.status_code == 200
        assert response.get_json() == {'status': 'read'}

    @patch('app.message_status_manager')

    def test_mark_message_read_failure(self, mock_message_status_manager, client):
        mock_message_status_manager.mark_as_read.return_value = None

        response = client.post('/api/messages/1/read', json={'user_id': 1})
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Failed to update status'}

    @pytest.mark.parametrize("user_id, expected_status_code, expected_response", [
        (1, 200, {'status': 'read'}),
        (None, 400, {'error': 'Failed to update status'}),
    ])
    @patch('app.message_status_manager')

    def test_mark_message_read_various_inputs(self, mock_message_status_manager, client, user_id, expected_status_code, expected_response):
        mock_message_status_manager.mark_as_read.return_value = {'status': 'read'} if user_id else None

        response = client.post('/api/messages/1/read', json={'user_id': user_id})
        assert response.status_code == expected_status_code
        assert response.get_json() == expected_response

# Third-party
# Local


import pytest
from unittest.mock import patch, Mock
from app import get_message_status
from flask import Flask  # app removed - use "from app import app"

class TestGetMessageStatus:
    @patch('app.message_status_manager.get_message_status')

    def test_get_message_status_found(self, mock_get_message_status, client):
        mock_get_message_status.return_value = {'status': 'delivered'}
        
        response = client.get('/api/messages/1/status')
        
        assert response.status_code == 200
        assert response.get_json() == {'status': 'delivered'}

    @patch('app.message_status_manager.get_message_status')

    def test_get_message_status_not_found(self, mock_get_message_status, client):
        mock_get_message_status.return_value = None
        
        response = client.get('/api/messages/999/status')
        
        assert response.status_code == 404
        assert response.get_json() == {'error': 'Message not found'}

    @pytest.mark.parametrize("message_id, mock_return_value, expected_status, expected_response", [
        (1, {'status': 'read'}, 200, {'status': 'read'}),
        (2, None, 404, {'error': 'Message not found'}),
    ])
    @patch('app.message_status_manager.get_message_status')

    def test_get_message_status_various_cases(self, mock_get_message_status, client, message_id, mock_return_value, expected_status, expected_response):
        mock_get_message_status.return_value = mock_return_value
        
        response = client.get(f'/api/messages/{message_id}/status')
        
        assert response.status_code == expected_status
        assert response.get_json() == expected_response

# Third-party
# Local - USE ACTUAL PATHS from source


import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import get_room_message_statuses

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

    @patch('app.message_status_manager.get_room_message_statuses')

    def test_get_room_message_statuses_invalid_room_id(self, mock_get_statuses, client):
        mock_get_statuses.side_effect = ValueError("Invalid room ID")
        
        response = client.get('/api/rooms/invalid/message-statuses?user_id=1')
        
        assert response.status_code == 404

# Third-party
# Local - USE ACTUAL PATHS from source

