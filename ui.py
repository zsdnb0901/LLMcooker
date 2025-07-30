# ui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

from ollama_utils import ask_vision_model, ask_recipe_model

selected_image_path = None

def run_interface():
    def upload_image():
        global selected_image_path
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            selected_image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((250, 250))
            img_tk = ImageTk.PhotoImage(img)
            image_label.configure(image=img_tk)
            image_label.image = img_tk
            #image_path_label.config(text=os.path.basename(file_path))
            ingredients_text.delete(1.0, tk.END)
            recipe_text.delete(1.0, tk.END)

    def run_vision():
        if not selected_image_path:
            messagebox.showwarning("no image", "please load a image first")
            return
        ingredients_text.delete(1.0, tk.END)
        ingredients_text.insert(tk.END, "processing... please wait...\n")
        window.update()

        result = ask_vision_model(selected_image_path)
        ingredients_text.delete(1.0, tk.END)
        ingredients_text.insert(tk.END, result)

    def run_recipe():
        ingredients = ingredients_text.get("1.0", tk.END).strip()
        if not ingredients:
            messagebox.showwarning("no ingredient", "process an image first")
            return
        recipe_text.delete(1.0, tk.END)
        recipe_text.insert(tk.END, "processing... plaese wait...\n")
        window.update()

        recipe_result = ask_recipe_model(ingredients)
        recipe_text.delete(1.0, tk.END)
        recipe_text.insert(tk.END, recipe_result)

    # layout
    window = tk.Tk()
    window.title("Cooker")
    window.geometry("1000x600")
    window.configure(bg="white")

    # intro text
    intro_label = tk.Label(window, text="1. Upload an image with all the food you have.", font=("Arial", 12), anchor='w', bg='white')
    intro_label.place(x=20, y=30)

    intro_label = tk.Label(window, text="2. Click 'analyze' for analysis food types.", font=("Arial", 12), anchor='w', bg='white')
    intro_label.place(x=20, y=80)

    intro_label = tk.Label(window, text="3. Click 'recommand' for possible dishes you can do", font=("Arial", 12), anchor='w', bg='white')
    intro_label.place(x=20, y=130)

    # upload an image
    upload_button = tk.Button(window, text="Click to upload an image", command=upload_image)
    upload_button.place(x=20, y=200)

    # show image
    image_label = tk.Label(window, bg="white", width=250, height=250)
    image_label.place(x=20, y=280)

    # image label (no need here)
    image_path_label = tk.Label(window, text="", bg="white")
    image_path_label.place(x=50, y=340)

    # analyze
    vision_button = tk.Button(window, text="analyze", command=run_vision)
    vision_button.place(x=280, y=200)

    # food box
    ingredients_text = tk.Text(window, height=12, width=35)
    ingredients_text.place(x=280, y=280)

    # recommand
    recipe_button = tk.Button(window, text="recommand", command=run_recipe)
    recipe_button.place(x=520, y=30)

    # dishes
    recipe_text = tk.Text(window, 
    height=30, width=50)
    recipe_text.place(x=600, y=30)

    window.mainloop()
