unzip_file_data = {
        'file_path':'',
        'file_name':'',
        'output_path':''
        }

def unzip_file(data):
    import os
    import tarfile

    ##minimal data inputs payload
    file_path = data.get('file_path', '')
    file_name = data.get('file_name', '')
    output_path = data.get('output_path', '')
    ##

    full_path = os.path.join(file_path, file_name)

    if not os.path.isfile(full_path):
        raise NameError(f'{full_path}  does not exist!!')

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    with tarfile.open(full_path) as file:
        file.extractall(output_path)
    return output_path
