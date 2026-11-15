from backend.documents.document_service import DocumentService
from backend.documents.document_repository import DocumentRepository
from backend.documents.document_mapper import (
    DocumentInfoOut,
    DocumentInfo,
    DocumentInfoFilter
)

from fastapi import APIRouter, Depends, UploadFile, File, Form


doc_route = APIRouter(prefix="/documents")

def get_repository():
    return DocumentRepository()

def get_service():
    return DocumentService(repository=get_repository())

@doc_route.get("/", response_model=list[DocumentInfoOut])
def get_all(
    doc_filter: DocumentInfoFilter,
    document_service: DocumentService = Depends(get_service)
    ):
    return document_service.get_all(doc_filter=doc_filter)

@doc_route.get("/{doc_id}", response_model=DocumentInfoOut)
def get_one(doc_id: int, document_service: DocumentService = Depends(get_service)):
    return document_service.get_all(doc_id=doc_id)

@doc_route.post("/")
def save_document_info(
    document_info: DocumentInfo,
    document_service: DocumentService = Depends(get_service)
    ):
    return document_service.save_info(document=document_info)

@doc_route.post("/{doc_id}/upload")
def upload_file(
    doc_id: int,
    doc_description: str = Form(...),
    document: UploadFile = File(...),
    document_service: DocumentService = Depends(get_service)
    ):
    return document_service.upload_file(doc_id=doc_id, file=document, doc_description=doc_description)

@doc_route.post("/upload")
def upload_file(
    doc_description: str = Form(...), 
    document: UploadFile = File(...),
    document_service: DocumentService = Depends(get_service)
    ):
    return document_service.upload_file(file=document, doc_description=doc_description)

@doc_route.delete("/")
def delete_document(
    doc_id: int,
    document_service: DocumentService = Depends(get_service)
    ):
    return document_service.delete(doc_id=doc_id)
