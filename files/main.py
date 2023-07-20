from mypackage import (
    module1 as m1,
    module2 as m2,
    module3 as m3,
    module4 as m4
)

m1.generate_files()


def copy():
    with open('files/some.txt', 'w+') as file:
        content = "Once there was an elephant,\nWho tried to use the telephant—\nNo! No! I mean an elephone\nWho tried to use the telephone—"
        file.write(content)
        file.seek(0)
        m2.copy_file_uppercase(file)


copy()

m3.record_score()
m4.record_highest_score()
