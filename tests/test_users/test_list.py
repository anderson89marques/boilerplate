async def test_when_list_users_return_success(client):
    # arraneg/act
    response = await client.get('/users/')

    # assert
    assert response.status_code == 200
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }