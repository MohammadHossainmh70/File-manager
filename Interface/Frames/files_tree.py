from tkinter import Tk,Frame,Event
from tkinter.ttk import Treeview
from os import path
from Proscessor.tree_generator import tree_generator

class FilesTree(Frame):
    def __init__(self,master:Tk):
        super().__init__(master,name='filetree')

        self.treeview=Treeview(self)
        self.treeview.pack(fill='y',side='left')

        self.treeview.column('#0',width=150)

        self.new_tree(r'C:\Users\user\Desktop')
        self.new_tree(r'C:\Users\user\Documents')
        self.new_tree(r'C:\Users\user\Downloads')
        self.new_tree(r'C:\Users\user\Music')
        self.new_tree(r'C:\Users\user\Pictures')
        self.new_tree(r'C:\Users\user\Videos')
        # self.new_tree(r'C:\\','Local DisK (C:)')
        # self.new_tree(r'D:\\','Local DisK (D:)')

        # self.treeview.bind('<<TreeviewSelect>>',self.send_file_path)
        self.treeview.bind('<Double-1>',self.send_file_path)
        
    def new_tree(self,folder_path:str,name:str=None):
        main_parent=self.treeview.insert('','end',iid=folder_path,text=path.basename(folder_path) if name==None else name)

        for main_parent,file_path,file_name in tree_generator(folder_path):
            self.treeview.insert(main_parent,'end',iid=file_path,text=file_name)

    def send_file_path(self,event:Event):
        file_path=self.treeview.selection()[0]
        self.master.children['filetable'].fill_table(file_path)