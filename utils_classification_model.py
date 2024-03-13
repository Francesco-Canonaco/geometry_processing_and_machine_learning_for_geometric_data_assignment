# importing libraries 
from sklearn.neural_network import MLPClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def iterated_hold_out_nn(X:pd.core.frame.DataFrame,y:pd.core.series.Series,iterations:int)->dict:
  results={'training_accuracy':[], 'test_accuracy':[]}
  for iter in range(iterations):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=iter)
    # initialize the MLPClassifier
    mlp_classifier = MLPClassifier(hidden_layer_sizes=(100, 50), activation='relu', solver='adam', alpha=1e-5,random_state=iter)
    # train the neural network
    mlp_classifier.fit(X_train, y_train)
    # predict on the training set
    y_pred_training = mlp_classifier.predict(X_train)
    # calculate accuracy on the training set
    accuracy_training = accuracy_score(y_pred_training, y_train)
    # predict on the test set
    y_pred = mlp_classifier.predict(X_test)
    # calculate accuracy
    accuracy_test = accuracy_score(y_test, y_pred)
    results['training_accuracy'].append(accuracy_training)
    results['test_accuracy'].append(accuracy_test)
  return results

