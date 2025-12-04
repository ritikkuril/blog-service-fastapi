from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models,schemas

router = APIRouter(prefix="/blogs", tags=["Blogs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.post("/", response_model=schemas.BlogOut)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    blog_model = models.Blog(title=blog.title, content=blog.content)
    db.add(blog_model)
    db.commit()
    db.refresh(blog_model)
    return blog_model

@router.get("/", response_model=list[schemas.BlogOut])
def get_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()

@router.get("/{id}", response_model=schemas.BlogOut)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/{id}", response_model=schemas.BlogOut)
def update_blog(id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    blog_data = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog_data:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog_data.title = blog.title
    blog_data.content = blog.content
    db.commit()
    db.refresh(blog_data)
    return blog_data

@router.delete("/{id}")
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    db.delete(blog)
    db.commit()

    return {"message": "Blog deleted successfully"}