from fastapi import FastAPI, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import HTTPAuthorizationCredentials
import models, schemas
from database import SessionLocal, engine, get_db
from utils import verify_jwt_token, security  # import shared security setup
from starlette.middleware.cors import CORSMiddleware
from models import Base

app = FastAPI(
    title="LibraryPal Books Service",
    description="API for managing books in the LibraryPal application.",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Add CORSMiddleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Healthcheck
@app.get("/health", tags=["Health"])
def healthcheck():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except SQLAlchemyError as e:
        return {"status": "error", "db": "unreachable", "detail": str(e)}
    finally:
        db.close()

# Create a Book
@app.post("/books/", response_model=schemas.Book, tags=["Books"])
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    verify_jwt_token(credentials)
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Update a Book
@app.put("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def update_book(
    book_id: int,
    book: schemas.BookUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    verify_jwt_token(credentials)
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

# Delete a Book
@app.delete("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    verify_jwt_token(credentials)
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book

# Get all Books
@app.get("/books/", response_model=list[schemas.Book], tags=["Books"])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

# Get a single Book by ID
@app.get("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book