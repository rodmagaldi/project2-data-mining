import numpy as np
import pandas as pd
import os

# sort files alphabetically
directory = '../Sketch-Data-master/SketchData/Domain01'
list_of_files = sorted(filter(lambda x: os.path.isfile(
    os.path.join(directory, x)), os.listdir(directory)))

# create empty dataframe
dataframe = pd.DataFrame(
    columns=['<x>', '<y>', '<z>', '<t>', 'class', 'user', 'iteration'])

# auxiliary function


def get_iteration(filename):
    return filename.split('.')[0][-1]


# read files and create dataframe with txt files data
for filename in list_of_files:
    lines = []
    with open(f'{directory}/{filename}') as f:
        lines = f.readlines()

    class_id = int(lines[1].split('=')[1])
    user_id = int(lines[2].split('=')[1])
    iteration = get_iteration(filename)

    df = pd.read_csv(f'{directory}/{filename}', header=3)
    df['class'] = class_id
    df['user'] = user_id
    df['iteration'] = iteration

    dataframe = dataframe.append(df)

print(dataframe)
