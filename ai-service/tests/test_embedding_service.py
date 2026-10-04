from unittest.mock import patch

from app.services.embedding_service import create_embedding_model


def test_create_embedding_model():
    with patch("app.services.embedding_service.OpenAIEmbeddings") as mock_embeddings:
        create_embedding_model()

        mock_embeddings.assert_called_once()

        kwargs = mock_embeddings.call_args.kwargs

        assert kwargs["model"] == "text-embedding-3-small"
        assert "api_key" in kwargs