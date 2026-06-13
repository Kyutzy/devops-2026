import pytest
from app import APP

@pytest.fixture()
def client():
    app = APP
    app.config.update({
        "TESTING" : True
    })
    yield app.test_client()

def test_index_is_acessible(client):
    response = client.get('/')
    assert response.status_code == 200

def test_name_in_response(client):
    response = client.get('/')
    assert 'Cesar Cunha Ziobro' in response.data.decode()
