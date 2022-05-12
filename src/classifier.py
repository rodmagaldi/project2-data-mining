from computation import Computation


class Classifier:

    def __init__(self):
        self.computation = Computation()

    def compute_distances(self, dataframe_test_single, dataframe_train, current_user):
        distances = []

        for user in range(1, 11):
            if current_user == user:
                continue

            print('user', user)

            for label in range(1, 11):
                for iteration in range(1, 11):

                    df = dataframe_train.query(
                        f'user == {user} and label == {label} and iteration == {iteration}')
                    cost = self.computation.multivariate_dtw(
                        df, dataframe_test_single)
                    distances.append((cost, label))

        return sorted(distances)

    def classify(self, dataframe_test_single, dataframe_train, current_user, k):
        distances = self.compute_distances(
            dataframe_test_single, dataframe_train, current_user)[:k]
        labels = [item[-1] for item in distances]
        classification = max(set(labels), key=labels.count)
        return classification
