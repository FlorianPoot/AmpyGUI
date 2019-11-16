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

        self.geometry("200x100" + "+" + str(int(self.parent.geometry().split("+")[1]) + 225)
                      + "+" + str(int(self.parent.geometry().split("+")[2]) + 65))

        self.resizable(False, False)
        self.title("Put...")
        self.iconbitmap("AmpyGUI_Data/AmpyGUI_icon.ico")

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

                    if relative_path != "" and path[:-1] + relative_path not in directories:
                        self.parent.files.mkdir(path[:-1] + relative_path)
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
