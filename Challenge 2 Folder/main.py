from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import upload_recipes, get_recipes, update_ingredient
from llm import process_chat_query

app = FastAPI()


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

@app.put("/ingredients/")
def update_ingredient_endpoint(name: str, quantity: float, db: Session = Depends(get_db)):
    return update_ingredient(name, quantity, db)

@app.post("/chatbot/")
def chatbot_endpoint(query: str, db: Session = Depends(get_db)):
    return process_chat_query(query, db)
