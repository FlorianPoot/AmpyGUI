from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import sys


class MkDir(Toplevel):

    def __init__(self, parent):

        super(MkDir, self).__init__()

        self.parent = parent
        self.transient(self.parent)

        width = 300
        height = 50

        pos_x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (width // 2)
        pos_y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        self.resizable(False, False)
        self.title("MkDir...")

        if sys.platform == "win32":
            self.iconbitmap("data/ampy_icon.ico")

        self.name = StringVar()

        entry = ttk.Entry(self, textvariable=self.name, font="Arial 12", width=25)
        entry.pack(expand=YES, fill=BOTH, side="left", padx=5, pady=10)

        ttk.Button(self, text="Ok", takefocus=0, command=self.mk_dir).pack(expand=YES, fill=BOTH, side="right", padx=5, pady=10)

        self.focus_set()
        self.grab_set()

        entry.focus()

    def mk_dir(self):

        """Make a directory on the board."""

        invalid_characters = "\\/:*?\"<>|."

        if self.name.get() != "" and not any((c in invalid_characters) for c in self.name.get()):
            if "." in self.parent.get_path():
                path = "/" + "/".join(self.parent.get_path().split("/")[:-2]) + self.name.get()
            else:
                path = self.parent.get_path() + self.name.get()

            self.parent.repl.stop_repl()  # Stop REPL to prevent serial conflict.

            self.parent.files.mkdir(path)
            self.parent.refresh()

            self.parent.repl.start_repl()
            self.destroy()
        else:
            messagebox.showerror("Error", f"You did not enter a directory name or you enter an invalid characters ({invalid_characters}).")
