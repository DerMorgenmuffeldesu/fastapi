from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/advertisement", response_model=schemas.AdvertisementOut)
def create_advertisement(advertisement: schemas.AdvertisementCreate, db: Session = Depends(get_db)):
    db_advertisement = models.Advertisement(**advertisement.dict())
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement

@app.patch("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementOut)
def update_advertisement(advertisement_id: int, advertisement: schemas.AdvertisementUpdate, db: Session = Depends(get_db)):
    db_advertisement = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()
    if not db_advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    for key, value in advertisement.dict(exclude_unset=True).items():
        setattr(db_advertisement, key, value)
    
    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement

@app.delete("/advertisement/{advertisement_id}")
def delete_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    db_advertisement = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()
    if not db_advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    db.delete(db_advertisement)
    db.commit()
    return {"detail": "Advertisement deleted"}

@app.get("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementOut)
def get_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    db_advertisement = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()
    if not db_advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_advertisement

@app.get("/advertisement")
def search_advertisements(title: str = None, author: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Advertisement)
    if title:
        query = query.filter(models.Advertisement.title.contains(title))
    if author:
        query = query.filter(models.Advertisement.author == author)
    return query.all()
