from tkinter import *
from tkinter import ttk

import sys
import threading
import time


class REPL(Toplevel):

    def __init__(self, parent):

        super(REPL, self).__init__()

        self.parent = parent
        self.serial = None
        # self.transient(self.parent)

        self.run = False
        self.visible = False
        self.hide()

        width = 800
        height = 400

        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
        self.title("REPL")

        if sys.platform == "win32":
            self.iconbitmap("data/ampy_icon.ico")

        self.repl_output = StringVar()
        self.repl_input = StringVar()

        output_frame = Frame(self)
        self.output_text = Text(output_frame, font="Arial 12", height=10, state=DISABLED)
        self.output_text.pack(expand=YES, fill=BOTH, side="left")
        # self.output_text.tag_config("input", foreground="blue")

        vsb = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        vsb.pack(fill=BOTH, side="right")

        self.output_text.config(yscrollcommand=vsb.set)
        output_frame.pack(expand=YES, fill=BOTH, side="top", padx=5, pady=5)

        self.input_entry = ttk.Entry(self, textvariable=self.repl_input, font="Arial 12", width=25)
        self.input_entry.pack(expand=YES, fill=BOTH, side="left", padx=5, pady=5)

        ttk.Button(self, text="Stop", takefocus=0, command=self.send_stop).pack(expand=NO, fill=BOTH, side="right", padx=5, pady=5)
        ttk.Button(self, text="Clear", takefocus=0, command=self.clear_output).pack(expand=NO, fill=BOTH, side="right", padx=5, pady=5)
        ttk.Button(self, text="Send", takefocus=0, command=self.send_cmd).pack(expand=NO, fill=BOTH, side="right", padx=5, pady=5)

        self.bind("<Return>", lambda e: self.send_cmd())
        self.protocol("WM_DELETE_WINDOW", self.hide)

        self.focus_set()

    def start_repl(self):

        """Start REPL serial read loop."""

        if not self.run and self.visible:
            repl_loop = threading.Thread(target=self.data_available, daemon=True)
            repl_loop.start()

    def stop_repl(self):

        """Stop REPL loop."""

        self.run = False

    def show(self):

        """Show hided REPL window."""

        self.serial = self.parent.board.serial
        self.deiconify()  # Show window
        self.visible = True

        self.input_entry.focus()

        self.start_repl()

    def hide(self):

        """REPL is not destroyed, only hided."""

        self.stop_repl()
        self.visible = False
        self.withdraw()  # Hide window

    def data_available(self):

        """Read all data available on the serial port."""

        self.run = True
        self.serial.reset_input_buffer()
        while self.run:
            if self.serial.in_waiting:
                data: str = self.serial.readline().decode("utf-8")
                data = data.replace(">>>", "").lstrip()

                if len(data) > 0:
                    self.output_text.config(state=NORMAL)
                    self.output_text.insert(END, data)
                    self.output_text.see(END)
                    self.output_text.config(state=DISABLED)
            else:
                time.sleep(0.1)

    def send_cmd(self):

        """Send command to the serial port."""

        cmd = self.repl_input.get().encode()
        self.serial.write(cmd + b"\r")
        self.repl_input.set("")

    def clear_output(self):

        """Clear output text widget"""

        self.output_text.config(state=NORMAL)
        self.output_text.delete(1.0, END)
        self.output_text.config(state=DISABLED)

    def send_stop(self):

        """Ctrl-C twice: interrupt any running program."""

        self.serial.write(b"\r\x03")
        time.sleep(0.1)
        self.serial.write(b"\x03")
        time.sleep(0.1)
