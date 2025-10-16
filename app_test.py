from unittest.mock import patch, Mock
import pytest
from flask import Flask
from app import app, login, get_messages, update_status, get_status

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
            id=1,
            username='testuser',
            check_password=Mock(return_value=True),
            create_session=Mock(return_value='session_token')
        )
        response = client.post('/api/users/login', json={'username': 'testuser', 'password': 'correct_password'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['token'] == 'session_token'
        assert data['user_id'] == 1

    @patch('app.User')
    def test_login_invalid_credentials(self, mock_user, client):
        mock_user.query.filter_by.return_value.first.return_value = Mock(
            id=1,
            username='testuser',
            check_password=Mock(return_value=False)
        )
        response = client.post('/api/users/login', json={'username': 'testuser', 'password': 'wrong_password'})
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'Invalid credentials'

    @pytest.mark.parametrize("username,password", [
        ('', 'password'),
        ('username', ''),
        ('', ''),
        (None, 'password'),
        ('username', None),
        (None, None)
    ])
    @patch('app.User')
    def test_login_edge_cases(self, mock_user, client, username, password):
        mock_user.query.filter_by.return_value.first.return_value = None
        response = client.post('/api/users/login', json={'username': username, 'password': password})
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'Invalid credentials'

class TestGetMessages:
    @patch('app.Message')
    def test_get_messages_happy_path(self, mock_message, client):
        mock_message.query.filter_by.return_value.order_by.return_value.all.return_value = [
            Mock(id=1, user_id=1, content='Hello', created_at=Mock(isoformat=lambda: '2023-10-01T12:00:00')),
            Mock(id=2, user_id=2, content='Hi', created_at=Mock(isoformat=lambda: '2023-10-01T12:01:00'))
        ]
        response = client.get('/api/messages?room_id=1')
        assert response.status_code == 200
        assert response.get_json() == [
            {'id': 1, 'user_id': 1, 'content': 'Hello', 'created_at': '2023-10-01T12:00:00'},
            {'id': 2, 'user_id': 2, 'content': 'Hi', 'created_at': '2023-10-01T12:01:00'}
        ]

    @patch('app.Message')
    def test_get_messages_no_messages(self, mock_message, client):
        mock_message.query.filter_by.return_value.order_by.return_value.all.return_value = []
        response = client.get('/api/messages?room_id=1')
        assert response.status_code == 200
        assert response.get_json() == []

class TestGetStatus:
    @patch('app.status_manager')
    def test_get_status_happy_path(self, mock_status_manager, client):
        mock_status_manager.get_user_status.return_value = {'status': 'online'}
        response = client.get('/api/status/1')
        assert response.status_code == 200
        assert response.get_json() == {'status': 'online'}