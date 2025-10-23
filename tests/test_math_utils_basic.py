from myapp.math_utils import safe_div

def test_safe_div_simple():
    assert safe_div(4, 2) == 2
