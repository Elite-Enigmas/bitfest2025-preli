from fastapi import APIRouter, HTTPException
from app.llm.model_loader import load_and_cache_model
from app.llm.llm_handler import generate_recipe

router = APIRouter()

# Load the model and tokenizer during startup
MODEL_NAME = "EleutherAI/gpt-neo-1.3B"  # Replace with the model you're using
CACHE_DIR = "./model_cache"  # Optional: Specify a custom cache directory

try:
    tokenizer, model = load_and_cache_model(MODEL_NAME, CACHE_DIR)
    print(f"Model '{MODEL_NAME}' loaded successfully and ready for use.")
except Exception as e:
    raise RuntimeError(f"Failed to load model '{MODEL_NAME}': {str(e)}")

@router.post("/chatbot/")
def chatbot_endpoint(query: str):
    """
    Chatbot endpoint to generate recipes based on user queries.
    """
    try:
        response = generate_recipe(query, tokenizer, model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
