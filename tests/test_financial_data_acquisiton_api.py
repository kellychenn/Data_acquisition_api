from financial_data_acquisiton_api import financial_data_acquisiton_api

"""
This test is to test the input type of the api. The input type should be string,
if not, it will raise error in the test. 
"""

def check_user_input(input):
    if type(input) == str:
        return True
    else:
        print("Pleas input a string.")

def test_api_input():
    example = 'apple'
    expected = True
    actual = check_user_input(example)
    assert actual == expected
