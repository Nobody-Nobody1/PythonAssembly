import tkinter as tk
from tkinter import messagebox, messagebox as messagebox
import subprocess
import sys
import os
import shutil
import tempfile

def run_file():

    temp_file_path = "VmExecuter.py"
    #open file and display its contents``
    
    if not temp_file_path:
        return  # User cancelled

    if not os.path.isfile(temp_file_path):
        messagebox.showerror("Error", "Selected file does not exist.")
        return

    try:
        # Run the file and capture output
        process = subprocess.Popen(
            [sys.executable, temp_file_path],  # Runs with current Python interpreter
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        # Clear previous output
        output_text.delete("1.0", tk.END)

        # Display stdout
        if stdout:
            output_text.insert(tk.END, "=== Output ===\n" + stdout + "\n")

        # Display stderr (if any)
        if stderr:
            output_text.insert(tk.END, "=== Errors ===\n" + stderr + "\n")

    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

def get_temp_copy(filename):
    # Returns the path to a temporary copy of a bundled file.
    # Determine base path (inside _MEIPASS when frozen)
    #todo: make 2 versions of this function, one for when the file is bundled and one for when it is not, and use the appropriate one based on the environment

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Temporary extraction folder for PyInstaller
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    source_path = os.path.join(base_path, filename)

    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Bundled file '{filename}' not found.")

    # Create a temp copy
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, filename)
    shutil.copy2(source_path, temp_path)

    return temp_path

if __name__ == "__main__":
    try:
        temp_file_path = get_temp_copy("VmExecuter.py")
        print(f"Temporary copy created at: {temp_file_path}")
        # need to add excution code here so temp copy is always run
            
    except Exception as e:
        print(f"Error: {e}")

def show_file():
   file = 'ByteCode.txt'
   if file:
       with open(file, 'r', encoding='utf-8') as file:
           content = file.read()
           output_text.delete(1.0, tk.END) # Clear previous content
           output_text.insert(tk.END, content) # Insert new content

def save_file():
    current_file_path = 'ByteCode.txt'
        #save directly to the file
    with open(current_file_path, "w", encoding="utf-8") as file:
        file.write(output_text.get("1.0", tk.END).rstrip())
    messagebox.showinfo("Saved", f"Changes saved to:\n{os.path.basename(current_file_path)}")

# Create main window
root = tk.Tk()
root.title("Code IDE")
root.geometry("600x400")
root.wm_attributes("-topmost", True)

# Create the menu bar
menu_bar = tk.Menu(root)

# ----- Menu -----
file_menu = tk.Menu(menu_bar, tearoff=0)  # tearoff=0 removes dashed line
file_menu.add_command(label="Run File VmExecuter.py", command=run_file)
file_menu.add_command(label="Edit ByteCode.txt", command=show_file)
file_menu.add_command(label="Save Changes", command=save_file)
file_menu.add_separator()  # Adds a horizontal line
file_menu.add_command(label="Exit", command=root.destroy)
menu_bar.add_cascade(label="File", menu=file_menu)

# Text widget to display output
output_text = tk.Text(root, wrap="word", height=20, width=70)
output_text.pack(padx=10, pady=10, fill=None, expand=False)

# Scrollbar for output
scrollbar = tk.Scrollbar(root, command=output_text.yview)
scrollbar.pack(side="right", fill="y")
output_text.config(yscrollcommand=scrollbar.set)

# Attach the menu bar to the window
root.config(menu=menu_bar)

# Run the application
root.mainloop()