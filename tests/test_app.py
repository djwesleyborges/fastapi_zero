from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app

client = TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to FastAPI Zero!'}


def test_create_user_deve_retornar_ok_e_usuario_criado():
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    response = client.post('/users/', json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()


def test_get_users_deve_retornar_ok_e_lista_de_usuarios():
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert 'users' in response.json()
    assert isinstance(response.json()['users'], list)


def test_update_user_deve_retornar_ok_e_usuario_atualizado():
    user_data = {
        'username': 'updateduser',
        'email': 'updateduser@example.com',
        'password': 'updatedpassword',
    }
    response = client.put('/users/1', json=user_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']


def test_delete_user_deve_retornar_ok_e_usuario_deletado():
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert 'username' in response.json()
    assert 'email' in response.json()
