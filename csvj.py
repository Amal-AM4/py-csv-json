import os
import tkinter as tk
from tkinter import filedialog, simpledialog
import pandas as pd
import datetime

class CSVToJSONConverter:
    def __init__(self, master):
        self.master = master
        master.title("CSV to JSON Converter")

        # Create the main widgets
        self.label = tk.Label(master, text="Select a CSV file:")
        self.label.pack(pady=10)

        self.file_path_var = tk.StringVar()
        self.file_path_entry = tk.Entry(master, textvariable=self.file_path_var, width=50)
        self.file_path_entry.pack(pady=10)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=10)

        self.convert_button = tk.Button(master, text="Convert to JSON", command=self.convert_to_json)
        self.convert_button.pack(pady=10)

        self.download_button = tk.Button(master, text="Download JSON", command=self.download_json)
        self.download_button.pack(pady=10)

        self.preview_label = tk.Label(master, text="JSON Preview:")
        self.preview_label.pack(pady=10)

        self.preview_text = tk.Text(master, height=10, width=80)
        self.preview_text.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.file_path_var.set(file_path)

    def convert_to_json(self):
        file_path = self.file_path_var.get()
        if file_path:
            try:
                data = pd.read_csv(file_path)
                self.data_json = data.to_json(orient='records', indent=2)
                self.preview_text.delete("1.0", tk.END)
                self.preview_text.insert(tk.END, self.data_json[:500])
            except Exception as e:
                simpledialog.messagebox.showerror("Error", str(e))
        else:
            simpledialog.messagebox.showerror("Error", "Please select a CSV file.")

    def download_json(self):
        if hasattr(self, 'data_json'):
            file_name = os.path.splitext(os.path.basename(self.file_path_var.get()))[0]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = filedialog.asksaveasfilename(
                initialfile=f"{file_name}_{timestamp}.json",
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json")]
            )
            if save_path:
                with open(save_path, 'w') as f:
                    f.write(self.data_json)
                simpledialog.messagebox.showinfo("Download Complete", f"JSON file saved to: {save_path}")
        else:
            simpledialog.messagebox.showerror("Error", "Please convert a CSV file to JSON first.")

root = tk.Tk()
app = CSVToJSONConverter(root)
root.mainloop()