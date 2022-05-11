from file_importer import FileImporter
from dtw import Computation

importer = FileImporter('../Sketch-Data-master/SketchData/Domain01')
computation = Computation()

data = importer.get_data()
data_1_1_1 = data.query('user == 1 and label == 1 and iteration == 1')
data_1_1_2 = data.query('user == 1 and label == 1 and iteration == 2')
data_2_1_1 = data.query('user == 2 and label == 1 and iteration == 1')


data_1_2_1 = data.query('user == 1 and label == 2 and iteration == 1')


list_1_1_1 = list(data_1_1_1['<x>'])
list_1_1_2 = list(data_1_1_2['<x>'])

cost = computation.multivariate_dtw(data_1_1_1, data_1_2_1)
print(cost)
