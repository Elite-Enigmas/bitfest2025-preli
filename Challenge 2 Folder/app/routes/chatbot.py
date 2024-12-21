from fastapi import APIRouter, HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer
import torch

router = APIRouter()

# Load the model and tokenizer once
MODEL_NAME = "EleutherAI/gpt-neo-1.3B"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")

# Initialize vector store
file_path = "/kaggle/input/kuet-preli-1/my_fav_recipes.txt"
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def load_recipes(file_path):
    """
    Load recipes from a text file.
    """
    with open(file_path, "r") as file:
        content = file.read()
    return [{"page_content": content, "metadata": {}}]  # Mock structure for compatibility


def split_documents(documents):
    """
    Split documents into smaller chunks for indexing.
    """
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents(documents)


def create_vectorstore(split_docs):
    """
    Create FAISS vector store.
    """
    embeddings = embedding_model
    return FAISS.from_documents(split_docs, embeddings)


def extract_first_recipe_block(response):
    """
    Extract the first recipe block from the response.
    """
    lines = response.splitlines()
    start_collecting = False
    collected_lines = []

    for line in lines:
        if line.startswith("#"):
            if start_collecting:
                break
            start_collecting = True
            continue
        if start_collecting:
            collected_lines.append(line.strip())

    return "\n".join(collected_lines)


# Load recipes and vector store at startup
documents = load_recipes(file_path)
split_docs = split_documents(documents)
vectorstore = create_vectorstore(split_docs)


def query_local_llm(query, vectorstore, tokenizer, model):
    """
    Query the local LLM using the vector store and return the generated response.
    """
    # Retrieve relevant documents
    docs = vectorstore.similarity_search(query, k=3)
    relevant_docs = "\n".join([doc.page_content for doc in docs])

    # Prepare prompt
    prompt = f"Relevant recipes:\n{relevant_docs}\n\nUser Query: {query}\nAnswer:"

    # Generate response
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        top_k=50,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


@router.post("/chatbot/")
def chatbot_endpoint(query: str):
    """
    Chatbot endpoint to generate recipes based on user queries.
    """
    try:
        response = query_local_llm(query, vectorstore, tokenizer, model)
        cleaned_response = extract_first_recipe_block(response)
        return {"response": cleaned_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
