import yaml
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import webbrowser

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
firefox_path = 'C:\Program Files\Mozilla Firefox\Firefox.exe'
firefox = webbrowser.Mozilla("C:\\Program Files\\Mozilla Firefox\\firefox.exe") 
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

def save_urls(file_path, url_data):
    try:
        with open(file_path, 'w') as file:
            yaml.dump({'urls': url_data}, file)
    except Exception as exc:
        messagebox.showerror("Error", f"Error writing YAML file: {exc}")

def add_url():
    url = simpledialog.askstring("Input", "Enter the URL:")
    if url:
        frame = tk.Frame(listbox_frame)
        frame.pack(fill=tk.X, pady=1)
        
        browser_combobox = ttk.Combobox(frame, values=['Google Chrome', 'Firefox'], width=15, font=text_font)
        browser_combobox.current(0)
        browser_combobox.pack(side=tk.RIGHT, padx=5)

        url_frames.append((frame, url, browser_combobox))
        url_listbox.insert(tk.END, url)

def remove_url():
    selected_index = url_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        url_listbox.delete(index)
        
        frame, _, _ = url_frames.pop(index)
        frame.destroy()
    else:
        messagebox.showwarning("Warning", "Please select a URL to remove.")

def save_config():
    url_data = [{'url': url_label, 'browser': combobox.get()} for _, url_label, combobox in url_frames]
    save_urls(config_file, url_data)
    messagebox.showinfo("Success", "Configuration saved successfully!")

def run_script():
    if not url_frames:
        messagebox.showwarning("Warning", "No URLs to open.")
        return

    for _, url_label, combobox in url_frames:
        url = url_label
        browser = combobox.get()
        if browser == 'Firefox':
            firefox.open_new_tab(url)
        elif browser == 'Google Chrome':
            webbrowser.get(chrome_path).open_new_tab(url)
        

    messagebox.showinfo("Info", "URLs have been opened in your selected browsers.")

root = tk.Tk()
root.title("URL Configurator")

config_file = 'config.yaml'

listbox_frame = tk.Frame(root)
listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

url_listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, width=50, font=("Calibri", 13))
url_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

url_frames = []

url_data = load_urls(config_file)
for data in url_data:
    frame = tk.Frame(listbox_frame)
    frame.pack(fill=tk.X, pady=1)


    browser_combobox = ttk.Combobox(frame, values=['Google Chrome', 'Firefox'], width=15)
    browser_combobox.set(data['browser']) 
    browser_combobox.pack(side=tk.RIGHT, padx=5)

    url_frames.append((frame, data['url'], browser_combobox))
    url_listbox.insert(tk.END, data['url'])

add_button = tk.Button(root, text="Add URL", command=add_url)
add_button.pack(side=tk.LEFT, padx=10, pady=10)

remove_button = tk.Button(root, text="Delete URL", command=remove_url)
remove_button.pack(side=tk.LEFT, padx=10, pady=10)

save_button = tk.Button(root, text="Save URLS", command=save_config)
save_button.pack(side=tk.LEFT, padx=10, pady=10)

run_button = tk.Button(root, text="Open browser", command=run_script)
run_button.pack(side=tk.RIGHT, padx=10, pady=10)
text_font = ('Courier New', '10')
root.option_add('*TCombobox*Listbox.font', text_font)
root.mainloop()
