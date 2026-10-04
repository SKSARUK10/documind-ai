from app.core.config import Settings, get_settings


def test_settings_load_from_env_file() -> None:
    settings = get_settings()
    assert settings.port > 0
    assert settings.cors_origins


def test_empty_llm_base_url_falls_back_to_default(monkeypatch) -> None:
    monkeypatch.setenv("LLM_BASE_URL", "")
    assert Settings(_env_file=None).llm_base_url == "https://api.openai.com/v1"


def test_explicit_llm_base_url_is_kept(monkeypatch) -> None:
    monkeypatch.setenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    assert Settings(_env_file=None).llm_base_url == "https://api.groq.com/openai/v1"
