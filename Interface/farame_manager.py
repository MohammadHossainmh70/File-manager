from tkinter import Frame
from Interface.main_tk import MainTK
from Interface.Frames.files_tree import FilesTree
from Interface.Frames.files_table import FilesTable
from Interface.Frames.toolbar import Toolbar

class FrameManager:
    def __init__(self):
        self.tk=MainTK('file manager','850x450+325+125')

        self.open_frame_with_place(Toolbar(self.tk),{'x':80,'y':0,'anchor':'n','relx':0.5,'rely':0.1,'relwidth':0.8,'relheight':0.5})
        self.open_frame_with_place(FilesTable(self.tk),{'x':80,'y':100,'anchor':'n','relx':0.5,'rely':0.1,'relwidth':0.8,'relheight':0.5})
        self.open_frame_with_pack(FilesTree(self.tk),{'fill':'y','side':'left','padx':5,'pady':5})
        
        self.tk.mainloop()

    def open_frame_with_place(self,frame:Frame,cordinat:dict):
        frame.place(**cordinat)

    # def open_frame_with_grid(self,frame:Frame,cordinat:dict):
    #     frame.grid(**cordinat)

    def open_frame_with_pack(self,frame:Frame,cordinat:dict):
        frame.pack(**cordinat)

    def hide_frame(self,name:str):
        self.tk.children[name].forget()