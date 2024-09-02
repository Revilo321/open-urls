import yaml
import tkinter as tk
from tkinter import messagebox, simpledialog
import webbrowser

def load_urls(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            return config.get('urls', [])
    except FileNotFoundError:
        return []
    except yaml.YAMLError as exc:
        messagebox.showerror("Error", f"Error reading YAML file: {exc}")
        return []

def save_urls(file_path, urls):
    try:
        with open(file_path, 'w') as file:
            yaml.dump({'urls': urls}, file)
    except Exception as exc:
        messagebox.showerror("Error", f"Error writing YAML file: {exc}")

def add_url():
    url = simpledialog.askstring("Input", "Indtast URL")
    if url:
        listbox.insert(tk.END, url)

def remove_url():
    selected = listbox.curselection()
    if selected:
        listbox.delete(selected)

def save_config():
    urls = list(listbox.get(0, tk.END))
    save_urls(config_file, urls)
    messagebox.showinfo("Success", "Konfigurationen er blevet gemt!")

def run_script():
    urls = list(listbox.get(0, tk.END))
    if not urls:
        messagebox.showwarning("Warning", "Tilføj URL før du prøver at åbne")
        return

    for url in urls:
        webbrowser.open_new_tab(url)

root = tk.Tk()
root.title("URL Config")

config_file = 'config.yaml'

listbox = tk.Listbox(root, selectmode=tk.SINGLE)
listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

urls = load_urls(config_file)
for url in urls:
    listbox.insert(tk.END, url)

add_button = tk.Button(root, text="Tilføj URL", command=add_url)
add_button.pack(side=tk.LEFT, padx=10, pady=10)

remove_button = tk.Button(root, text="Slet URL", command=remove_url)
remove_button.pack(side=tk.LEFT, padx=10, pady=10)

save_button = tk.Button(root, text="Gem Konfigurationen", command=save_config)
save_button.pack(side=tk.LEFT, padx=10, pady=10)

run_button = tk.Button(root, text="Opsæt browser", command=run_script)
run_button.pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()
