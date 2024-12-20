from tkinter import Tk,Frame,Event,messagebox
from tkinter.ttk import Treeview
from Proscessor.table_generator import TableMaker
from Proscessor.tools import Tools
from Interface.Frames import get_treeview_one_selection
from Interface.Frames.lock_frame import OpenLock

class FilesTable(Frame):
    def __init__(self,master:Tk):
        super().__init__(master,name='filetable')
        self.tree_item=[]

        self.treeview=Treeview(self,name='table',columns=('name','type','size','create date','last change','last access'),height=25)
        self.treeview.pack(fill='both')

        text_list=['#','name','type','size','create date','last change','last access']
        width_list=[50,175,75,100,125,125,125]
        for i in range(7):
            self.treeview.heading(f'#{i}',anchor='w',text=text_list[i])
            self.treeview.column(f'#{i}',width=width_list[i])

        self.fill_table(r'C:\Users\user\Desktop')

        # self.treeview.bind('<<TreeviewSelect>>',self.open_file_or_folder)
        self.treeview.bind('<Double-1>',self.open_file_or_folder)

        self.treeview.bind('<Escape>',self.back)
        self.treeview.bind('<Control-c>',self.copy)
        self.treeview.bind('<Control-x>',self.cut)
        self.treeview.bind('<Control-v>',self.paste)
        self.treeview.bind('<Shift-Delete>',self.delete)

    def fill_table(self,selection_path:str):
        try:
            TableMaker.path_exist(selection_path)

        except FileNotFoundError:
            messagebox.showerror('file manager',message=f'path {selection_path} not existe. Check it and try again.')
        
        else:
            self.master.children['toolbar'].path_var.set(selection_path)
        
            for item in self.tree_item:
                self.treeview.delete(item)
            self.tree_item.clear()
        
            row_number=1
            for infos in TableMaker.table_generator(selection_path):
                item=self.treeview.insert('','end',iid=infos.path,text=str(row_number),values=(infos.name,infos.type,infos.size,infos.create_date,infos.modifide_date,infos.access_date))
                self.tree_item.append(item)
                row_number+=1
            
    def open_file_or_folder(self,event:Event|None):
        selected=get_treeview_one_selection(self.treeview)
        if selected:
            if not Tools.is_lock(selected):
                Tools.open_path(selected,self.fill_table)

            else:
                match Tools.is_lock(selected):
                    case 'main_lock':
                        self.lock_frame=OpenLock(self.master,selected,self.fill_table)
                        self.lock_frame.place(x=0,y=0,anchor='center',relx=0.5,rely=0.5,relwidth=0.5,relheight=0.4)
                    
                    case 'item_lock':
                        Tools.open_path(selected,self.fill_table)

    def back(self,event:Event|None):
        self.master.children['toolbar'].back()

    def copy(self,event:Event|None):
        self.master.children['toolbar'].copy()

    def cut(self,event:Event|None):
        self.master.children['toolbar'].cut()

    def paste(self,event:Event|None):
        self.master.children['toolbar'].paste()

    def delete(self,event:Event|None):
        self.master.children['toolbar'].delete()