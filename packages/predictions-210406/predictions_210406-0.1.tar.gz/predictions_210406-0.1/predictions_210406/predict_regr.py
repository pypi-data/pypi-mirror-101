from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

from .predict import Predict


class Predict_Regr(Predict):

    def __init__(self, data_train_path, dependent):
        Predict.__init__(self, data_train_path, dependent)
        self.svmr = 'no value assigned yet'
        self.lreg = 'no value assigned yet'
        self.acc_svmr = 'no value assigned yet'
        self.acc_lreg = 'no value assigned yet'

    """
    Prediction class for training and inferencing two types of regression models:
        Support Vector Machine Regression (non-linear w/ polynomial kernel)
        Linear Regression w/ polynomial features

    Attributes:
        dependent (string): name of dependent variable (inherited from parent class Predict)
        data_train_path (string): path to training data set (inherited from parent class Predict)
        svmr (model object): Support vector machine regression model object
        lreg (model object): LinearRegression model object (fit with OLS)
        acc_svmr (float): coefficient of determination (R2) of support vector machine regression
        acc_lreg (float): coefficient of determination (R2) of linear regression
    """

    def train_svmr(self, degr, c):
        """
        Function to: 
            (i) fit support vector machine regression model to training data
            (ii) calculate coefficient of determination (R2) of SVM regression on training data
        Args: 
			degr (float): degree of polynomial kernel function
            c (float): Regularization parameter (the smaller c the stronger the regularization)
		Returns: 
			None
        https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html#sklearn.svm.SVR
        """     
        self.svmr = SVR(kernel = "poly", 
                       degree = degr, 
                       C = c, 
                       epsilon = 0.1
                       )
        self.svmr.fit(self.data_train_x, self.data_train_y)
        self.acc_svmr = self.svmr.score(self.data_train_x, self.data_train_y)

    def train_lreg(self, degr, bias):
        """
        Function to: 
            (i) fit linear regression model (w/ polynomial features) to training dataw with OLS
            (ii) calculate coefficient of determination (R2) of linear regression model on training data
        Args: 
			degr (float): degree of polynomial
            bias (Boolean): Include intercept / bias term (yes or no)
		Returns: 
			None
        https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
        https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html
        """
        self.lreg = Pipeline([
            ("poly_features", PolynomialFeatures(degree = degr, include_bias = bias)),
            ("lin_reg", LinearRegression()),
            ])
        self.lreg.fit(self.data_train_x, self.data_train_y)
        self.acc_lreg = self.lreg.score(self.data_train_x, self.data_train_y)

    def predict_svmr(self):
        """
        Function to: 
            predict outcome with fitted support vector machine regression model
        Args: 
			None
		Returns: 
			pred_svmr (Numpy array): Array of predicted values
        """
        pred_svmr = self.svmr.predict(self.data_pred)
        return pred_svmr

    def predict_lreg(self):
        """
        Function to: 
            predict outcome with linear regression model
        Args: 
			None
		Returns: 
			pred_lreg (Numpy array): Array of predicted values
        """
        pred_lreg = self.lreg.predict(self.data_pred)
        return pred_lreg