from sqlalchemy.orm import Session
from models import IngredientModel
from database import engine, SessionLocal, Base

def initialize_database():
    # Create tables if they do not exist
    Base.metadata.create_all(bind=engine)

def add_default_ingredients(db: Session):
    # Predefined ingredients
    default_ingredients = [
        {"name": "Flour", "quantity": 1.0, "unit": "kg"},
        {"name": "Sugar", "quantity": 500.0, "unit": "grams"},
        {"name": "Eggs", "quantity": 12.0, "unit": "pieces"},
        {"name": "Butter", "quantity": 200.0, "unit": "grams"},
        {"name": "Milk", "quantity": 5.0, "unit": "liters"}
    ]

    # Add ingredients if they do not already exist
    for ingredient in default_ingredients:
        existing = db.query(IngredientModel).filter(IngredientModel.name == ingredient["name"]).first()
        if not existing:
            new_ingredient = IngredientModel(
                name=ingredient["name"],
                quantity=ingredient["quantity"],
                unit=ingredient["unit"]
            )
            db.add(new_ingredient)
    db.commit()

def bootstrap():
    print("Initializing database and adding default ingredients...")
    initialize_database()
    db = SessionLocal()
    try:
        add_default_ingredients(db)
    finally:
        db.close()
    print("Bootstrap completed successfully!")
