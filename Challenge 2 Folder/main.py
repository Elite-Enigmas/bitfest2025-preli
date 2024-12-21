from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session

from app.routes import chatbot
from bootstrap import bootstrap
from database import get_db
from crud import upload_recipes, get_recipes, update_ingredient, update_ingredients_logic
from models import IngredientModel
from schemas import Ingredient
from app.llm.model_loader import load_and_cache_model


app = FastAPI()

# Bootstrap the application on startup
bootstrap()

# Model configuration
MODEL_NAME = "EleutherAI/gpt-neo-1.3B"
CACHE_DIR = "./model_cache"  # Specify a custom cache directory if needed

# Load and cache the model at startup
tokenizer, model = load_and_cache_model(MODEL_NAME, CACHE_DIR)

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

app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])

