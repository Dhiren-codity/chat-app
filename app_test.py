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

# Third-party
# Local
import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import get_status
# Third-party
# Local
import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import start_typing
# Import the function to be tested
import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import stop_typing
# Third-party
# Local
import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import get_typing_users
# Third-party
# Local
import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import create_group
# Third-party
# Local
import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import rename_group
# Third-party
# Local - USE ACTUAL PATHS from source
import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import customize_group_title
# Third-party
# Local
import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import mark_message_delivered
# Third-party
# Local
import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import mark_message_read
# Third-party
# Local
import pytest
from unittest.mock import patch, Mock
from app import get_message_status
from flask import Flask  # app removed - use "from app import app"
# Third-party
# Local - USE ACTUAL PATHS from source
import pytest
from unittest.mock import patch, Mock
from flask import Flask  # app removed - use "from app import app"
from app import get_room_message_statuses
# Third-party
# Local - USE ACTUAL PATHS from source