from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from AmpyGUI_Data.Loading import Loading

import os
import ampy.pyboard
import threading


class PutFiles(Toplevel):

    def __init__(self, parent):

        super(PutFiles, self).__init__()

        self.parent = parent
        self.transient(self.parent)

        width = 200
        height = 100

        pos_x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (width // 2)
        pos_y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (height // 2) - 10

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        self.resizable(False, False)
        self.title("Put...")

        if sys.platform == "win32":
            self.iconbitmap("AmpyGUI_Data/AmpyGUI_icon.ico")
        elif sys.platform == "linux":
            self.icon = Image("photo", file="AmpyGUI_Data/AmpyGUI_icon.png")
            self.tk.call("wm", "iconphoto", self._w, self.icon)

        ttk.Button(self, text="Put folder", takefocus=0, command=self.folder).pack(expand=YES, fill=BOTH, padx=5, pady=4)
        ttk.Button(self, text="Put files", takefocus=0, command=self.files).pack(expand=YES, fill=BOTH, padx=5, pady=4)

        self.focus_set()
        self.grab_set()

    def folder(self):

        def folder_thread():
            try:
                directories = list()
                for root, dirs, files in os.walk(folder):

                    relative_path = root.replace(folder, "").replace("\\", "/")

                    # Directories with '.' are ignored.
                    if "." in relative_path:
                        continue

                    if relative_path != "" and path[:-1] + relative_path not in directories:
                        self.parent.files.mkdir(path[:-1] + relative_path, exists_okay=True)
                        directories.append(path[:-1] + relative_path)

                    for file in files:
                        with open(root + "/" + file, "rb") as data:
                            self.parent.files.put(path[:-1] + relative_path + "/" + file, data.read())

                self.parent.refresh()
                loading.close()
            except (Exception, ampy.pyboard.PyboardError) as e:
                self.parent.show_error(e)

        path = self.parent.get_path()

        folder = filedialog.askdirectory()
        if folder != "":
            loading = Loading(self.parent, title="Uploading")
            threading.Thread(target=folder_thread).start()

        self.destroy()

    def files(self):

        def files_thread():
            try:
                for file in files:
                    with open(file.name, "rb") as data:
                        self.parent.files.put(path + file.name.split("/")[-1], data.read())

                self.parent.refresh()
                loading.close()
            except (Exception, ampy.pyboard.PyboardError) as e:
                self.parent.show_error(e)

        path = self.parent.get_path()

        files = filedialog.askopenfiles()
        if files != "":
            loading = Loading(self.parent, title="Uploading")
            threading.Thread(target=files_thread).start()

        self.destroy()
