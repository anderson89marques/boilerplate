async def test_when_delete_user_return_success(client, user):
    response = await client.delete(f'/users/{user.id}')

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}
