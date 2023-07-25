from database import SessionLocal, Document
from schemas import DocumentCreate
from elasticsearch import Elasticsearch


es = Elasticsearch(hosts=["https://localhost:9200"])
es.indices.create(index='my-index', ignore=400)


def create_document(document: DocumentCreate):
    session = SessionLocal()
    db_document = Document(
        id=document.id,
        rubrics=document.rubrics,
        text=document.text,
        created_date=document.created_date
    )
    session.add(db_document)
    session.commit()
    session.refresh(db_document)
    session.close()
    index_document(db_document)
    return db_document


def get_documents(query: str):
    body = {
        "query": {
            "match": {
                "text": query
            }
        },
        "sort": [
            {
                "created_date": "desc"
            }
        ],
        "size": 20
    }
    results = es.search(index="documents", body=body)
    document_ids = [hit["_source"]["id"] for hit in results["hits"]["hits"]]
    session = SessionLocal()
    documents = session.query(Document).filter(Document.id.in_(document_ids)).all()
    session.close()
    return documents


def delete_document(document_id: int):
    session = SessionLocal()
    document = session.query(Document).filter(Document.id == document_id).first()
    if not document:
        return False
    session.delete(document)
    session.commit()
    session.close()
    delete_document_from_index(document_id)
    return True


def index_document(document: Document):
    es.index(index='documents', id=document.id, body={"id": document.id, "text": document.text})


def delete_document_from_index(document_id: int):
    es.delete(index='documents', id=document_id)


def create_index():
    if not es.indices.exists(index='documents'):
        es.indices.create(index='documents', body={
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "text": {"type": "text"}
                }
            }
        })


create_index()
