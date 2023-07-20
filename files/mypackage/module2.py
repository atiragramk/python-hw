import os
import io


def copy_file_uppercase(input_file: io.TextIOWrapper):

    file_path = os.path.basename(input_file.name)
    name_list = os.path.splitext(file_path)
    data = input_file.read()
    with open(f'./files/{name_list[0]}-upper{name_list[1]}', 'w') as copy_file:
        copy_file.write(data.upper())
