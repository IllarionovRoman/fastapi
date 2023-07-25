from pydantic import BaseModel
from typing import List
from datetime import date


class DocumentBase(BaseModel):
    rubrics: List[str]
    text: str
    created_date: date


class DocumentCreate(DocumentBase):
    id: int


class Document(DocumentBase):
    id: int

    class Config:
        orm_mode = True
