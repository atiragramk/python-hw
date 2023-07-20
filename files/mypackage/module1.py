import string
from random import randint

alphabet = []
for i in string.ascii_uppercase:
    alphabet.append(i)


def generate_files():
    data = []
    for ch in alphabet:
        with open(f'./files/{ch}.txt', 'w+') as file:
            file.write(f'{randint(1, 100)}')
            file.seek(0)
            data.append(f'{ch}.txt:{file.read()}\n')

    with open('./files/summary.txt', 'w') as sum_file:
        sum_file.writelines(data)
