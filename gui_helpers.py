
def gui_get_column(dataset):
    while True:
        print(10*"=")
        print('Columns:', dataset.columns)

        target_column = input('What is the target column:  ')
        if target_column in dataset.columns:
            
            break
        else:
            print('Wrong answer!')
    return target_column