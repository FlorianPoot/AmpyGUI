from tkinter import *
from tkinter import ttk

import sys


class About(Toplevel):

    def __init__(self, parent):

        super(About, self).__init__()

        self.parent = parent
        self.transient(self.parent)

        width = 300
        height = 200

        pos_x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (width // 2)
        pos_y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        self.resizable(False, False)
        self.title("About")

        if sys.platform == "win32":
            self.iconbitmap("data/ampy_icon.ico")

        Label(self, text=f"AmpyGUI - Version {self.parent.version}").pack(pady=5)

        labelframe_text_bind = ttk.Label(self, text="Requirements")
        label_frame_bind = ttk.LabelFrame(self, labelwidget=labelframe_text_bind)

        bind_frame = Frame(label_frame_bind)

        Label(bind_frame, text="adafruit-ampy 1.1.0\npyserial 3.5\nTkinter 8.6.12\nmpy-cross 1.19.1\nPillow 9.4.0\nPython 3.11.2").pack(fill=BOTH, expand=YES)

        bind_frame.pack(fill=BOTH, expand=YES)
        label_frame_bind.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        Label(self, text="Copyright © 2023 Florian Poot", font="Arial 10 bold").pack(side=BOTTOM)

        self.focus_set()
        self.grab_set()
