import pytest
from sklearn.metrics import confusion_matrix 



def custom_score(y_actual, y_pred):
    
    tp,fp,fn,tn = confusion_matrix(y_actual, y_pred).ravel()
    cost = ((1/10)*fn + fp + tp )/len(y_actual)

    return float(cost)


def test_same_y_actual_y_test():

    y_actual = [0,1,1,0,0]
    y_pred =    [0,1,1,0,0]

    result = custom_score(y_actual, y_pred)
    expected_values = float(3/5)

    assert result == expected_values

 