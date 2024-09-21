import os
import yaml
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
import webbrowser

default_browsers = {
    'Google Chrome': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s',
    'Firefox': 'C:/Program Files/Mozilla Firefox/firefox.exe'
}

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            urls = config.get('urls', [])
            browsers = config.get('browsers', default_browsers)

            return urls, browsers
    except FileNotFoundError:
        return [], default_browsers
    except yaml.YAMLError as exc:
        messagebox.showerror("Error", f"Error reading YAML file: {exc}")
        return [], default_browsers

def save_urls(file_path, url_data):
    try:
        with open(file_path, 'w') as file:
            yaml.dump(url_data, file)
    except Exception as exc:
        messagebox.showerror("Error", f"Error writing YAML file: {exc}")

def configure_browser_paths():
    for browser in browsers.keys():
        current_path = browsers[browser]
        new_path = filedialog.askopenfilename(initialdir=os.path.dirname(current_path), title=f"Select {browser} executable")
        
        if new_path:
            browsers[browser] = new_path
            messagebox.showinfo("Success", f"{browser} path updated successfully!")

    save_browser_paths()

def save_browser_paths():
    config_data = {'browsers': browsers, 'urls': [{'url': url, 'browser': combobox.get()} for _, url, combobox, _ in url_frames]}
    save_urls(config_file, config_data)

def ensure_browser_paths():
    for browser, path in browsers.items():
        if not os.path.exists(path):
            result = messagebox.askyesno("Path Not Found", f"Path for {browser} not found. Would you like to set it now?")
            if result:
                configure_browser_paths()

def add_url():
    url = simpledialog.askstring("Input", "Enter the URL:")
    if url:
        frame = tk.Frame(listbox_frame)
        frame.pack(fill=tk.X, pady=1)

        ensure_browser_paths()

        browser_combobox = ttk.Combobox(frame, values=list(browsers.keys()), width=15, font=text_font)
        browser_combobox.pack(side=tk.RIGHT, padx=5)

        browser_combobox.current(0)
        
        url_frames.append((frame, url, browser_combobox))
        url_listbox.insert(tk.END, url)

def remove_url():
    selected_index = url_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        url_listbox.delete(index)
        
        frame, _, _, _ = url_frames.pop(index)
        frame.destroy()
    else:
        messagebox.showwarning("Warning", "Please select a URL to remove.")

def save_config():
    url_data = [{'url': url, 'browser': combobox.get()} for _, url, combobox in url_frames]
    config_data = {'urls': url_data, 'browsers': browsers}
    save_urls(config_file, config_data)
    messagebox.showinfo("Success", "Configuration saved successfully!")

def run_script():
    if not url_frames:
        messagebox.showwarning("Warning", "No URLs to open.")
        return

    for _, url_label, combobox in url_frames:
        url = url_label
        browser = combobox.get()
        browser_path = browsers.get(browser, "")
        
        if browser == 'Firefox':
            webbrowser.get(f'"{browser_path}" %s').open_new_tab(url)
        elif browser == 'Google Chrome':
            webbrowser.get(f'"{browser_path}" %s').open_new_tab(url)


root = tk.Tk()
root.title("URL Configurator")

config_file = 'config.yaml'

url_data, browsers = load_config(config_file)

listbox_frame = tk.Frame(root)
listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

url_listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, width=50, font=("Calibri", 13))
url_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

url_frames = []

for data in url_data:
    frame = tk.Frame(listbox_frame)
    frame.pack(fill=tk.X, pady=1)

    browser_combobox = ttk.Combobox(frame, values=list(browsers.keys()), width=15)
    browser_combobox.set(data['browser']) 
    browser_combobox.pack(side=tk.RIGHT, padx=5)

    url_frames.append((frame, data['url'], browser_combobox))
    url_listbox.insert(tk.END, data['url'])

add_button = tk.Button(root, text="Add URL", command=add_url)
add_button.pack(side=tk.LEFT, padx=10, pady=10)

remove_button = tk.Button(root, text="Delete URL", command=remove_url)
remove_button.pack(side=tk.LEFT, padx=10, pady=10)

save_button = tk.Button(root, text="Save URLs", command=save_config)
save_button.pack(side=tk.LEFT, padx=10, pady=10)

run_button = tk.Button(root, text="Open Browser", command=run_script)
run_button.pack(side=tk.RIGHT, padx=10, pady=10)

config_button = tk.Button(root, text="Configure Browser Paths", command=configure_browser_paths)
config_button.pack(side=tk.LEFT, padx=10, pady=10)

text_font = ('Calibri', '10')
root.option_add('*TCombobox*Listbox.font', text_font)

root.mainloop()
