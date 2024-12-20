from os import scandir,DirEntry,path,walk
from datetime import datetime
from typing import Generator
from dataclasses import dataclass
from Proscessor import get_file_name_and_type

@dataclass
class dir_info:
    path:str
    name:str
    type:str
    size:str
    create_date:datetime
    modifide_date:datetime
    access_date:datetime

class TableMaker:
    @staticmethod
    def path_exist(path_location:str) -> FileNotFoundError:
        '''Check if the path_location exists \n
        if not raise FileNotFoundError'''
        if not path.exists(path_location):
            raise FileNotFoundError
        
    @staticmethod
    def source_sorter(source_path:str) -> list:
        '''Sort the folder and files in the source_path and return it as list'''
        TableMaker.path_exist(source_path)

        dir_entry_list=[]
        for dir_entry in scandir(source_path):
            dir_entry_list.append(dir_entry)
        
        folder_list=filter(lambda x1:x1.is_dir(),dir_entry_list)
        folder_list=sorted(folder_list,key=lambda x1:x1.name)

        file_list=filter(lambda x2:x2.is_file(),dir_entry_list)
        file_list=sorted(file_list,key=lambda x2:x2.name)

        folder_list.extend(file_list)

        return folder_list
    
    @staticmethod
    def search(source_path:str,text:str|None='',kind:str|None='proper')->str:
        '''Search source_path for given tex\n
        return all items in source_path if text == None'''

        search_folers={'',}
        search_folers.clear()
        search_files={'',}
        search_files.clear()
        act=True
        if kind=='proper':
            act=False
        for main_folder,folders,files in walk(source_path):
            if text in main_folder:
                if act:
                    search_folers.add(main_folder)
                act=True
            for file in files:
                if text in file:
                    search_files.add(file)
        
        search_list=list(search_folers)
        search_list.sort()
        search_files=list(search_files)
        search_files.sort()
        search_list.extend(search_files)

        return search_list
        
    @staticmethod
    def table_generator(source_path:str|None=None,source_list:list|None=None) -> Generator[dir_info,None,None]:
        '''Generator for files's informatin in source_path'''
        folder_list=''
        if source_path:
            TableMaker.path_exist(source_path)
            folder_list=TableMaker.source_sorter(source_path)
        elif source_list:
            folder_list=source_list

        for dir_entry in folder_list:
            dir_entry:DirEntry[str]
            dir_path=dir_entry.path
            dir_information=dir_entry.stat()

            if dir_entry.is_dir():
                dir_name=dir_entry.name
                dir_type='file folder'
                dir_size=''
            else:
                dir_name_type=get_file_name_and_type(dir_entry.path)
                dir_name=dir_name_type['name']
                dir_type=dir_name_type['type']

                dir_size=str(dir_information.st_size/1000)+' KB'
            dir_create=datetime.fromtimestamp(dir_information.st_birthtime)
            dir_modifide=datetime.fromtimestamp(dir_information.st_mtime)
            dir_access=datetime.fromtimestamp(dir_information.st_atime)

            yield dir_info(dir_path,dir_name,dir_type,dir_size,dir_create,dir_modifide,dir_access)