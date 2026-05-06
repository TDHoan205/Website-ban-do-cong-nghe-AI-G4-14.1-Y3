"""
Seed Controller - Chay seed du lieu
Tuong duong Controllers/SeedController.cs trong C#
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Data.database import get_db
from Data.Seed.seed_data import seed_all

router = APIRouter(prefix="/Seed")


@router.post("/Run")
def run_seed(db: Session = Depends(get_db)):
    seed_all(db)
    return {"success": True}
