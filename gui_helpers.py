import os

def gui_choose_option(options, msg=None):
    if msg:
        print(msg)
    print('Options:')
    for option in options:
        print(options)
    while True:
        choice = input('Choose an option: ')
        print('-- you have chosen %s' % choice)
        if choice in options:
            break
    return choice
    

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

def gui_get_integer(default=None, min=0, max=10, msg='Enter degree', *args, **kwargs):
    while True:
        value = input('{msg}(min:{min}, max:{max}, default:{default}: '.format(msg=msg, min=min, max=max, default=default))
        
        if value == '' and default:
            value = default
        
        try:
            int_value = int(value)
            if int_value >= min and int_value <= max:
                break
        except ValueError:
            pass
    return int_value