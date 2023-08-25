import io
from pathlib import Path


def copy_file_uppercase(input_file: io.TextIOWrapper):
    root, ext = Path(input_file.name).parts
    data = input_file.read()
    with open(f'./{root}/upper-{ext}', 'w') as copy_file:
        copy_file.write(data.upper())
