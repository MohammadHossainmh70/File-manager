from tkinter import Tk

class MainTK(Tk):
    def __init__(self,tk_name:str,geometry:str):
        super().__init__()
        self.title(tk_name)
        self.geometry(geometry)

    def mainloop(self, n = 0):
        return super().mainloop(n)