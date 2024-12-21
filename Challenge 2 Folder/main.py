from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session

from bootstrap import bootstrap
from database import get_db
from crud import upload_recipes, get_recipes, update_ingredient, update_ingredients_logic
from llm import process_chat_query
from models import IngredientModel
from schemas import Ingredient

app = FastAPI()

# Bootstrap the application on startup
bootstrap()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/upload-recipes/")
async def upload_recipes_endpoint(file: UploadFile, db: Session = Depends(get_db)):
    return await upload_recipes(file, db)

@app.get("/recipes/")
def get_recipes_endpoint(taste: str = None, db: Session = Depends(get_db)):
    return get_recipes(taste, db)

@app.get("/ingredients/")
def get_all_ingredients(db: Session = Depends(get_db)):
    # Query all ingredients
    ingredients = db.query(IngredientModel).all()
    return ingredients

@app.put("/ingredients/")
def update_ingredient_endpoint(update: Ingredient, db: Session = Depends(get_db)):
    return update_ingredient(update.name, update.quantity, update.unit, db)

@app.put("/ingredients/bulk/")
def update_ingredients_bulk(ingredients: list[Ingredient], db: Session = Depends(get_db)):
    return update_ingredients_logic(ingredients, db)

@app.post("/chatbot/")
def chatbot_endpoint(query: str, db: Session = Depends(get_db)):
    return process_chat_query(query, db)

