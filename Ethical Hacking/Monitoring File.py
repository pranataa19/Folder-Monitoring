import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import winsound

class EventHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_created(self, event):
        self.app.show_message("File created: " + event.src_path)
        self.app.play_alert_sound()
        self.app.show_notification("File created", event.src_path)

    def on_deleted(self, event):
        self.app.show_message("File deleted: " + event.src_path)
        self.app.play_alert_sound()
        self.app.show_notification("File deleted", event.src_path)

    def on_modified(self, event):
        self.app.show_message("File modified: " + event.src_path)
        self.app.play_alert_sound()
        self.app.show_notification("File modified", event.src_path)

    def on_moved(self, event):
        self.app.show_message("File moved: " + event.src_path + " to " + event.dest_path)
        self.app.play_alert_sound()
        self.app.show_notification("File moved", event.src_path + " to " + event.dest_path)

class FolderMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Monitor App")
        self.folder_to_monitor = ""
        self.observer = None
        self.is_monitoring = False

        # Create UI components
        self.label_folder = tk.Label(root, text="Folder to Monitor:")
        self.label_folder.pack()

        self.entry_folder = tk.Entry(root, width=50)
        self.entry_folder.pack()

        self.btn_browse = tk.Button(root, text="Browse", command=self.browse_folder)
        self.btn_browse.pack()

        self.btn_start = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.btn_start.pack()

        self.btn_stop = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.btn_stop.pack()

        # Watchdog event handler
        self.event_handler = EventHandler(self)

    def browse_folder(self):
        self.folder_to_monitor = filedialog.askdirectory()
        self.entry_folder.delete(0, tk.END)
        self.entry_folder.insert(tk.END, self.folder_to_monitor)

    def start_monitoring(self):
        if not self.folder_to_monitor:
            messagebox.showerror("Error", "Please select a folder to monitor.")
            return

        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.folder_to_monitor, recursive=True)
        self.observer.start()

        self.is_monitoring = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

    def stop_monitoring(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()

        self.is_monitoring = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

    def show_message(self, message):
        print(message)

    def play_alert_sound(self):
        winsound.Beep(1000, 100)  # Play a beep sound

    def show_notification(self, action, file_path):
        message = f"{action}:\n{file_path}"
        messagebox.showinfo("Folder Monitor", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderMonitorApp(root)
    root.mainloop()
