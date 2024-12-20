from tkinter.ttk import Treeview

def get_treeview_one_selection(table:Treeview):
    try:
        return table.selection()[0]
    except IndexError:
        return None
    
def get_treeview_selections(table:Treeview):
    try:
        return table.selection()
    except IndexError:
        return None