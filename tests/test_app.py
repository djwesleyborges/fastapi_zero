from http import HTTPStatus

from fastapi_zero.schema import UserPublicSchema


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to FastAPI Zero!'}


def test_create_user_deve_retornar_ok_e_usuario_criado(client):
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


def test_create_user_deve_retornar_conflito_quando_usuario_existir(client):
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    client.post('/users/', json=user_data)
    response = client.post('/users/', json=user_data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_deve_retornar_conflito_quando_email_existir(client):
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    client.post('/users/', json=user_data)
    user_data['username'] = 'updateduser'
    response = client.post('/users/', json=user_data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def teste_read_user_with_users(user, client):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_users_deve_retornar_ok_e_lista_de_usuarios(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert 'users' in response.json()
    assert isinstance(response.json()['users'], list)


def test_update_user_deve_retornar_ok_e_usuario_atualizado(client, user):
    user_data = {
        'username': 'updateduser',
        'email': 'updateduser@example.com',
        'password': 'updatedpassword',
    }
    response = client.put('/users/1', json=user_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']


def test_delete_user_deve_retornar_ok_e_usuario_deletado(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert 'message' in response.json()


def test_update_integrity_error_deve(client, user):
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user das fixtures para fausto
    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or email already exists'
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'nonexistentuser',
            'email': 'nonexistentuser@example.com',
            'password': 'nonexistentpassword',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_not_found(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
