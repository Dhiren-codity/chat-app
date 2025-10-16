from unittest.mock import patch, Mock
import pytest
from flask import Flask
from app import app

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

    @patch('app.User')
    def test_login_user_not_found(self, mock_user, client):
        mock_user.query.filter_by.return_value.first.return_value = None

        response = client.post('/api/users/login', json={'username': 'nonexistent', 'password': 'any_password'})
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

    @patch('app.Message')
    def test_get_messages_invalid_room_id(self, mock_message, client):
        mock_message.query.filter_by.return_value.order_by.return_value.all.return_value = []

        response = client.get('/api/messages?room_id=invalid')

        assert response.status_code == 200
        assert response.get_json() == []