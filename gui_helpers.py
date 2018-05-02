import os

def gui_get_file_path(msg=None):
    if not msg:
        msg = 'enter file path'
    while True:
        path = input(msg)
        if os.path.isfile(path):
            break
    return path

def gui_get_column(dataset, msg=None):
    if not msg:
        msg = 'Enter Column name'
    while True:
        print(10*"=")
        print('Columns:', dataset.columns)

        target_column = input(msg + ':  ')
        if target_column in dataset.columns:
            break
        else:
            print('Wrong answer!')
    return target_column