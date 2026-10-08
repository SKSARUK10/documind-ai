import re

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.services.embedding_service import create_embedding_model


# Highest squared-L2 distance still considered relevant.
# Measured on the stored indexes: topical best scores are 0.75-1.38
# (rank 2/3 up to 1.62) while clearly unrelated queries start at 1.72.
MAX_RELEVANT_SCORE = 1.5

# Candidates may not fall this far behind the best candidate,
# so a long tail of weakly related chunks is never returned.
SCORE_MARGIN = 0.6


def create_vector_store(
    chunks: list[dict],
    document_id: str,
) -> FAISS:
    embedding_model = create_embedding_model()

    texts = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            "document_id": document_id,
            "page_number": chunk["page_number"],
            "chunk_index": index,
            **(
                {"sheet_name": chunk["sheet_name"]}
                if "sheet_name" in chunk
                else {}
            ),
        }
        for index, chunk in enumerate(chunks)
    ]

    vector_store = FAISS.from_texts(
        texts,
        embedding_model,
        metadatas=metadatas,
    )

    return vector_store


def save_vector_store(
    vector_store: FAISS,
    path: str,
) -> None:
    vector_store.save_local(path)


def load_vector_store(
    path: str,
) -> FAISS:
    embedding_model = create_embedding_model()

    return FAISS.load_local(
        path,
        embedding_model,
        allow_dangerous_deserialization=True,
    )


def filter_relevant_results(
    results: list[tuple[Document, float]],
) -> list[tuple[Document, float]]:

    if not results:
        return []

    best_score = min(
        score
        for _, score in results
    )

    ceiling = min(
        MAX_RELEVANT_SCORE,
        best_score + SCORE_MARGIN,
    )

    return [
        (document, score)
        for document, score in results
        if score <= ceiling
    ]


def search_vector_store(
    vector_store: FAISS,
    query: str,
    k: int = 3,
) -> list[dict]:

    module_match = re.search(
        r"\bmodule\s+(\d+)\b",
        query,
        re.IGNORECASE,
    )

    if module_match:

        module_number = module_match.group(1)

        all_documents = list(
            vector_store.docstore._dict.values()
        )

        matching_documents = [
            document
            for document in all_documents
            if re.search(
                rf"\bModule\s+{module_number}\s*:",
                document.page_content,
                re.IGNORECASE,
            )
        ]

        if matching_documents:

            target_index = matching_documents[0].metadata[
                "chunk_index"
            ]

            results = [
                (
                    document,
                    None,
                )
                for document in all_documents
                if document.metadata.get("chunk_index") in {
                    target_index,
                    target_index + 1,
                }
            ]

            results.sort(
                key=lambda result: result[0].metadata["chunk_index"]
            )

        else:
            results = []

    else:

        results = filter_relevant_results(
            [
                (
                    document,
                    float(score),
                )
                for document, score in vector_store.similarity_search_with_score(
                    query,
                    k=k,
                )
            ]
        )

    return [
        {
            "document_id": document.metadata["document_id"],
            "page_number": document.metadata["page_number"],
            "text": document.page_content,
            "score": score,
        }
        for document, score in results
    ]
