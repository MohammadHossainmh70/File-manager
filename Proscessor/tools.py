from os import path,rename,walk,unlink,rmdir,startfile,mkdir
from shutil import copy2,copytree,move,Error
from openpyxl import Workbook
from Data.path_password import save_lock,open_lock,is_path_lock,delete_lock
from Proscessor.table_generator import TableMaker
from typing import Callable

class Tools():
    @staticmethod
    def copy(file_path:str,location_path:str):
        '''Make copy of file or folder\n
        can not make several copy of one file or folder in one directory'''
        if path.isdir(location_path):
            location_path=path.join(location_path,f'{path.basename(file_path)}')

        try:
            if path.isdir(file_path):
                copytree(file_path,location_path)
            else:
                copy2(file_path,location_path)
        except FileExistsError:
            pass   
        except PermissionError:
            pass

    @staticmethod
    def cut(file_path:str,location_path:str):
        '''Move file or folder to other path'''
        try:
            move(file_path,location_path)
        except Error:
            pass
    
    @staticmethod
    def rename_file_or_folder(file_path:str,new_name:str):
        '''Rename file or folder'''
        if not path.exists(new_name):
            new_name=path.join(path.dirname(file_path),new_name)

        rename(file_path,new_name)

    @staticmethod
    def delete_file_or_folder(file_path:str)->str|None:
        '''Delete file\n
        Delte folder even if it is not empty'''
        if path.isfile(file_path):
            try:
                unlink(file_path)
            except FileNotFoundError:
                pass
        
        else:
            act=True
            search=TableMaker.search(file_path,kind='proper')
            for i in search:
                if Tools.is_lock(i)=='main_lock':
                    act=False
                    break
            if not act:
                return 'There are some main_locked files in this folder'

            main_folders=[]
            for main_folder,folders,files in walk(file_path):
                try:
                    for file in files:
                        unlink(path.join(main_folder,file))

                    rmdir(main_folder)  
                except FileNotFoundError:
                    pass

                except OSError:
                    main_folders.append(main_folder)

            main_folders.reverse()
            for main_folder in main_folders:
                try:
                    rmdir(main_folder)
                except FileNotFoundError:
                    pass
    
    @staticmethod
    def folder_items(folder_path:str)->list:
        '''return list of folder's items path'''
        items=[]
        for main_folder,folders,files in walk(folder_path):
            for file in files:
                items.append(path.join(main_folder,file))
        return items

    @staticmethod
    def lock_file(file_path:str,password:str)->str|None:
        '''Set a password for file or folder'''
        if len(password)<4:
            return 'password too short'
        
        if path.isdir(file_path):
            path_items=Tools.folder_items(file_path)
        else:
            path_items=[]
        save_lock(file_path,password,path_items)

    @staticmethod
    def open_lock_file(file_path:str,password:str)->bool:
        '''returen True if password is correct'''
        return open_lock(file_path,password)
    
    @staticmethod
    def is_lock(file_path:str|None)->str|bool:
        '''Check if the file or folder is locked\n
        if yes returen the kind of lock\n
        else False'''
        if file_path:
            return is_path_lock(file_path) 
        
        return False
    @staticmethod
    def open_path(file_path:str,folder_opener:Callable[[str],None]):
        '''Run file or open folder'''
        if path.isdir(file_path):
            folder_opener(file_path)
        else:
            startfile(file_path)

    @staticmethod
    def paste_lock(kind:str,file_path:str,password:str,old_path:str|None=None):
        if kind=='copy':
            save_lock(file_path,password,Tools.folder_items(file_path))

        elif kind=='cut':
            delete_lock(old_path)
            save_lock(file_path,password,Tools.folder_items(file_path))

    @staticmethod
    def delete_lock(file_path:str):
        delete_lock(file_path)

    @staticmethod
    def new_thing(thing:str,location_path:str):
        type_dict={'Folder':'Folder','Text':'txt','Excel':'xlsx','Zip':'zip'}
        type_thing=type_dict[thing]

        num=1
        copy_except=''
        while True:
            try:
                if type_thing=='Folder':
                    mkdir(rf'{location_path}\New folder{copy_except}')
                elif type_thing=='xlsx':
                    if path.exists(rf'{location_path}\New Excel{copy_except}.xlsx'):
                        raise FileExistsError
                    workbook=Workbook()
                    workbook.save(rf'{location_path}\New Excel{copy_except}.xlsx')
                else:
                    with open(rf'{location_path}\new {thing}{copy_except}.{type_thing}','x'):
                        pass
            except FileExistsError:
                copy_except=f'-copy{num}'
                num+=1
            else:
                break