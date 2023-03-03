from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from distutils import dir_util

from data.loading import Loading
# from data import mpy_cross

import os
import sys
import ampy.pyboard
import threading
import shutil
import mpy_cross


class PutFiles(Toplevel):

    def __init__(self, parent, mpy=False):

        super(PutFiles, self).__init__()

        self.parent = parent
        self.transient(self.parent)

        self.mpy = mpy

        width = 200
        height = 100

        pos_x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (width // 2)
        pos_y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        self.resizable(False, False)
        self.title("Put..." if not self.mpy else "Put MPY...")

        if sys.platform == "win32":
            self.iconbitmap("data/ampy_icon.ico")

        ttk.Button(self, text="Put folder", takefocus=0, command=self.folder).pack(expand=YES, fill=BOTH, padx=5, pady=4)
        ttk.Button(self, text="Put files", takefocus=0, command=self.files).pack(expand=YES, fill=BOTH, padx=5, pady=4)

        self.focus_set()
        self.grab_set()

    @staticmethod
    def convert_to_mpy():
        for root, dirs, files in os.walk("MPY"):
            root = root.replace("\\", "/")
            for file in files:
                if ".py" == file[-3:] and file != "main.py":
                    py_path = root + "/" + file
                    mpy_cross.run(py_path).wait()
                    os.remove(py_path)

    def folder(self):

        def folder_thread():
            try:
                if self.mpy:
                    # Compile python files to mpy.
                    if os.path.exists("MPY"):
                        shutil.rmtree("MPY")

                    dir_util._path_created = {}
                    dir_util.copy_tree(folder, "MPY")

                    self.convert_to_mpy()

                directories = list()
                for root, dirs, files in os.walk(folder if not self.mpy else "MPY"):

                    relative_path = root.replace(folder if not self.mpy else "MPY", "").replace("\\", "/")

                    # Directories with '.' are ignored.
                    if "." in relative_path:
                        continue

                    if relative_path != "" and path[:-1] + relative_path not in directories:
                        self.parent.files.mkdir(path[:-1] + relative_path, exists_okay=True)
                        directories.append(path[:-1] + relative_path)

                    for file in files:
                        with open(root + "/" + file, "rb") as data:
                            self.parent.files.put(path[:-1] + relative_path + "/" + file, data.read())

                if self.mpy:
                    shutil.rmtree("MPY")

                self.parent.refresh()
            except (Exception, ampy.pyboard.PyboardError) as e:
                self.parent.show_error(e)

            loading.close()

        path = self.parent.get_path()

        folder = filedialog.askdirectory()
        if folder != "":
            loading = Loading(self.parent, title="Uploading")
            threading.Thread(target=folder_thread).start()

        self.destroy()

    def files(self):

        def files_thread():
            try:
                if self.mpy:
                    # Compile python files to mpy.
                    if os.path.exists("MPY"):
                        shutil.rmtree("MPY")

                    os.mkdir("MPY")

                    for file in files:
                        shutil.copy2(file.name, "MPY/" + file.name.split("/")[-1])
                    self.convert_to_mpy()

                    for file in os.listdir("MPY"):
                        with open("MPY/" + file, "rb") as data:
                            self.parent.files.put(path + file, data.read())
                else:
                    for file in files:
                        with open(file.name, "rb") as data:
                            self.parent.files.put(path + file.name.split("/")[-1], data.read())

                if self.mpy:
                    shutil.rmtree("MPY")

                self.parent.refresh()
            except (Exception, ampy.pyboard.PyboardError) as e:
                self.parent.show_error(e)

            loading.close()

        path = self.parent.get_path()

        files = filedialog.askopenfiles()
        if files != "":
            loading = Loading(self.parent, title="Uploading")
            threading.Thread(target=files_thread).start()

        self.destroy()
