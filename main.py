"""
File-Type Validator

Author: [TS / devTobias876]

Copyright: (c) 2026

Version: 1.2.0 (UX Upgrade)

License: MIT

Description: A security-focused offline tool to verify file integrity by
             comparing file extensions with their actual "Magic Bytes" (headers).
             Designed for high-security, air-gapped environments where
             no internet connection is available.

Usage:       Run the script to open the GUI. Select a file to validate.
             The tool will alert if the file signature does not match the extension.
"""

import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

# --- CONFIGURATION ---
CONFIG_FILE = "signatures.json"

def load_signatures(config_path: str = CONFIG_FILE) -> dict:
    # Loads signatures from JSON file. Returns empty dict if failed
    if not os.path.exists(config_path):
        return {}

    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            return {item["extension"]: item["magic"] for item in data["signatures"]}
    except Exception:
        return {}

def get_file_signature(file_path: str) -> str:
    # Reads the first 4 bytes of a file and returns them as a Hex string
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header.hex().upper()
    except Exception:
        return ""

def handle_drop(event):
    # Handles the file drop event
    # Some OS wrap the path in curly braces if it contains spaces
    file_path = event.data.strip('{}')

    if os.path.isfile(file_path):
        process_file(file_path)


def select_and_check_file():
    # Triggered by the manual selection button
    file_path = filedialog.askopenfilename(title="Select File for Analysis")
    if file_path:
        process_file(file_path)


def process_file(file_path):
    #  Refactored logic to handle both button and drag-drop
    status, message, color = validate_file(file_path)
    label_status.config(text=status, fg=color)
    label_details.config(text=message)
    label_path.config(text=f"File: {os.path.basename(file_path)}")


def validate_file(file_path: str) -> tuple:
    # Checks file content against the signature database
    signatures = load_signatures()

    if not signatures:
        return "ERROR", "Signature database not found!", "#dc3545"

    _, extension = os.path.splitext(file_path.lower())
    actual_signature = get_file_signature(file_path)

    if not actual_signature:
        return "ERROR", "File could not be read.", "#dc3545"

    if extension not in signatures:
        return "UNKNOWN", f"Extension {extension} not in database.\nHeader: {actual_signature}", "#6c757d"

    expected_signature = signatures[extension].upper()

    if actual_signature.startswith(expected_signature):
        return "VALID", f"Match confirmed!\nExtension: {extension}\nHeader: {actual_signature}", "#28a745"
    else:
        return "ALARM", f"MISMATCH DETECTED!\nExpected: {expected_signature}\nFound: {actual_signature}", "#dc3545"

# --- GUI ACTIONS ---

def perform_startup_check():
    # Checks if the signature file exists at startup
    if not os.path.exists(CONFIG_FILE):
        label_status.config(text="DB MISSING", fg="#dc3545")
        label_details.config(text=f"Critical Error: '{CONFIG_FILE}' not found.\nApplication restricted.", fg="#dc3545")
        btn_select.config(state="disabled") # Deactivate button
    else:
        label_status.config(text="SYSTEM READY", fg="#28a745")
        label_details.config(text="Database loaded successfully. Please select a file.")

# --- UI SETUP ---
root = TkinterDnD.Tk()
root.title("File-Type Validator v1.2")
root.geometry("500x500")
root.configure(padx=25, pady=25)

# Set GUI Icon
try:
    # Use .ico file
    root.iconbitmap("icon.ico")
except Exception:
    # Fallback: if .ico fails, try the .png directly
    try:
        img = tk.PhotoImage(file='icon.png')
        root.tk.call('wm', 'icon photo', root._w, img)
    except Exception:
        # Ignore if both icons are missing
        pass

# Title
title_label = tk.Label(root, text="File-Type Validator", font=("Arial", 18, "bold"))
title_label.pack(pady=(0, 20))

# Status Section (Changes dynamically)
label_status = tk.Label(root, text="INITIALIZING...", font=("Arial", 22, "bold"), fg="#0056b3")
label_status.pack()

label_details = tk.Label(root, text="Running startup diagnostics...",
                         font=("Arial", 10), justify="center", wraplength=400, pady=10)
label_details.pack()

# Instruction for the user
drop_label = tk.Label(
    root,
    text="--- DROP FILE HERE ---",
    font=("Arial", 10, "bold"),
    fg="#666",
    bg="#eee",
    pady=30,
    relief="groove"
)
drop_label.pack(fill="x", padx=20, pady=10)

# Register the label as a drop target
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind('<<Drop>>', handle_drop)

# Separator
tk.Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", pady=15)

# Action Section
btn_select = tk.Button(root, text="SCAN FILE", command=select_and_check_file,
                       font=("Arial", 12, "bold"), bg="#007bff", fg="white",
                       activebackground="#0056b3", padx=30, pady=12, cursor="hand2")
btn_select.pack(pady=10)

label_path = tk.Label(root, text="Current selection: None", font=("Arial", 9, "italic"), fg="#666")
label_path.pack()

# Footer
footer = tk.Label(root, text="Offline Security Environment | v1.2.0", font=("Arial", 8), fg="gray")
footer.pack(side="bottom", pady=(20, 0))

# Run the startup check after the window is initialized
root.after(500, perform_startup_check)

if __name__ == "__main__":
    root.mainloop()