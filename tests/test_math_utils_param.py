import pytest
from myapp.math_utils import safe_div


@pytest.mark.parametrize("args,kwargs,expect", [([4, 2], {}, 2),([1, 1], {}, 1),([5, -1], {}, -5),([0, 3], {}, 0),([10, 0], {}, raises:ZeroDivisionError),])
def test_safe_div_param(args, kwargs, expect):
    from myapp.math_utils import safe_div
    import pytest
    if isinstance(expect, str) and expect.startswith("raises:"):
        exc = getattr(__import__('builtins'), expect.split(":")[1])
        with pytest.raises(exc):
            safe_div(*args, **kwargs)
    else:
        assert safe_div(*args, **kwargs) == expect