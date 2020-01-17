from tkinter import *
from tkinter import ttk


class About(Toplevel):

    def __init__(self, parent):

        super(About, self).__init__()

        self.parent = parent
        self.transient(self.parent)

        width = 300
        height = 175

        pos_x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (width // 2)
        pos_y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        # self.resizable(False, False)
        self.title("About")

        if sys.platform == "win32":
            self.iconbitmap("AmpyGUI_Data/AmpyGUI_icon.ico")
        elif sys.platform == "linux":
            self.icon = Image("photo", file="AmpyGUI_Data/AmpyGUI_icon.png")
            self.tk.call("wm", "iconphoto", self._w, self.icon)

        Label(self, text="AmpyGUI - Version 1.1.0 Beta").pack(pady=5)

        labelframe_text_bind = ttk.Label(self, text="Dependencies")
        label_frame_bind = ttk.LabelFrame(self, labelwidget=labelframe_text_bind)

        bind_frame = Frame(label_frame_bind)

        Label(bind_frame, text="Ampy\nMpy_cross\nTkinter\nPillow\nPython 3.7").pack(fill=BOTH, expand=YES)

        bind_frame.pack(fill=BOTH, expand=YES)
        label_frame_bind.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        Label(self, text="Copyright © 2020 Florian Poot", font="Arial 10 bold").pack(side=BOTTOM)

        self.focus_set()
        self.grab_set()
