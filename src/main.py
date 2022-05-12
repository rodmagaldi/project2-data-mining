from file_importer import FileImporter
from classifier import Classifier

importer = FileImporter('../Sketch-Data-master/SketchData/Domain01')
classifier = Classifier()

data = importer.get_data()

user = 10
k = 50

data_train = data.query(f'user != {user}')
data_test = data.query(f'user == {user}')
data_test_single = data_test.query('label == 1 and iteration == 1')

classification = classifier.classify(data_test_single, data_train, user, k)

print(classification)
