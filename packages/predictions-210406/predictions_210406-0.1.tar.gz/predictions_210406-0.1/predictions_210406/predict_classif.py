from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from .predict import Predict


class Predict_Classif(Predict):

    def __init__(self, data_train_path, dependent):
        Predict.__init__(self, data_train_path, dependent)
        self.svm = 'no value assigned yet'
        self.dtc = 'no value assigned yet'
        self.acc_svm = 'no value assigned yet'
        self.acc_dtc = 'no value assigned yet'

    """
    Prediction class for training of and inferencing with two types of classification models:
        Support Vector Machine (non-linear w/ polynomial kernel)
        Decision Tree Classifier

    Attributes:
        dependent (string): name of dependent variable (inherited from parent class Predict)
        data_train_path (string): path to training data set (inherited from parent class Predict)
        svm (Pipeline object): Pipeline object including StandardScaler and SVM classification
        dtc (model object): DecisionTreeClassifier model object
        acc_svm (float): accuracy of support vector machine
        acc_dtc (float): accuracy of decision tree classifer
    """

    def train_svm(self, degr, c, c0 = 0):
        """
        Function to: 
            (i) fit support vector machine model to training data
            (ii) calculate accuracy score on training data
        Args: 
			degr (float): degree of polynomial kernel function
            c (float): Regularization parameter (the smaller c the stronger the regularization)
            c0 (float): Independent term in kernel function
		Returns: 
			None
        https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
        """        
        self.svm = Pipeline([
            ('scaler', StandardScaler()),
            ('svm_clf', SVC(kernel = 'poly',
                            degree = degr, 
                            coef0 = c0, 
                            C = c)
            )
        ])
        self.svm.fit(self.data_train_x, self.data_train_y)
        self.acc_svm = self.svm.score(self.data_train_x, self.data_train_y)

    def train_dtc(self, md):
        """
        Function to: 
            (i) fit decision tree classification model to training data
            (ii) calculate accuracy score on training data
        Args: 
			md (float): maximum depth of tree
		Returns: 
			None
        https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html?highlight=decisiontree#sklearn.tree.DecisionTreeClassifier
        """        
        self.dtc = DecisionTreeClassifier(max_depth = md)
        self.dtc.fit(self.data_train_x, self.data_train_y)
        self.acc_dtc = self.dtc.score(self.data_train_x, self.data_train_y)

    def predict_svm(self):
        """
        Function to: 
            predict outcome with fitted support vector machine model
        Args: 
			None
		Returns: 
			pred_svm (Numpy array): Array of predicted values
        """    
        pred_svm = self.svm.predict(self.data_pred)
        return pred_svm

    def predict_dtc(self):
        """
        Function to: 
            predict outcome with fitted decision tree classification model
        Args: 
			None
		Returns: 
			pred_dtc (Numpy array): Array of predicted values
        """    
        pred_dtc = self.dtc.predict(self.data_pred)
        return pred_dtc