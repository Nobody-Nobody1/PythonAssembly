import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

from src.vmexecuter import VmExecuter
try:
    from src.ByteCodeReader import Reader
except ImportError:
    from ByteCodeReader import Reader


class VMGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Bytecode VM Runner")

        # File label
        self.file_label = tk.Label(root, text="No file selected")
        self.file_label.pack(pady=5)

        # Select file button
        self.select_button = tk.Button(root, text="Select Bytecode File", command=self.select_file)
        self.select_button.pack(pady=5)

        # Run button
        self.run_button = tk.Button(root, text="Run Program", command=self.run_vm, state=tk.DISABLED)
        self.run_button.pack(pady=5)

        # Output box
        self.output_box = scrolledtext.ScrolledText(root, width=80, height=20)
        self.output_box.pack(pady=10)

        self.selected_file = None

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Bytecode File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"Selected: {file_path}")
            self.run_button.config(state=tk.NORMAL)

    def run_vm(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected")
            return

        try:
            # Load bytecode from selected file
            bytecode = Reader.read_file_lines(self.selected_file)

            # Force VM to capture output into buffer (no terminal printing)
            vm = VmExecuter(force_buffer=True)

            # Execute program
            vm.execute(bytecode)

            # Show output
            self.output_box.delete("1.0", tk.END)
            output = vm.get_output()

            if output and output.strip():
                self.output_box.insert(tk.END, output)
            else:
                self.output_box.insert(tk.END, "(Program finished with no output)")

        except Exception as e:
            messagebox.showerror("Execution Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    gui = VMGui(root)
    root.mainloop()