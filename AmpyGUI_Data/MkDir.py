from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class MkDir(Toplevel):

    def __init__(self, parent):

        super(MkDir, self).__init__()

        self.parent = parent
        self.transient(self.parent)

        self.geometry("300x50" + "+" + str(int(self.parent.geometry().split("+")[1]) + 175)
                      + "+" + str(int(self.parent.geometry().split("+")[2]) + 65))

        self.resizable(False, False)
        self.title("MkDir...")
        self.iconbitmap("AmpyGUI_Data/AmpyGUI_icon.ico")

        self.name = StringVar()
        ttk.Entry(self, textvariable=self.name, font="Arial 12", width=25).pack(expand=YES, fill=BOTH, side="left", padx=5, pady=10)
        ttk.Button(self, text="Ok", takefocus=0, command=self.mk_dir).pack(expand=YES, fill=BOTH, side="right", padx=5, pady=10)

        self.focus_set()
        self.grab_set()

    def mk_dir(self):

        """Make a directory on the board."""

        invalid_characters = "\\/:*?\"<>|."

        if self.name.get() != "" and not any((c in invalid_characters) for c in self.name.get()):
            if "." in self.parent.get_path():
                path = "/" + "/".join(self.parent.get_path().split("/")[:-2]) + self.name.get()
            else:
                path = self.parent.get_path() + self.name.get()

            self.parent.files.mkdir(path)
            self.parent.refresh()
            self.destroy()
        else:
            messagebox.showerror("Error", f"You did not enter a directory name or you enter an invalid characters ({invalid_characters}).")
