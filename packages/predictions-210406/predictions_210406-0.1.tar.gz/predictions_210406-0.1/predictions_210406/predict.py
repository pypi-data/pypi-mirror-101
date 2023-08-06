import pandas as pd


class Predict:

    def __init__(self, data_train_path, dependent):
        self.dependent = dependent
        self.data_train_path = data_train_path
        self.data_train_x = 'no value assigned yet'
        self.data_train_y = 'no value assigned yet'
        self.data_pred_path = 'no value assigned yet'
        self.data_pred = 'no value assigned yet'

    """
    Generic Predict class for training of and inferencing with various predictive models
    Parent class of Predict_Classif and Predict_Regr

    Attributes:
        dependent (string): name of dependent variable
        data_train_path (string): path to training data set
        data_train_x (pandas DataFrame): n x m dimensional matrix of training dataset, excluding 
            dependent variable (n - # of training instances, m - # of features)
        data_train_y (Numpy array): n dimensional array of dependent variable
        data_pred_path (string): path to prediction data set
        data_pred (string): n x m dimensional matrix of feature values to predict dependent variable
    """
    
    def load_data_train(self):
        """
        Function to: 
            (i) load in training dataset from drive (accepted formats: xlsx, xls, csv)
            (ii) split into features dataset and array of dependent variable
        Args: 
			None
		Returns: 
			None
        """
        if self.data_train_path[-5:] == '.xlsx':
            self.data_train = pd.read_excel(self.data_train_path)
        elif self.data_train_path[-4:] == '.xls':
            self.data_train = pd.read_excel(self.data_train_path)
        elif self.data_train_path[-4:] == '.csv':
            self.data_train = pd.read_csv(self.data_train_path)
        else:
            print('[ERROR] Please provide data in format csv, xlsx, or xls.')
        self.data_train_x = self.data_train.loc[:,self.data_train.columns != self.dependent]
        self.data_train_y = self.data_train.loc[:,self.data_train.columns == self.dependent].values.flatten()

    def load_data_pred(self, data_pred_path):
        """
        Function to: 
            load in prediction dataset from drive (accepted formats: xlsx, xls, csv)
        Args: 
			data_pred_path
		Returns: 
			None
        """
        self.data_pred_path = data_pred_path
        if self.data_pred_path[-5:] == '.xlsx':
            self.data_pred = pd.read_excel(self.data_pred_path)
        elif self.data_pred_path[-4:] == '.xls':
            self.data_pred = pd.read_excel(self.data_pred_path)
        elif self.data_pred_path[-4:] == '.csv':
            self.data_pred = pd.read_csv(self.data_pred_path)
        else:
            print('[ERROR] Please provide data in format csv, xlsx, or xls.')