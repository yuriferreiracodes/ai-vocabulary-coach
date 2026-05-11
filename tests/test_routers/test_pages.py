def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Vocab Coach" in response.text


def test_onboarding_page_returns_200(client):
    response = client.get("/onboarding")
    assert response.status_code == 200
    assert "Get Started" in response.text or "onboarding" in response.text.lower()


def test_decks_page_returns_200(client):
    response = client.get("/decks")
    assert response.status_code == 200
