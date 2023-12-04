from business_score import custom_score



def test_same_y_actual_y_test():
    
    y_actual = [0,1,1,0,0]
    y_pred =    [0,1,1,0,0]

    result = custom_score(y_actual, y_pred)
    expected_values = float(0)

    assert result == expected_values


def test_diff_y_actual_y_test():

    y_actual = [1,1,1,1,0]
    y_pred =    [0,1,1,0,0]

    result = custom_score(y_actual, y_pred)
    expected_values = float(12)
    assert result == expected_values