from backend.documents.document_service import DocumentService
from backend.documents.document_repository import DocumentRepository
from backend.documents.document_mapper import (
    DocumentOut,
    DocumentIn,
)

from fastapi import APIRouter, Depends

doc_route = APIRouter(prefix="/documents")

def get_repository():
    return DocumentRepository()

def get_service():
    return DocumentService(repository=get_repository())

@doc_route.get("/", response_model=DocumentOut)
def get_user(
    doc_id: int,
    document_service: DocumentService = Depends(get_service)
    ):
    return document_service.get(doc_id=doc_id)

@doc_route.post("/")
def save_user(
    document: DocumentIn,
    document_service: DocumentService = Depends(get_service)
    ):
    return document_service.save(document=document)

@doc_route.delete("/")
def delete_user(
    doc_id: int,
    document_service: DocumentService = Depends(get_service)
    ):
    return document_service.delete(doc_id=doc_id)
