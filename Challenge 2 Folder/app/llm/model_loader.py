from transformers import AutoModelForCausalLM, AutoTokenizer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_cache_model(model_name: str, cache_dir: str = None):
    logger.info(f"Loading model '{model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir, device_map="auto")
    logger.info(f"Model '{model_name}' loaded successfully.")
    return tokenizer, model

def preload_models(model_names: list, cache_dir: str = None):
    """
    Preload multiple models and store them in a dictionary.
    """
    loaded_models = {}
    for model_name in model_names:
        try:
            tokenizer, model = load_and_cache_model(model_name, cache_dir)
            loaded_models[model_name] = (tokenizer, model)
        except Exception as e:
            logger.error(f"Failed to load model '{model_name}': {str(e)}")
    return loaded_models