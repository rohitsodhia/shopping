def test_login(client):
    response = client.post("/auth/login", json={"password": "test"})
    assert response.status_code == 200
