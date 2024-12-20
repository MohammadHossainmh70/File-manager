from os import path

def get_file_name_and_type(file_path:str)->dict[str,str]:
    file_name=path.basename(file_path)
    splited_name=file_name.split('.')
    
    file_type=''
    if len(splited_name)==2:
        file_name=splited_name[0]
        file_type=splited_name[1]

    elif len(splited_name)>2:
        file_type=splited_name.pop(-1)
        file_name=''
        for i in range(len(splited_name)):
            if i<len(splited_name)-1:
                file_name+=splited_name[i]+'.'
            elif i==len(splited_name)-1:
                file_name+=splited_name[i]
    
    return {'name':file_name,'type':file_type}