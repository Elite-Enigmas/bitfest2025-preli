import openai
from sqlalchemy.orm import Session
from models import Ingredient

# Replace with your OpenAI API key
openai.api_key = "your-openai-api-key"

def process_chat_query(query: str, db: Session):
    ingredients = db.query(Ingredient).all()
    ingredient_list = ", ".join([f"{ing.name} ({ing.quantity} {ing.unit})" for ing in ingredients])
    prompt = f"""
    You are a helpful kitchen assistant. Based on the following ingredients available at home: {ingredient_list}, 
    suggest a recipe for the user. 
    The user query is: {query}.
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return {"response": response.choices[0].text.strip()}
