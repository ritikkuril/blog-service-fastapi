from pydantic import BaseModel

class BlogCreate(BaseModel):
    title: str
    content: str

class BlogOut(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True
#So FastAPI can convert SQLAlchemy objects → Pydantic objects.