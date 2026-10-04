from typing import Sequence

from openai import OpenAI

from langchain_core.embeddings import Embeddings

from app.core.config import get_settings


class OpenAIEmbeddingModel(Embeddings):

    def __init__(self):
        settings = get_settings()

        self.client = OpenAI(
            api_key=settings.llm_api_key.get_secret_value(),
            base_url=settings.llm_base_url,
        )

        self.model = settings.embedding_model

    def embed_documents(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:

        response = self.client.embeddings.create(
            model=self.model,
            input=list(texts),
        )

        return [
            item.embedding
            for item in response.data
        ]

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding


def create_embedding_model() -> OpenAIEmbeddingModel:

    return OpenAIEmbeddingModel()
