from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


async def test_when_say_hello_Return_with_success():
    # arrange
    expected = {'message': 'Hello World'}

    # act
    response = client.get('/')

    # assert
    assert response.status_code == 200
    assert response.json() == expected
