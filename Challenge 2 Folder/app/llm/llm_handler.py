def generate_recipe(prompt: str, tokenizer, model):
    """
    Generate a recipe based on a user prompt using GPT-J.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_length=200,
        temperature=0.7,  # Adjust creativity
        top_k=50,        # Filter for the top-k tokens
        top_p=0.9        # Nucleus sampling
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
