from fastapi import APIRouter, File, UploadFile, HTTPException, Depends

from app.api.dependencies import get_current_user
from app.repositories.document_repository import (
    get_document_by_id,
    get_document_history,
)
from app.schemas.document_schema import DocumentUploadResponse
from app.services.document_service import save_uploaded_document

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    return await save_uploaded_document(file , current_user)

@router.get("/history")
async def document_history(
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    ):
    documents = await get_document_history(
        user_id=current_user["user_id"],
        limit=limit,
    )
    return {
        "message": "Document history fetched successfully",
        "count": len(documents),
        "documents": documents,
    }

@router.get("/{document_id}")
async def document_detail(
    document_id: str,
    current_user: dict = Depends(get_current_user),
):
    document = await get_document_by_id(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    if document.get("uploaded_by") != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view this document",
        )

    return document