import tkinter as tk
from tkinter import ttk
import os
from threading import Thread
from flask import Flask, send_from_directory
import webbrowser

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Server Control Panel")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.server = Flask(__name__)
        self.server_thread = None
        self.server_running = False
        
        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Server control section
        control_frame = ttk.LabelFrame(main_frame, text="Server Control", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Server", command=self.start_server)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.open_browser_btn = ttk.Button(control_frame, text="Open in Browser", command=self.open_browser)
        self.open_browser_btn.pack(side=tk.LEFT, padx=5)
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Server Status", padding="10")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Server is stopped")
        self.status_label.pack()
        
        # Files section
        files_frame = ttk.LabelFrame(main_frame, text="Available Files", padding="10")
        files_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create treeview for files
        self.files_tree = ttk.Treeview(files_frame, columns=("File", "Size", "Type"), show="headings")
        self.files_tree.heading("File", text="Filename")
        self.files_tree.heading("Size", text="Size (bytes)")
        self.files_tree.heading("Type", text="File Type")
        self.files_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.files_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_tree.configure(yscrollcommand=scrollbar.set)
        
        self.update_file_list()
        
    def update_file_list(self):
        # Clear existing items
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        
        # Add files from static folder
        static_path = os.path.join(os.path.dirname(__file__), "static")
        if os.path.exists(static_path):
            print(f"Scanning directory: {static_path}")
            for file in os.listdir(static_path):
                file_path = os.path.join(static_path, file)
                size = str(os.path.getsize(file_path))  # Convert size to string
                file_type = os.path.splitext(file)[1] or "No extension"
                print(f"Found file: {file} | Size: {size} | Type: {file_type}")
                self.files_tree.insert("", tk.END, values=(file, size, file_type))
        else:
            print(f"Static directory not found at: {static_path}")
            os.makedirs(static_path)
            print("Created static directory")

    
    def start_server(self):
        if not self.server_running:
            self.server_thread = Thread(target=self.run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            self.server_running = True
            self.status_label.config(text="Server is running on http://localhost:3000")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            print("RUNNING BABE")
            self.update_file_list()
    
    def stop_server(self):
        if self.server_running:
            # Implement server shutdown logic here
            self.server_running = False
            self.status_label.config(text="Server is stopped")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def open_browser(self):
        if self.server_running:
            webbrowser.open('http://localhost:3000')
    
    def run_server(self):
        @self.server.route('/')
        def hello_world():
            return 'Hello, World!'

        @self.server.route('/<path:filename>')
        def serve_file(filename):
            return send_from_directory('static', filename, as_attachment=True)
            
        self.server.run(host='0.0.0.0', port=3000, use_reloader=False)

if __name__ == '__main__':
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()
