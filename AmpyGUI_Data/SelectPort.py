from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import serial


class SelectPort(Toplevel):

    def __init__(self, parent):

        super(SelectPort, self).__init__()

        self.parent = parent
        self.transient(self.parent)

        self.geometry("300x100" + "+" + str(int(self.parent.geometry().split("+")[1]) + 175)
                      + "+" + str(int(self.parent.geometry().split("+")[2]) + 65))

        self.resizable(False, False)
        self.title("Board")
        self.iconbitmap("AmpyGUI_Data/AmpyGUI_icon.ico")

        # region Port
        port = Frame(self, bd=1, relief=GROOVE)
        Label(port, text="Select port: ", anchor=W).grid(column=0, row=0, sticky=E, pady=5, padx=5)

        self.combo_box = ttk.Combobox(port, state="readonly", takefocus=0, width=10)
        self.serial_ports()

        self.combo_box.bind("<FocusIn>", self.connect_button)

        self.combo_box.grid(column=1, row=0, sticky=W)

        port.columnconfigure(0, weight=1)
        port.columnconfigure(1, weight=1)
        port.rowconfigure(0, weight=1)

        port.grid(column=0, row=0, columnspan=2, sticky=N+S+E+W, padx=10, pady=10)
        # endregion

        ttk.Button(self, text="Refresh", takefocus=False, command=self.serial_ports).grid(column=0, row=1, sticky=N+S+E+W, padx=10, pady=5)
        self.connect = ttk.Button(self, text="Connect", takefocus=False, state=DISABLED, command=self.connect)
        self.connect.grid(column=1, row=1, sticky=N+S+E+W, padx=10, pady=5)

        for i in range(2):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.close)

        self.focus_set()
        self.grab_set()

    def connect_button(self, event=None):

        """Enable connect button if port selected."""

        # Force focus to avoid blue selection on combobox.
        self.focus_set()

        if self.combo_box.get() != "":
            self.connect.config(state=NORMAL)

    def serial_ports(self):

        """Lists available serial port names."""

        ports = ["COM%s" % (i + 1) for i in range(256)]

        result = list()
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        self.combo_box.config(values=result)

    def connect(self):

        """If a port is selected, close this window and connect to the board."""

        if self.combo_box.get() == "":
            messagebox.showwarning("Warning", "No port selected. Please select one.")
        else:
            self.parent.connect(self.combo_box.get())
            self.destroy()

    def close(self):

        """Close all windows and quit application"""

        self.destroy()
        self.parent.destroy()