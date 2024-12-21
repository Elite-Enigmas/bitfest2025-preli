from sqlalchemy.orm import Session
from models import Recipe, IngredientModel
from typing import List


async def upload_recipes(file, db: Session):
    content = await file.read()
    recipes = content.decode("utf-8").split("\n\n")  # Split by recipes

    # Calculate the starting recipe number
    with open("my_fav_recipes.txt", "r") as f:
        existing_recipes = f.read().strip().split("\n\n")
    next_recipe_number = len(existing_recipes) + 1

    with open("my_fav_recipes.txt", "a") as f:  # Open file in append mode
        for recipe in recipes:
            lines = recipe.strip().split("\n")

            # Parse recipe details
            name = lines[0].split(": ")[1]  # Extract recipe name
            ingredients_section = ": ".join(lines[1].split(": ")[1:]).strip()  # Safely handle nested ": "

            # Parse ingredients with quantities
            ingredients = []
            for ingredient_line in ingredients_section.split(", "):  # Split by ', '
                if ": " in ingredient_line:
                    ingredient_name, ingredient_quantity = ingredient_line.split(": ", 1)
                    ingredients.append(f"{ingredient_name.strip()} ({ingredient_quantity.strip()})")
                else:
                    print(f"Skipping malformed ingredient: {ingredient_line}")

            taste = lines[2].split(": ")[1]  # Extract taste
            cuisine = lines[3].split(": ")[1]  # Extract cuisine
            preparation_time = int(lines[4].split(": ")[1])  # Extract preparation time

            # Combine instructions
            instructions_start_index = 6  # Instructions start after "Instructions:"
            instructions = "\n".join(lines[instructions_start_index:])

            # Combine parsed data
            recipe_data = {
                "name": name,
                "ingredients": ", ".join(ingredients),  # Store as a comma-separated string
                "taste": taste,
                "cuisine": cuisine,
                "preparation_time": preparation_time,
                "instructions": instructions
            }

            # Add to database
            new_recipe = Recipe(**recipe_data)
            db.add(new_recipe)

            # Write to file with auto-generated recipe number
            f.write(f"# Recipe {next_recipe_number}\n")
            f.write(f"Name: {name}\n")
            f.write(f"Ingredients: {', '.join(ingredients)}\n")
            f.write(f"Taste: {taste}\n")
            f.write(f"Cuisine: {cuisine}\n")
            f.write(f"Preparation Time: {preparation_time}\n")
            f.write("Instructions:\n")
            f.write(f"{instructions}\n\n")

            next_recipe_number += 1  # Increment for the next recipe

    db.commit()
    return {"message": "Recipes uploaded, parsed, and saved to file successfully"}



def get_recipes(taste: str, db: Session):
    query = db.query(Recipe)
    if taste:
        query = query.filter(Recipe.taste == taste)
    return query.all()


def update_ingredient(name: str, quantity: float, unit: str, db: Session):
    ingredient = db.query(IngredientModel).filter(IngredientModel.name == name).first()
    if ingredient:
        ingredient.quantity += quantity
        ingredient.unit = unit
    else:
        new_ingredient = IngredientModel(name=name, quantity=quantity, unit=unit)
        db.add(new_ingredient)
    db.commit()
    return {"message": f"Ingredient '{name}' updated successfully"}

def update_ingredients_logic(ingredients: list, db: Session):
    for ingredient in ingredients:
        existing = db.query(IngredientModel).filter(IngredientModel.name == ingredient.name).first()
        if existing:
            existing.quantity += ingredient.quantity
            existing.unit = ingredient.unit
        else:
            new_ingredient = IngredientModel(
                name=ingredient.name, quantity=ingredient.quantity, unit=ingredient.unit
            )
            db.add(new_ingredient)
    db.commit()
    return {"message": "Ingredients updated successfully"}