from file_importer import FileImporter
from classifier import Classifier

importer = FileImporter('../Sketch-Data-master/SketchData/Domain01')
classifier = Classifier()

data = importer.get_data()

user = 10
k = 10

data_train = data.query(f'user != {user}')
data_test = data.query(f'user == {user}')
data_test_single = data_test.query('label == 1 and iteration == 1')

results = []

for label in range(1, 11):
    for iteration in range(1, 11):
        data_test_single = data_test.query(
            f'label == {label} and iteration == {iteration}')
        classification = classifier.classify(
            data_test_single, data_train, user, k)

        results.append(classification == label)

        print("TEST #", (label - 1) * 10 + iteration, ":")
        print("original label:", label)
        print("classification:", classification)
        print("classification correct:", classification == label)
        print()

print(results)
print("Correctly classified:", 100 * sum(results) / len(results), "%")
