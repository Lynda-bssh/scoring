from sklearn.metrics import confusion_matrix


def custom_score(y_actual, y_pred):
    
    tp,fp,fn,tn = confusion_matrix(y_actual, y_pred).ravel()
    cost = (10*fn) + fp 

    return float(cost)