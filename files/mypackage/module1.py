import string
from random import randint


def generate_files():
    data = []
    for ch in list(string.ascii_uppercase):
        with open(f'./files/{ch}.txt', 'w+') as file:
            file.write(f'{randint(1, 100)}')
            file.seek(0)
            data.append(f'{ch}.txt:{file.read()}\n')

    with open('./files/summary.txt', 'w') as sum_file:
        sum_file.writelines(data)
