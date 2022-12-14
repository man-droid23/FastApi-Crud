from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_posts = models.Post(**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def get_Allposts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    get_data = db.query(models.Post).filter(models.Post.id == id).first()
    if not get_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return get_data

@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    get_data = db.query(models.Post).filter(models.Post.id == id)
    if not get_data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    get_data.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": "Post updated successfully"}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    delete_data = db.query(models.Post).filter(models.Post.id == id)
    if not delete_data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    delete_data.delete(synchronize_session=False)
    db.commit()
    return {"data": f"Post {id} deleted successfully"}