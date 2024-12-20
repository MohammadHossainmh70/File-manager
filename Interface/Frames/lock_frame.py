from tkinter import Frame,Button,Entry,StringVar,Label,messagebox
from Proscessor.tools import Tools
from typing import Callable
from os import path

class LockFrame(Frame):
    def __init__(self,master:str,file_path:str):
        super().__init__(master,name='lockframe')

        self.file_path=file_path
        self.file_type='File' if not path.isdir(file_path) else 'Folder'
        self.file_name=path.basename(file_path)
 
        self.lock_file_label=Label(self,text=f'{self.file_type} :')
        self.lock_file_label.place(x=-100,y=-50,anchor='e',relx=0.5,rely=0.5,relwidth=0.2)

        self.lock_file_entry=Entry(self)
        self.lock_file_entry.place(x=-50,y=-50,anchor='w',relx=0.5,rely=0.5,relwidth=0.5)
        self.lock_file_entry.insert(0,self.file_name)
        self.lock_file_entry.config(state='readonly')

        self.password_label=Label(self,text='Password: ')
        self.password_label.place(x=-100,y=-25,anchor='e',relx=0.5,rely=0.5,relwidth=0.2)

        self.password_var=StringVar()
        self.password_entry=Entry(self,textvariable=self.password_var)
        self.password_entry.place(x=-50,y=-25,anchor='w',relx=0.5,rely=0.5,relwidth=0.5)

        self.close_lock_button=Button(self,text='X',command=lambda x=self:x.destroy(),bg='red',fg='white',borderwidth=0,activeforeground='black',activebackground='red')
        self.close_lock_button.place(x=0,y=10,anchor='e',relx=1,relwidth=0.1)


class MakeLock(LockFrame):
    def __init__(self,master:str,file_path:str):
        super().__init__(master,file_path)

        self.save_lock_button=Button(self,text='save',width=5,command=self.save)
        self.save_lock_button.place(x=-50,y=25,anchor='e',relx=1,rely=0.5)

    def save(self):
        password=self.password_var.get()
        error=Tools.lock_file(self.file_path,password)
        if error:
            messagebox.showerror('file manager',error)
        else:
            self.destroy()

class OpenLock(LockFrame):
    def __init__(self,master:str,file_path:str,folder_opener:Callable[[str],None]):
        super().__init__(master,file_path)

        self.folder_opener=folder_opener

        self.open_lock_button=Button(self,text='open',width=5,command=self.open)
        self.open_lock_button.place(x=-50,y=25,anchor='e',relx=1,rely=0.5)

    def open(self):
        password=self.password_var.get()
        if not Tools.open_lock_file(self.file_path,password):
            messagebox.showerror('file manager','Wrong password')
        else:
            Tools.open_path(self.file_path,self.folder_opener)
            self.destroy()


class PasteLock(LockFrame):
    def __init__(self,master:str,file_path:str,new_path:str,kind:str,folder_opener:Callable[[str],None]):
        super().__init__(master,file_path)

        self.new_path=new_path
        self.paste_kind=kind
        self.folder_opener=folder_opener

        self.paste_lock_button=Button(self,text='paste',width=5,command=self.paste)
        self.paste_lock_button.place(x=-50,y=25,anchor='e',relx=1,rely=0.5)

    def paste(self):
        password=self.password_var.get()
        if not Tools.open_lock_file(self.file_path,password):
            messagebox.showerror('file manager','Wrong password')
        else:
            try:
                file_new_path=path.join(self.new_path,path.basename(self.file_name))
                if self.paste_kind=='copy':
                    Tools.copy(self.file_path,self.new_path)
                    Tools.paste_lock('copy',file_new_path,password)

                elif self.paste_kind=='cut':
                    Tools.cut(self.file_path,self.new_path)
                    Tools.paste_lock('cut',file_new_path,password,self.file_path)

            except FileNotFoundError:
                messagebox.showerror('file manager','Could not find this item')

            self.folder_opener(self.new_path)
            self.destroy()

class DeleteLock(LockFrame):
    def __init__(self,master:str,file_path:str,folder_opener:Callable[[str],None],file_delete:bool|None=True):
        super().__init__(master,file_path)

        self.folder_opener=folder_opener

        if file_delete:
            self.delete_lock_button=Button(self,text='delete',width=5,command=self.file_delete)
            self.delete_lock_button.place(x=-50,y=25,anchor='e',relx=1,rely=0.5)
        else:
            self.delete_lock_button=Button(self,text='delete',width=5,command=self.lock_delete)
            self.delete_lock_button.place(x=-50,y=25,anchor='e',relx=1,rely=0.5)

    def file_delete(self):
        if path.isdir(self.file_path):
            act=messagebox.askyesno('file manager','Are you sure you want to premanently delete this folder?')
        else:
            act=messagebox.askyesno('file manager','Are you sure you want to premanently delete this file?')
        if act:
            password=self.password_var.get()
            if not Tools.open_lock_file(self.file_path,password):
                messagebox.showerror('file manager','Wrong password')
            else:
                result=Tools.delete_file_or_folder(self.file_path)
                if not result:
                    Tools.delete_lock(self.file_path)
                    self.folder_opener(path.dirname(self.file_path))
                    self.destroy()
                else:
                    messagebox.showerror('file manager',result)

    def lock_delete(self):
        act=messagebox.askyesno('file manager','''Are you sure you want to delete this file's lock?''')
        if act:
            password=self.password_var.get()
            if not Tools.open_lock_file(self.file_path,password):
                messagebox.showerror('file manager','Wrong password')
            else:
                Tools.delete_lock(self.file_path)
                self.folder_opener(path.dirname(self.file_path))
                self.destroy()