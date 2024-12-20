from tkinter import Tk,Frame,StringVar,Entry,Button,Event,messagebox,OptionMenu
from Proscessor.tools import Tools
from Proscessor import get_file_name_and_type
from Interface.Frames import get_treeview_one_selection,get_treeview_selections
from Interface.Frames.lock_frame import MakeLock,PasteLock,DeleteLock
from os import path

class Toolbar(Frame):
    def __init__(self,master:Tk):
        super().__init__(master,name='toolbar')

        self.paste_kind=''
        self.paste_cash=''

        self.path_var=StringVar(name='path_var')
        self.path_entry=Entry(self,textvariable=self.path_var)
        self.path_entry.pack(fill='x',side='top',anchor='w')

        self.path_entry.bind('<Return>',self.locate_path)

        self.back_button=Button(self,text='<',command=self.back)
        self.back_button.place(x=0,y=50,anchor='w')

        self.copy_button=Button(self,text='Copy',command=self.copy)
        self.copy_button.place(x=50,y=50,anchor='w')

        self.cut_button=Button(self,text='Cut',command=self.cut)
        self.cut_button.place(x=90,y=50,anchor='w')

        self.paste_button=Button(self,text='Paste',command=self.paste)
        self.paste_button.place(x=140,y=50,anchor='w')

        self.rename_button=Button(self,text='Rename',command=self.rename)
        self.rename_button.place(x=200,y=50,anchor='w')

        self.delete_button=Button(self,text='Delete',command=self.delete)
        self.delete_button.place(x=260,y=50,anchor='w')

        self.lock_button=Button(self,text='lock',command=self.lock)
        self.lock_button.place(x=315,y=50,anchor='w')

        self.unlock_button=Button(self,text='unlock',command=self.unlock)
        self.unlock_button.place(x=350,y=50,anchor='w')

        self.new_var=StringVar()
        self.new_var.set('New')
        self.new_values=('Folder','Text','Excel','Zip')
        self.new_button=OptionMenu(self,self.new_var,*self.new_values,command=self.new_thing)
        self.new_button.place(x=410,y=50,anchor='w')

    def locate_path(self,event:Event|None=None):
        file_path=self.path_var.get()
        self.master.children['filetable'].fill_table(file_path)

    def paste(self):
        paste_place=self.path_var.get()

        for paste_cash in self.paste_cash:
            if not Tools.is_lock(paste_cash):
                try:
                    if self.paste_kind=='copy':
                        Tools.copy(paste_cash,paste_place)

                    elif self.paste_kind=='cut':
                        Tools.cut(paste_cash,paste_place)
                except FileNotFoundError:
                    messagebox.showerror('file manager','Could not find this item')

                self.master.children['filetable'].fill_table(paste_place)
            else:
                self.lock_frame=PasteLock(self.master,paste_cash,paste_place,self.paste_kind,self.master.children['filetable'].fill_table)
                self.lock_frame.place(x=0,y=0,anchor='center',relx=0.5,rely=0.5,relwidth=0.5,relheight=0.4)

    def copy(self):
        self.paste_kind='copy'
        self.paste_cash=get_treeview_selections(self.master.children['filetable'].children['table'])
            
    def cut(self):
        self.paste_kind='cut'
        self.paste_cash=get_treeview_selections(self.master.children['filetable'].children['table'])

    def rename(self):
        file_path=get_treeview_one_selection(self.master.children['filetable'].children['table'])
        if path.isdir(file_path):
            file_name=path.basename(file_path)
        else:
            file=get_file_name_and_type(file_path)
            file_name=file['name']
        self.path_var.set(file_name)

        def renameing(event):
            if path.isdir(file_path):
                file_new_name=self.path_var.get()
            else:
                file_new_name=f'{self.path_var.get()}.{file['type']}'
            Tools.rename_file_or_folder(file_path,file_new_name)
            self.master.children['filetable'].fill_table(path.dirname(file_path))
            self.path_entry.bind('<Return>',self.locate_path)

        self.path_entry.bind('<Return>',renameing)

    def delete(self):
        file_paths=get_treeview_selections(self.master.children['filetable'].children['table'])
        
        if len(file_paths)==1:
            if path.isdir(file_paths[0]):
                act=messagebox.askyesno('file manager','Are you sure you want to premanently delete this folder?')
            else:
                act=messagebox.askyesno('file manager','Are you sure you want to premanently delete this file?')
        elif len(file_paths)>1:
            act=messagebox.askyesno('file manager','Are you sure you want to premanently delete these files?')
        
        for file_path in file_paths:
            if not Tools.is_lock(file_path):
                if act:
                    result=Tools.delete_file_or_folder(file_path)
                    if result:
                        messagebox.showerror('file manager',result)
                    else:
                        self.master.children['filetable'].fill_table(path.dirname(file_path))
            else:
                self.lock_frame=DeleteLock(self.master,file_path,self.master.children['filetable'].fill_table)
                self.lock_frame.place(x=0,y=0,anchor='center',relx=0.5,rely=0.5,relwidth=0.5,relheight=0.4)

    def back(self):
        folder_name=self.path_var.get()
        dir_name=path.dirname(folder_name)
        self.master.children['filetable'].fill_table(dir_name)

    def lock(self):
        file_path=get_treeview_one_selection(self.master.children['filetable'].children['table'])

        if file_path:
            file_type='File' if not path.isdir(file_path) else 'Folder'
            frame_name='lockframe'

            if not frame_name in self.master.children.keys():
                if Tools.is_lock(file_path):
                    messagebox.showinfo('file manager',f'{file_type} is already locked')

                else:
                    self.lock_frame=MakeLock(self.master,file_path)
                    self.lock_frame.place(x=0,y=0,anchor='center',relx=0.5,rely=0.5,relwidth=0.5,relheight=0.4)

    def unlock(self):
        file_path=get_treeview_one_selection(self.master.children['filetable'].children['table'])
        
        if file_path:
            if not Tools.is_lock(file_path):
                file_type='File' if not path.isdir(file_path) else 'Folder'
                messagebox.showerror('file manager',f'{file_type} is not locked')
            else:
                self.lock_frame=DeleteLock(self.master,file_path,self.master.children['filetable'].fill_table,False)
                self.lock_frame.place(x=0,y=0,anchor='center',relx=0.5,rely=0.5,relwidth=0.5,relheight=0.4)


    def new_thing(self,thing):
        thing=self.new_var.get()

        location_path=self.path_var.get()
        Tools.new_thing(thing,location_path)

        self.new_var.set('New')

        self.master.children['filetable'].fill_table(location_path)