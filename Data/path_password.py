from sqlite3 import connect

DATABASE=r'Data\path_lock.db'

def save_lock(file_path:str,password:str,folder_items:list):
    with connect(DATABASE) as connection:
        cursor=connection.cursor()
        cursor.execute('''
        INSERT INTO path_lock (
            path,
            password)
        VALUES (
            ?,
            ?);''',(file_path,password))
        connection.commit()
        
        for item in folder_items:
            cursor.execute('''
            INSERT INTO folder_items_lock (
                path,
                folder,
                password)
            VALUES (
                ?,
                ?,
                ?);''',(item,file_path,password))
            
            connection.commit()
        
def open_lock(file_path:str,password:str)->bool:
    with connect(DATABASE) as connection:
        cursor=connection.cursor()
        cursor.execute('''
        SELECT path
        FROM path_lock
        WHERE path=? AND password=?;''',(file_path,password))

        file=cursor.fetchone()

        cursor.execute('''
            SELECT path
            FROM folder_items_lock
            WHERE path=? AND password=?;''',(file_path,password))

        item=cursor.fetchone()

        if file or item:
            return True
                    
        return False

def is_path_lock(file_path:str)->str|bool:
    with connect(DATABASE) as connection:
        cursor=connection.cursor()
        cursor.execute('''
        SELECT path
        FROM path_lock
        WhERE path=?;''',(file_path,))

        file=cursor.fetchone()

        cursor=connection.cursor()
        cursor.execute('''
        SELECT path
        FROM folder_items_lock
        WhERE path=?;''',(file_path,))

        item=cursor.fetchone()
        
        if file:
            return 'main_lock'
        
        elif item:
            return 'item_lock'

        return False
    
def delete_lock(file_path:list):
    with connect(DATABASE) as connection:
        cursor=connection.cursor()
        cursor.execute('''
        DELETE FROM path_lock
        WHERE path = ?;''',(file_path,))

        connection.commit()

        # for item in folder_items:
        #     cursor=connection.cursor()
        #     cursor.execute('''
        #     DELETE FROM folder_items_lock
        #     WHERE path = ?;''',(item,))

        #     connection.commit()

        cursor=connection.cursor()
        cursor.execute('''
        DELETE FROM folder_items_lock
        WHERE folder = ?;''',(file_path,))

        connection.commit()