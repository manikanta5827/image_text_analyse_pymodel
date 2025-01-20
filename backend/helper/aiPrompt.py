def generate_prompt(extracted_text, include_details):
    return f"""
    The input is extracted text from a restaurant menu card. Your task is to:
    0. Don't exclude any food items.
    1. Identify and group all food items strictly under the categories explicitly mentioned in the input text. 
    2. Ensure all food items mentioned in the menu text are included in the output, grouped under their most relevant category. Do not exclude any food items.
    3. If duplicate food items are detected, include them and assign each duplicate to the nearest relevant category.
    4. Do not create or infer new categories or food items. Use only the categories and food names explicitly present in the prompt.
    5. Ensure that food names and categories are grammatically correct and formatted consistently, preserving the exact names and prices as they appear in the prompt.
    6. Retain the original currency format for prices (e.g., '$', '₹', 'rupees'). If the price field contains an 'S' character mistakenly converted from '$', replace the 'S' with '$'. If no price is mentioned, set the price field to `null`. Strictly ensure that the price field is a valid 'integer', 'number', or 'float'.
    7. Include a 'diet' field for each food item with values 'veg' or 'Non-veg' based on the item's type.
    8. Provide a detailed description (2-3 sentences) for each food item in the 'description' field, highlighting its ingredients, taste, and appeal. For beverages or simple items, descriptions can be concise but still engaging.
    9. If 'includeDetails' is true, add the following fields:
        - 'ingredients': A list of key ingredients for each food item.
        - 'nutrition': A dictionary with keys 'fats', 'proteins', 'carbs', and 'calories' (values as strings).
        - 'spiceLevel': The spice level of the dish ('low', 'medium', 'high', or 'null' for non-spicy items like beverages or desserts).
    10. If 'includeDetails' is false, exclude 'ingredients', 'nutrition', and 'spiceLevel' fields from the output.
    11. Ensure that every food item and category are separated using commas so that the structure is clear and parsable.

    Structure the output strictly as:
    {{
        "categories": ["category1", "category2", ...],
        "items": [
            {{
                "name": "food_name",
                "category": "category_name",
                "description": "Detailed and engaging description",
                "price": "price"/'number',
                "diet": "veg/Non-veg",
                {', '.join([
                    '"ingredients": ["ingredient1", "ingredient2"]',
                    '"nutrition": { "fats": "value", "proteins": "value", "carbs": "value", "calories": "value" }',
                    '"spiceLevel": spiceLevel_value'
                ]) if include_details else ''}
            }}
        ]
    }}

    Additional Notes:
    - Ensure the food names, prices, and categories match exactly as they appear in the menu text.
    - Ensure proper grammatical and capitalization accuracy throughout.
    - Replace any 'S' in the price field with '$' if detected.
    - If any item cannot be assigned to a category, include it under a general category like 'Uncategorized', but avoid creating categories not present in the input text.
    - If no price is mentioned for an item, set the price field to `null`.
    -  If duplicate food items are detected, include them and assign each duplicate to the nearest relevant category.

    Input text:
    [{extracted_text}]
    
    includeDetails: [{include_details}]

    Important:
    - Return **only** the JSON response in the specified structure, without any additional text, commentary, or formatting, and ensure it is in double quotes.
    - Use double quotes for all property names and string values.
    - Validate that all food items from the menu text are accounted for and appropriately categorized.
    - Double-check that all items in the menu of Input text are present in the specified structure.
    - Ensure that food names and categories are grammatically correct and formatted consistently, preserving the exact names and prices as they appear in the prompt.
    """
