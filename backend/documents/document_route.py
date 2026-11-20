from backend.documents.document_service import DocumentService
from backend.documents.document_repository import DocumentRepository
from backend.documents.document_mapper import (
    DocumentOut,
    DocumentIn,
)
from backend.documents.document_storage import (
    get_stored_upload,
    remove_stored_upload,
    store_upload,
)

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse

from backend.auth.auth_dependency import get_current_user
from backend.users.user_model import UserSqlModel

doc_route = APIRouter(prefix="/documents")

def get_repository():
    return DocumentRepository()

def get_service():
    return DocumentService(repository=get_repository())

@doc_route.get("/all", response_model=list[DocumentOut])
def get_all_documents(
    name: str | None = Query(default=None, max_length=80),
    document_service: DocumentService = Depends(get_service),
    current_user: UserSqlModel = Depends(get_current_user),
) -> list[DocumentOut]:
    return document_service.get_all(
        category=current_user.category,
        name=name,
    )

@doc_route.get("/download", response_class=FileResponse)
def download_document(
    doc_id: int,
    document_service: DocumentService = Depends(get_service),
    current_user: UserSqlModel = Depends(get_current_user),
) -> FileResponse:
    download = document_service.get_for_download(
        doc_id=doc_id,
        category=current_user.category,
    )
    if download is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    document, doc_path = download
    stored_file = get_stored_upload(doc_path)
    if stored_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document file not found",
        )

    return FileResponse(
        path=stored_file,
        filename=document.doc_name,
        media_type="application/octet-stream",
    )

@doc_route.get("/", response_model=DocumentOut)
def get_document(
    doc_id: int,
    document_service: DocumentService = Depends(get_service),
    current_user: UserSqlModel = Depends(get_current_user),
):
    document = document_service.get(
        doc_id=doc_id,
        category=current_user.category,
    )
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return document

@doc_route.post("/", response_model=list[DocumentOut], status_code=status.HTTP_201_CREATED)
async def upload_documents(
    files: list[UploadFile] = File(...),
    document_service: DocumentService = Depends(get_service),
    current_user: UserSqlModel = Depends(get_current_user),
) -> list[DocumentOut]:
    stored_uploads: list[tuple[str, str]] = []

    try:
        for upload in files:
            stored_uploads.append(await store_upload(upload))

        documents = [
            DocumentIn(doc_name=doc_name, doc_path=doc_path)
            for doc_name, doc_path in stored_uploads
        ]
        return document_service.save_many(
            documents=documents,
            owner_user_id=current_user.user_id,
        )
    except ValueError as error:
        for _, doc_path in stored_uploads:
            remove_stored_upload(doc_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except Exception:
        for _, doc_path in stored_uploads:
            remove_stored_upload(doc_path)
        raise
    finally:
        for upload in files:
            await upload.close()

@doc_route.delete("/")
def delete_user(
    doc_id: int,
    document_service: DocumentService = Depends(get_service),
    current_user: UserSqlModel = Depends(get_current_user),
) -> Response:
    deleted = document_service.delete(
        doc_id=doc_id,
        owner_user_id=current_user.user_id,
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
