import os
import tkinter as tk
from tkinter import filedialog, messagebox


# --- LOGIK-TEIL (BACKEND) ---

def get_file_signature(file_path):
    """Liest die ersten 4 Bytes einer Datei und gibt sie als Hex-String zurück."""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header.hex().upper()
    except Exception as e:
        return None


def validate_file(file_path):
    """
    Prüft, ob die Magic Bytes zur Dateiendung passen.
    Erweiterbar über das Dictionary 'signatures'.
    """
    # Datenbank der Magic Bytes (Hex-Repräsentation)
    # Diese könnte später in eine signatures.json ausgelagert werden
    signatures = {
        ".pdf": "25504446",
        ".png": "89504E47",
        ".jpg": "FFD8FFE0",
        ".jpeg": "FFD8FFE0",
        ".exe": "4D5A",
        ".zip": "504B0304",
        ".docx": "504B0304"  # Word nutzt oft das ZIP-Format als Container
    }

    _, extension = os.path.splitext(file_path.lower())
    actual_signature = get_file_signature(file_path)

    if actual_signature is None:
        return "FEHLER", "Datei konnte nicht gelesen werden.", "orange"

    if extension not in signatures:
        return "INFO", f"Endung {extension} unbekannt.\nHeader: {actual_signature}", "gray"

    expected_signature = signatures[extension]

    # Vergleich: Startet der Datei-Header mit der erwarteten Signatur?
    if actual_signature.startswith(expected_signature):
        return "OK", f"Validierung erfolgreich!\nTyp: {extension}\nHeader: {actual_signature}", "green"
    else:
        return "ALARM", f"Manipulation? Endung ist {extension},\naber Header ist {actual_signature}!", "red"


# --- GUI-TEIL (FRONTEND) ---

def select_and_check_file():
    """Wird aufgerufen, wenn der Button geklickt wird."""
    file_path = filedialog.askopenfilename(title="Datei zur Sicherheitsprüfung auswählen")

    if file_path:
        status, message, color = validate_file(file_path)

        # UI-Elemente aktualisieren
        label_status.config(text=status, fg=color)
        label_details.config(text=message)
        label_path.config(text=f"Datei: {os.path.basename(file_path)}")


# Hauptfenster Setup
root = tk.Tk()
root.title("Sicherheits-Check: File-Type Validator")
root.geometry("500x350")
root.configure(padx=20, pady=20)

# UI Komponenten
title_label = tk.Label(root, text="Air-Gap File Validator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

btn_select = tk.Button(root, text="Datei auswählen & prüfen", command=select_and_check_file,
                       font=("Arial", 12), bg="#d1d1d1", padx=10, pady=5)
btn_select.pack(pady=20)

label_path = tk.Label(root, text="Keine Datei ausgewählt", font=("Arial", 10, "italic"))
label_path.pack()

label_status = tk.Label(root, text="BEREIT", font=("Arial", 20, "bold"), fg="blue")
label_status.pack(pady=10)

label_details = tk.Label(root, text="Warten auf Eingabe...", font=("Arial", 10), justify="center")
label_details.pack(pady=10)

# Fußzeile für professionelles Aussehen
footer = tk.Label(root, text="Offline Security Tool | v1.0", font=("Arial", 8), fg="gray")
footer.pack(side="bottom")

if __name__ == "__main__":
    root.mainloop()