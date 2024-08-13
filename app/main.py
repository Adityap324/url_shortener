from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
import string, random

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.post("/shorten", response_model=schemas.URLInfo)
def shorten_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()
    db_url = models.URL(original_url=url.original_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(db_url.original_url)
