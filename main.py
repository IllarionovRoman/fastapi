from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from typing import List
import uvicorn
from database import engine, init_db
from crud import get_documents, delete_document, create_document as create_document_crud
from schemas import Document, DocumentCreate

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(title="FastAPI", version=1, routes=app.routes)


@app.post("/documents/", response_model=Document)
async def create_document(document: DocumentCreate):
    return create_document_crud(document)


@app.get("/documents/", response_model=List[Document])
async def search_documents(query: str):
    documents = get_documents(query)
    return documents


@app.delete("/documents/{document_id}")
async def remove_document(document_id: int):
    deleted = delete_document(document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
