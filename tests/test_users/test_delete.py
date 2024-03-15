async def test_when_delete_user_return_success(client):
    response_c = await client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    response = await client.delete(f'/users/{response_c.json()["id"]}')

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}