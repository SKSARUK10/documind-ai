from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_returns_501_not_implemented() -> None:
    response = client.post(
        "/agent/chat",
        json={"messages": [{"role": "user", "content": "hello"}]},
    )
    assert response.status_code == 501
    assert "not implemented" in response.json()["detail"].lower()


def test_chat_rejects_empty_messages() -> None:
    response = client.post("/agent/chat", json={"messages": []})
    assert response.status_code == 422


def test_chat_rejects_unknown_role() -> None:
    response = client.post(
        "/agent/chat",
        json={"messages": [{"role": "wizard", "content": "hi"}]},
    )
    assert response.status_code == 422


def test_chat_schema_exposes_request_and_response_models() -> None:
    schema = client.get("/openapi.json").json()["components"]["schemas"]
    assert "ChatRequest" in schema
    assert "ChatResponse" in schema
    assert set(schema["ChatResponse"]["properties"]) == {"answer", "traces", "sources"}


def test_list_tools_returns_empty_registry() -> None:
    response = client.get("/agent/tools")
    assert response.status_code == 200
    assert response.json() == {"tools": []}
