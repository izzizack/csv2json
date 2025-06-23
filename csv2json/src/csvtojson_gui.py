import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import json
import os


class CsvToJsonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV to JSON Converter")
        self.csv_data = []
        self.headers = []
        self.entries = []
        self.file_path = None
        self.row_vars = []

        # File selection
        self.select_btn = tk.Button(root, text="Select CSV File", command=self.load_csv)
        self.select_btn.pack(pady=10)
        
        # Frame for dynamic entries
        self.entries_frame = tk.Frame(root)
        self.entries_frame.pack(fill=tk.BOTH, expand=True)

        # Create the JSON output window as a separate window
        self.json_window = tk.Toplevel(self.root)
        self.json_window.title("Live JSON Output")
        self.json_text = tk.Text(self.json_window, height=15, width=80)
        self.json_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")],
            title="Select a CSV file"
        )
        if not file_path:
            return
        self.file_path = file_path
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self.headers = reader.fieldnames
                self.csv_data = list(reader)
            self.display_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def display_entries(self):
        # Clear previous widgets
        for widget in self.entries_frame.winfo_children():
            widget.destroy()
        self.entries = []
        self.row_vars = []

        if not self.headers:
            return

        # Show headers
        for idx, header in enumerate(self.headers):
            tk.Label(self.entries_frame, text=header, relief=tk.RIDGE, width=15).grid(row=0, column=idx, padx=2, pady=2)

        # Show all rows for editing
        for row_idx, row in enumerate(self.csv_data):
            row_var = []
            for col_idx, header in enumerate(self.headers):
                var = tk.StringVar(value=row.get(header, ""))
                entry = tk.Entry(self.entries_frame, textvariable=var, width=15)
                entry.grid(row=row_idx+1, column=col_idx, padx=2, pady=2)
                var.trace_add("write", self.live_update)
                row_var.append(var)
            self.row_vars.append(row_var)

        # Add a button to add more rows
        add_row_btn = tk.Button(self.entries_frame, text="Add Row", command=self.add_row)
        add_row_btn.grid(row=len(self.csv_data)+1, column=0, columnspan=len(self.headers), pady=5)

        self.live_update()

    def add_row(self):
        row_idx = len(self.row_vars)
        row_var = []
        for col_idx, header in enumerate(self.headers):
            var = tk.StringVar(value="")
            entry = tk.Entry(self.entries_frame, textvariable=var, width=15)
            entry.grid(row=row_idx+1, column=col_idx, padx=2, pady=2)
            var.trace_add("write", self.live_update)
            row_var.append(var)
        self.row_vars.append(row_var)
        self.live_update()

    def live_update(self, *args):
        # Build data from entry fields
        data = []
        for row in self.row_vars:
            row_dict = {header: var.get() for header, var in zip(self.headers, row)}
            # Only add non-empty rows
            if any(v for v in row_dict.values()):
                data.append(row_dict)
        # Update JSON output in the separate window
        self.json_text.delete(1.0, tk.END)
        self.json_text.insert(tk.END, json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    root = tk.Tk()
    app = CsvToJsonGUI(root)
    root.mainloop()
