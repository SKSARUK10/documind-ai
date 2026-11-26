from unittest.mock import patch

from app.core.config import get_settings
from app.services.embedding_service import (
    OpenAIEmbeddingModel,
    create_embedding_model,
)


def test_create_embedding_model() -> None:
    with patch("app.services.embedding_service.OpenAI") as mock_openai:
        model = create_embedding_model()

    assert isinstance(model, OpenAIEmbeddingModel)
    assert model.model == get_settings().embedding_model
    assert model.client is mock_openai.return_value
