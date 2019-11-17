from tkinter import *
from PIL import Image, ImageTk
from itertools import count


class AnimatedGif(Label):

    def __init__(self, parent=None):

        super(AnimatedGif, self).__init__(parent)
        self.loc = 0
        self.frames = []
        self.delay = int()

    def load(self, image):

        if isinstance(image, str):
            image = Image.open(image)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(image.copy()))
                image.seek(i)
        except EOFError:
            pass

        try:
            self.delay = image.info["duration"]
        except KeyError:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
