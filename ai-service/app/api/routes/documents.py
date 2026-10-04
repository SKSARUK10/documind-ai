from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.document import DocumentResponse
from app.services.document_ingestion_service import ingest_document
from app.services.document_storage_service import save_document


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
)
def upload_document(
    file: UploadFile = File(...),
) -> DocumentResponse:

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    document_id, file_path = save_document(file)

    ingest_document(
        document_id,
        file_path,
        file.filename,
    )

    return DocumentResponse(
        document_id=document_id,
        document_name=file.filename,
    )
