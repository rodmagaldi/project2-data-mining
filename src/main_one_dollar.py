from file_importer import FileImporter
from classifier import Classifier
from one_dollar import OneDollar
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

importer = FileImporter('Projeto 2\git\project2-data-mining\Sketch-Data-master\SketchData\Domain01')
classifier = Classifier()

data = importer.get_data()

user = 1

data_train = data.query(f'user != {user}')
data_test = data.query(f'user == {user}')

results = []

one_dollar = OneDollar()
for label in range(1, 11):
    for iteration in range(1, 11):
        data_test_single = data_test.query(
            f'label == {label} and iteration == {iteration}')
        classification = one_dollar.classify(
            data_test_single, data_train, user)

        results.append(classification == label)

        print("TEST #", (label - 1) * 10 + iteration, ":")
        print("original label:", label)
        print("classification:", classification)
        print("classification correct:", classification == label)
        print()

print(results)
print("Correctly classified:", 100 * sum(results) / len(results), "%")


