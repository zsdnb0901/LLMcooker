# ollama_utils.py
import requests
import base64

def ask_vision_model(image_path, vision_prompt="Please identify what food or ingredient is in the picture. The answer must be each ingredient, not general answers (e.g. vegetables, fruits, meat)? Just answer the result, no extra nonsense."):
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5vl:7b",
            "prompt": vision_prompt,
            "images": [img_base64],
            "stream": False
        }
    )
    res = response.json()
    return res.get("response", "error: no model")


def ask_recipe_model(ingredients_list):
    prompt = f"I have such foods: {ingredients_list}。Please recommand me 3 easy dishes (only picks foods I provide). And, provide how to cook (plus estimate time at the end). Only respond the steps for each dishes, no redundent text. "
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5vl:7b",  
            "prompt": prompt,
            "stream": False
        }
    )
    res = response.json()
    return res.get("response", "error: no responds")
