"""
Password Generator with Tkinter GUI
Generates random passwords with customizable options
Includes strength indicator and copy to clipboard
"""

import random
import string
import tkinter as tk
from tkinter import messagebox


def generate_password():
    """Generate a random password based on selected options"""
    length = int(slider_length.get())
    characters = ""

    if var_lowercase.get():
        characters += string.ascii_lowercase
    if var_uppercase.get():
        characters += string.ascii_uppercase
    if var_numbers.get():
        characters += string.digits
    if var_symbols.get():
        characters += string.punctuation

    if not characters:
        messagebox.showwarning("Warning", "Please select at least one character type")
        return

    password = "".join(random.choice(characters) for _ in range(length))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    update_strength(password)


def update_strength(password):
    """Calculate and display password strength"""
    score = 0
    length = len(password)

    # Length scoring
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    # Character variety scoring
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    variety = sum([has_lower, has_upper, has_digit, has_symbol])
    score += variety

    # Display strength
    if score >= 5:
        strength_text = "Strong"
        strength_color = "#2e7d32"
    elif score >= 3:
        strength_text = "Medium"
        strength_color = "#f57c00"
    else:
        strength_text = "Weak"
        strength_color = "#c62828"

    label_strength.config(text=f"Strength: {strength_text}", fg=strength_color)


def copy_to_clipboard():
    """Copy the generated password to clipboard"""
    password = entry_password.get()
    if not password:
        messagebox.showwarning("Warning", "Generate a password first")
        return
    root.clipboard_clear()
    root.clipboard_append(password)
    label_copied.config(text="Copied!")
    root.after(2000, lambda: label_copied.config(text=""))


def update_length_label(value):
    """Update the length display when slider moves"""
    label_length_val.config(text=f"Length: {int(float(value))}")


# Create main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x380")
root.resizable(False, False)

# Title
label_title = tk.Label(root, text="Password Generator", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

# Password display field
frame_password = tk.Frame(root)
frame_password.pack(pady=5, padx=20, fill=tk.X)

entry_password = tk.Entry(frame_password, font=("Courier", 13), justify="center")
entry_password.pack(side=tk.LEFT, fill=tk.X, expand=True)

btn_copy = tk.Button(frame_password, text="Copy", command=copy_to_clipboard, width=6)
btn_copy.pack(side=tk.RIGHT, padx=(5, 0))

# Copied confirmation label
label_copied = tk.Label(root, text="", font=("Arial", 9), fg="#2e7d32")
label_copied.pack()

# Length slider
frame_length = tk.Frame(root)
frame_length.pack(pady=5, padx=20, fill=tk.X)

label_length_val = tk.Label(frame_length, text="Length: 16", font=("Arial", 11))
label_length_val.pack()

slider_length = tk.Scale(
    frame_length, from_=8, to=32,
    orient=tk.HORIZONTAL, command=update_length_label,
    showvalue=False, length=300
)
slider_length.set(16)
slider_length.pack()

# Character type checkboxes
frame_options = tk.Frame(root)
frame_options.pack(pady=10)

var_lowercase = tk.BooleanVar(value=True)
var_uppercase = tk.BooleanVar(value=True)
var_numbers = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

cb_lower = tk.Checkbutton(frame_options, text="Lowercase (a-z)", variable=var_lowercase)
cb_lower.grid(row=0, column=0, sticky="w", padx=10)

cb_upper = tk.Checkbutton(frame_options, text="Uppercase (A-Z)", variable=var_uppercase)
cb_upper.grid(row=0, column=1, sticky="w", padx=10)

cb_numbers = tk.Checkbutton(frame_options, text="Numbers (0-9)", variable=var_numbers)
cb_numbers.grid(row=1, column=0, sticky="w", padx=10)

cb_symbols = tk.Checkbutton(frame_options, text="Symbols (!@#$)", variable=var_symbols)
cb_symbols.grid(row=1, column=1, sticky="w", padx=10)

# Generate button
btn_generate = tk.Button(
    root, text="Generate Password",
    command=generate_password,
    font=("Arial", 12), width=20
)
btn_generate.pack(pady=15)

# Strength indicator
label_strength = tk.Label(root, text="Strength: -", font=("Arial", 11))
label_strength.pack()

# Start the app
root.mainloop()
