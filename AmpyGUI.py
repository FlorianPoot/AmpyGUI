from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from ampy.pyboard import Pyboard
from ampy.files import Files

from AmpyGUI_Data.PutFiles import PutFiles
from AmpyGUI_Data.SelectPort import SelectPort
from AmpyGUI_Data.Loading import Loading
from AmpyGUI_Data.MkDir import MkDir

import threading
import textwrap
import ast


class AmpyGUI(Tk):

    def __init__(self):

        # Report all exceptions to a MessageBox.
        Tk.report_callback_exception = self.show_error
        
        super(AmpyGUI, self).__init__()

        self.title("AmpyGUI - Version 1.0.0 Beta")
        self.geometry("650x250")
        self.minsize(650, 250)
        self.iconbitmap("AmpyGUI_Data/AmpyGUI_icon.ico")

        self.tree_view = ttk.Treeview(self, selectmode=BROWSE)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree_view.yview)
        vsb.grid(column=1, row=0, sticky=N+S)

        self.tree_view.configure(yscrollcommand=vsb.set)

        self.tree_view["columns"] = ("type", "size")

        self.tree_view.column("type", width=50, minwidth=50, stretch=NO)
        self.tree_view.column("size", width=150, minwidth=150, stretch=NO)

        self.tree_view.heading("#0", text="Name", anchor=W)
        self.tree_view.heading("type", text="Type", anchor=W)
        self.tree_view.heading("size", text="Size", anchor=W)

        self.tree_view.grid(column=0, row=0, sticky=N+S+E+W)
        self.tree_view.bind("<ButtonRelease-1>", self.select_item)

        ttk.Separator(orient=HORIZONTAL).grid(column=0, row=1, columnspan=2, sticky=N+S+E+W)

        memory = Frame(self, bd=1, relief=GROOVE)

        self.total_label = Label(memory, text="Total: N/A MB")
        self.total_label.pack(expand=YES, fill=BOTH, side="left", padx=10)

        self.free_label = Label(memory, text="Free: N/A MB")
        self.free_label.pack(expand=YES, fill=BOTH, side="left", padx=10)

        self.used_label = Label(memory, text="Used: N/A %")
        self.used_label.pack(expand=YES, fill=BOTH, side="left", padx=10)

        memory.grid(column=0, row=2, columnspan=2, pady=5)

        buttons = Frame(self)

        self.get_button = ttk.Button(buttons, text="Get", takefocus=False, command=self.get, state=DISABLED)
        self.get_button.grid(column=0, row=0, sticky=E+W, padx=5)

        ttk.Button(buttons, text="Put", takefocus=False, command=self.put).grid(column=1, row=0, sticky=E+W, padx=5)
        ttk.Button(buttons, text="MkDir", takefocus=False, command=self.mk_dir).grid(column=2, row=0, sticky=E+W, padx=5)
        ttk.Button(buttons, text="Reset", takefocus=False, command=self.reset).grid(column=3, row=0, sticky=E+W, padx=5)

        self.remove_button = ttk.Button(buttons, text="Remove", takefocus=False, command=self.remove, state=DISABLED)
        self.remove_button.grid(column=4, row=0, sticky=E+W, padx=5)

        ttk.Button(buttons, text="Format", takefocus=False, command=self.format).grid(column=5, row=0, sticky=E+W, padx=5)

        for i in range(6):
            buttons.columnconfigure(i, weight=1)

        buttons.grid(column=0, row=3, columnspan=2, sticky=N+S+E+W, padx=10, pady=5)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.port = None
        self.board = None
        self.files = None

        self.real_paths = dict()  # ID: Path

        self.update()
        # Start port popup
        SelectPort(self)

        self.protocol("WM_DELETE_WINDOW", self.close)

        self.mainloop()

    def select_item(self, event=None):

        """Enable buttons if an item is selected in tree view."""

        item = self.tree_view.item(self.tree_view.focus())["text"]

        if item != "":
            self.remove_button.config(state=NORMAL)

            # Folders are determined by the lack of extension.
            if "." in item:
                self.get_button.config(state=NORMAL)
            else:
                self.get_button.config(state=DISABLED)
        else:
            self.remove_button.config(state=DISABLED)
            self.get_button.config(state=DISABLED)

    def connect(self, port):

        """Connect to the selected port and fill window infos"""

        self.port = port
        self.board = Pyboard(self.port)
        self.files = Files(self.board)

        self.refresh()

    def get_path(self):

        name = self.tree_view.item(self.tree_view.focus())
        item = self.tree_view.focus()

        # Folders are determined by the lack of extension.
        if item != "" and "." not in name:
            return self.real_paths[item] + "/"
        else:
            return "/"

    def list_dir(self):

        """Listdir board and insert result into tree view"""

        directories = {"/": ""}
        files = self.files.ls(recursive=True)

        for file in files:
            name, size = file.split(" - ")
            directory = name.split("/")[:-1]

            for index in range(1, len(directory)):
                if "/".join(directory[:index + 1]) not in directories:
                    _id = self.tree_view.insert(directories["/" + directory[index - 1]], "end", text=directory[index])
                    self.real_paths[_id] = "/".join(directory[:index + 1])
                    directories["/".join(directory[:index + 1])] = _id

        for file in files:
            name, size = file.split(" - ")
            directory = name.split("/")[:-1]
            directory = "/".join(directory)[1:]

            # Folders are determined by the lack of extension.
            if "." in name:
                _id = self.tree_view.insert(directories["/" + directory], "end", text=name.split("/")[-1], values=(name.split("/")[-1].split(".")[1].upper(), size))
            else:
                _id = self.tree_view.insert(directories["/" + directory], "end", text=name.split("/")[-1])

            self.real_paths[_id] = name

    def clear(self):

        """Clear tree view"""

        self.real_paths = dict()
        self.tree_view.delete(*self.tree_view.get_children())

    def time_out(self):

        """Close board and spread an error popup if delay is over."""

        self.board.close()

    def get_space_info(self):

        command = """\
                  import uos
                  print(uos.statvfs("/"))
                  """

        self.board.enter_raw_repl()
        out = self.board.exec_(textwrap.dedent(command)).decode("utf-8")
        self.board.exit_raw_repl()

        out = ast.literal_eval(out)

        total = round((out[0] * out[2]) / 1024**2, 2)
        self.total_label.config(text=f"Total: {total} MB")

        free = round((out[0] * out[3]) / 1024**2, 2)
        self.free_label.config(text=f"Free: {free} MB")

        used = round(((total - free) / total) * 100, 2)
        self.used_label.config(text=f"Used: {used} %")

    def refresh(self):

        """Clear treeview, Listdir and get space info."""

        # Start timer
        timer = threading.Timer(5, self.time_out)
        timer.start()

        self.clear()
        self.list_dir()
        self.select_item()
        self.get_space_info()

        timer.cancel()

    def get(self):

        """Download selected item to selected directory."""

        def get_thread():
            try:
                with open(path + "/" + name, "wb") as file:
                    file.write(self.files.get(self.real_paths[item]))
                loading.close()
            except Exception as e:
                self.show_error(e)

        name = self.tree_view.item(self.tree_view.focus())["text"]
        item = self.tree_view.focus()

        path = filedialog.askdirectory()

        loading = Loading(self, title="Downloading")
        threading.Thread(target=get_thread).start()

    def put(self):

        """Upload files or folder."""

        PutFiles(self)

    def mk_dir(self):

        """Make a directory on the board."""

        MkDir(self)

    def remove(self):

        """Remove selected file or folder."""

        if not messagebox.askyesno("Remove", "Are you sure you want to remove the selected file or folder ?"):
            return

        item = self.tree_view.focus()

        # Folders are determined by the lack of extension.
        if "." not in self.real_paths[item]:
            self.files.rmdir(self.real_paths[item])
        else:
            self.files.rm(self.real_paths[item])

        del self.real_paths[item]

        self.tree_view.delete(self.tree_view.focus())
        self.get_space_info()

    def reset(self):

        """Perform a soft reset."""

        self.board.serial.write(b"\x03\x04")

    def format(self):

        """Remove all files except boot.py."""

        def format_thread():
            try:
                for value in self.real_paths.values():
                    if value != "/boot.py" and "/" not in value[1:]:
                        # Folders are determined by the lack of extension.
                        if "." not in value:
                            self.files.rmdir(value)
                        else:
                            self.files.rm(value)
                self.refresh()
                loading.close()
            except Exception as e:
                self.show_error(e)

        if not messagebox.askyesno("Format", "Are you sure you want to remove all files except boot.py ?"):
            return

        loading = Loading(self, title="Formatting")
        threading.Thread(target=format_thread).start()

    def close(self):

        """Close board and destroy window."""

        self.board.close()
        self.destroy()

    @staticmethod
    def show_error(*args):
        messagebox.showerror("Exception", args)


if __name__ == "__main__":
    AmpyGUI()
