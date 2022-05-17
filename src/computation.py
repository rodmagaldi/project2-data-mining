import numpy as np
from sklearn.preprocessing import  StandardScaler,MaxAbsScaler,MinMaxScaler
import pandas as pd

class Computation:
    def dtw_cost(self, series1, series2):
        n, m = len(series1), len(series2)
        dtw_matrix = np.zeros((n+1, m+1))
        for i in range(n+1):
            for j in range(m+1):
                dtw_matrix[i, j] = np.inf
        dtw_matrix[0, 0] = 0

        for i in range(1, n+1):
            for j in range(1, m+1):
                cost = abs(series1[i-1] - series2[j-1])
                last_min = np.min(
                    [dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1]])
                dtw_matrix[i, j] = cost + last_min
        return dtw_matrix[-1][-1]

    def multivariate_dtw(self, df1, df2):

        df1_norm = pd.DataFrame(self.normalize(df1[['<x>','<y>','<z>']]),columns = ['<x>','<y>','<z>'])
        df2_norm = pd.DataFrame(self.normalize(df2[['<x>','<y>','<z>']]),columns = ['<x>','<y>','<z>'])

        dtw_x = self.dtw_cost(df1_norm['<x>'], df2_norm['<x>'])
        dtw_y = self.dtw_cost(df1_norm['<y>'], df2_norm['<y>'])
        dtw_z = self.dtw_cost(df1_norm['<z>'], df2_norm['<z>'])

        return (dtw_x + dtw_y + dtw_z)

    def normalize(self,df):

        scaler = MinMaxScaler()
        scaler.fit(df)

        return scaler.transform(df)


