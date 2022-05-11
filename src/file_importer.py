import pandas as pd
import os


class FileImporter:
    def __init__(self, directory):
        self.directory = directory
        self.list_of_files = sorted(filter(lambda x: os.path.isfile(
            os.path.join(self.directory, x)), os.listdir(self.directory)))
        self.dataframe = pd.DataFrame()

    def get_iteration(self, filename):
        last_digit = int(filename.split('.')[0][-1])
        if last_digit != 0:
            return last_digit
        return 10

    def get_data(self):
        for filename in self.list_of_files:
            lines = []
            with open(f'{self.directory}/{filename}') as f:
                lines = f.readlines()

            class_id = int(lines[1].split('=')[1])
            user_id = int(lines[2].split('=')[1])
            iteration = self.get_iteration(filename)

            df = pd.read_csv(f'{self.directory}/{filename}', header=3)
            df['user'] = user_id
            df['class'] = class_id
            df['iteration'] = iteration

            self.dataframe = self.dataframe.append(df)

        self.dataframe.sort_values(
            ['user', 'class', 'iteration'], inplace=True)

        return self.dataframe
