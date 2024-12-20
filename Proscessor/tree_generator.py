from os import path,walk
from typing import Generator

def tree_generator(folder_path:str)->Generator[str, str, str]:
    '''Directory tree generator for tkinter.ttk Treeview()
    
    user os.walk() to yield main_parent,file_path,file_name for Treeview parent,iid,text'''
    for main_folder,folders,files in walk(folder_path):
            main_parent=main_folder
            for folder in folders:
                  yield main_parent,path.join(main_folder,folder),path.basename(folder)