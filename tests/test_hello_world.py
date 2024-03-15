async def test_when_say_hello_Return_with_success(client):
    # arrange
    expected = {'message': 'Hello World'}

    # act
    response = await client.get('/')

    # assert
    assert response.status_code == 200
    assert response.json() == expected
