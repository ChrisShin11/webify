from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    file_path: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    uploaded_at: datetime
    uploaded_by: int

    class Config:
        from_attributes = True