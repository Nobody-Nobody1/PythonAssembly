import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

from src.vmexecuter import VmExecuter
try:
    from src.ByteCodeReader import Reader
except ImportError:
    from ByteCodeReader import Reader


class BytecodeIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("PythonAssembly IDE")

        self.current_file = None

        # ---------------- MENU BAR ----------------
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save As", command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        runmenu = tk.Menu(menubar, tearoff=0)
        runmenu.add_command(label="Run", command=self.run_program)
        menubar.add_cascade(label="Run", menu=runmenu)

        root.config(menu=menubar)

        # ---------------- EDITOR ----------------
        self.editor = scrolledtext.ScrolledText(root, width=90, height=25, undo=True)
        self.editor.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # ---------------- OUTPUT CONSOLE ----------------
        tk.Label(root, text="Output:").pack(anchor="w", padx=10)
        self.output_box = scrolledtext.ScrolledText(root, width=90, height=10, state=tk.DISABLED)
        self.output_box.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=False)

        # ---------------- STATUS BAR ----------------
        self.status = tk.Label(root, text="Ready", anchor="w")
        self.status.pack(fill=tk.X)

        # ---------------- KEYBOARD SHORTCUTS ----------------
        root.bind("<Control-s>", lambda e: self.save_file())
        root.bind("<Control-o>", lambda e: self.open_file())
        root.bind("<Control-n>", lambda e: self.new_file())
        root.bind("<F5>", lambda e: self.run_program())

    # ---------------- FILE OPERATIONS ----------------

    def new_file(self):
        self.editor.delete("1.0", tk.END)
        self.current_file = None
        self.status.config(text="New file")

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Open Bytecode File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not path:
            return

        try:
            with open(path, "r") as f:
                content = f.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert(tk.END, content)
            self.current_file = path
            self.status.config(text=f"Opened {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_file(self):
        if not self.current_file:
            return self.save_as()

        try:
            with open(self.current_file, "w") as f:
                f.write(self.editor.get("1.0", tk.END))
            self.status.config(text=f"Saved {self.current_file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_as(self):
        path = filedialog.asksaveasfilename(
            title="Save Bytecode File As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not path:
            return

        try:
            with open(path, "w") as f:
                f.write(self.editor.get("1.0", tk.END))
            self.current_file = path
            self.status.config(text=f"Saved as {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- RUN PROGRAM ----------------

    def run_program(self):
        try:
            # Read editor content as bytecode lines
            text = self.editor.get("1.0", tk.END).strip()
            if not text:
                messagebox.showinfo("Info", "Editor is empty")
                return

            bytecode = [line.split() for line in text.splitlines()]

            vm = VmExecuter(force_buffer=True)
            vm.execute(bytecode)

            output = vm.get_output()

            self.output_box.config(state=tk.NORMAL)
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, output if output else "(No output)")
            self.output_box.config(state=tk.DISABLED)

            self.status.config(text="Program executed")

        except Exception as e:
            messagebox.showerror("Execution Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    ide = BytecodeIDE(root)
    root.mainloop()