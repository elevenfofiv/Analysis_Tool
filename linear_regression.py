import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import seaborn as sns

class linearRegression(object):
    
    """
    Tensorflow 이용 linear regression 실행을 위한 Class
    """
    
    def __init__(self,trainData):
        self.trainData = trainData
        
    
    def initData(self):
        """
        Training을 위한 Data 선별 및 Plot화
        """
        x_data = self.trainingData[]