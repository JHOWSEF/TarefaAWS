import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_healthcheck(client):
    response = client.get('/image/healthcheck')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}
