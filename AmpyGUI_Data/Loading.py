from tkinter import *

from AmpyGUI_Data.AnimatedGif import AnimatedGif


class Loading(Toplevel):

    def __init__(self, parent, title):

        super(Loading, self).__init__()

        self.parent = parent
        self.transient(self.parent)

        width = 200
        height = 80

        pos_x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (width // 2)
        pos_y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (height // 2) - 10

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        self.resizable(False, False)
        self.title(title)
        self.iconbitmap("AmpyGUI_Data/AmpyGUI_icon.ico")

        frame = Frame(self)
        self.loading = AnimatedGif(frame)
        self.loading.grid(column=0, row=0)

        Label(frame, text=title + "...").grid(column=1, row=0)
        frame.pack(expand=YES)

        self.loading.load("AmpyGUI_Data/Loading.gif")

        self.protocol("WM_DELETE_WINDOW", lambda: None)

        self.focus_set()
        self.grab_set()

    def close(self):

        self.loading.unload()
        self.destroy()
