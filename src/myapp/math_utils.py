def safe_div(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("b cannot be zero")
    return a / b
