import numpy as np
from sklearn.decomposition import PCA

class OneDollar:
    def __init__ (self):
        self.n = 64
        self.phi =  0.5*(-1 + np.sqrt(5))
        self.theta = np.pi/4
        self.theta_delta = np.pi/90

    def pca(self,df):
        pca_ = PCA()
        pca_transformed = pca_.fit_transform(df)
        return pca_transformed[:,0:2]

    def distance(self,a,b):
        return np.linalg.norm(np.array(b) - np.array(a))

    def path_length(self,A):
        d = 0
        for i in range (1,len(A)):
            d += self.distance(A[i-1],A[i])
        return d 

    def resample(self,points):
        points_actual = np.copy(points).tolist()
        I = self.path_length(points)/ float(self.n-1)
        D = 0
        newPoints = [points_actual[0]]
        for i in range(1,len(points_actual)):
            d = self.distance(points_actual[i-1],points_actual[i])
            if (D + d) >= I:
                qx = points_actual[i-1][0] + ((I - D)/d) * (points_actual[i][0] - points_actual[i-1][0])
                qy = points_actual[i-1][1] + ((I - D)/d) * (points_actual[i][1] - points_actual[i-1][1])
        
                newPoints.append([qx,qy])
                points_actual.insert(i, [qx,qy])
                D = 0
            else:
                D += d
        return newPoints

    def rotate_to_zero(self,points):
        c = np.mean(points,axis=0).tolist()
        theta = np.arctan((c[1]-points[0][1])/(c[0]-points[0][0])).tolist()
        newPoints = self.rotate_by(points,-theta)
        return newPoints

    def rotate_by(self,points,theta):
        c = np.mean(points,axis=0).tolist()
        newPoints = [] 
       
        for i in range(len(points)):
            qx = (points[i][0] - c[0])*np.cos(theta) - (points[i][1] - c[1])*np.sin(theta) + c[0]
            qy = (points[i][0] - c[0])*np.sin(theta) - (points[i][1] - c[1])*np.cos(theta) + c[1]
            newPoints.append([qx,qy])

        return newPoints

    def scale_to_square(self,points,size):
        max_x, max_y = np.max(points, 0)
        min_x, min_y = np.min(points, 0)
        newPoints = [] 
        for p in points:
            qx = p[0] * (size/ (max_x - min_x))
            qy = p[1] * (size/ (max_y - min_y))
            newPoints.append([qx,qy])
        return newPoints

    def translate_to_origin(self,points):
        newPoints = []
        c = np.mean(points,axis=0).tolist()
        for p in points:
            qx = p[0] - c[0]
            qy = p[1] - c[1]
            newPoints.append([qx,qy])
        return newPoints
    
    def recognize(self,points,templates):
        for i in templates:
            print(len(i))

        b = np.inf
        for T in templates:

            d = self.distance_at_best_angle(points,T,-self.theta,self.theta,self.theta_delta)
            if d<b:
                b = d 
                T_ = T 
        score = 1- b/(0.5*np.sqrt(size**2 + size**2))
        return (score,T_)
    
    def distance_at_best_angle(self,points,T,theta_a,theta_b,theta_delta):
        print(len(points),len(points[0]))
        print(len(T),len(T[0]))
        x1 = self.phi*theta_a + (1-self.phi)*theta_b
        f1 = self.distance_at_angle(points,T,x1)
        x2 = (1-self.phi)*theta_a + self.phi*theta_b
        f2 = self.distance_at_angle(points,T,x2)
        while abs(theta_b-theta_a) > theta_delta:
            if f1<f2:
                theta_b = x2
                x2 = x1
                f2 = f1
                x1 = self.phi*theta_a + (1-self.phi)*theta_b
                f1 = self.distance_at_angle(points,T,x1)
            else:
                theta_a = x1 
                x1 = x2
                f1 = f2
                x2 = (1-self.phi)*theta_a + self.phi*theta_b
                f2 = self.distance_at_angle(points,T, x2)
        return min(f1,f2)

    def distance_at_angle(self,points,T,theta):
        newPoints = self.rotate_by(points,theta)
        d = self.path_distance(newPoints,T)
        return d
    
    def path_distance(self,A,B):
        print(len(A),len(B))
        d = 0
        for i in range(len(A)):
            d += self.distance(A[i],B[i])
        return d/len(A)

    def all_algorithms(self,points):
        data_pca = self.pca(points).tolist()
        data_resampled = self.resample(data_pca)
        data_rotated = self.rotate_to_zero(data_resampled)
        data_scaled = self.scale_to_square(data_rotated, size = 200)
        data_translated = self.translate_to_origin(data_scaled)
        return data_translated

    def classify(self,dataframe_test_single, dataframe_train, current_user):
        for user in range(1, 11):
            if current_user == user:
                continue
            for iteration in range(1,11):
                templates = []
                for label in range(1,11):
                    df = dataframe_train.query(f'user == {user} and label == {label} and iteration == {iteration}')
                    df_treated = self.all_algorithms(df[['<x>','<y>', '<z>']].values.tolist())
                    templates.append(df_treated) 

                df_single_treated =  self.all_algorithms(dataframe_test_single[['<x>','<y>', '<z>']])
                cost = self.recognize(df_single_treated,templates)
                
        return df

