# Minimal local generator (no API) that inspects your repo and creates a param test.
import pathlib, re, json
from jinja2 import Template

# --- find target functions in changed file(s) (very simple for demo) ---
SRC = pathlib.Path("src/myapp/math_utils.py")
code = SRC.read_text(encoding="utf-8")
funcs = re.findall(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\(", code)

# --- if our demo function exists, propose parameterized tests ---
plan = {
  "tests": [
    {
      "file_path": "tests/test_math_utils_param.py",
      "imports": ["import pytest", "from myapp.math_utils import safe_div"],
      "parametrized": {
        "name": "test_safe_div_param",
        "target": "safe_div",
        "params": [
          {"args": [4, 2], "kwargs": {}, "expect": 2},
          {"args": [1, 1], "kwargs": {}, "expect": 1},
          {"args": [5, -1], "kwargs": {}, "expect": -5},
          {"args": [0, 3], "kwargs": {}, "expect": 0},
          {"args": [10, 0], "kwargs": {}, "expect": "raises:ZeroDivisionError"}
        ]
      },
      "edge_cases": ["zero divisor", "negative numbers", "zero numerator"]
    }
  ]
}


from jinja2 import Environment, StrictUndefined

env = Environment(undefined=StrictUndefined)
env.filters["py"] = lambda v: repr(v)  # render as valid Python literal

PYTEST_TEMPLATE = env.from_string("""\
{% for imp in test.imports %}{{ imp }}
{% endfor %}

import pytest

@pytest.mark.parametrize("args,kwargs,expect", [
{%- for p in test.parametrized.params -%}
    ({{ p.get("args", []) | py }}, {{ p.get("kwargs", {}) | py }}, {{ p.get("expect") | py }}),
{%- endfor -%}
])
def {{ test.parametrized.name }}(args, kwargs, expect):
    from myapp.math_utils import {{ test.parametrized.target }}
    if isinstance(expect, str) and expect.startswith("raises:"):
        exc = getattr(__import__('builtins'), expect.split(":",1)[1])
        with pytest.raises(exc):
            {{ test.parametrized.target }}(*args, **kwargs)
    else:
        assert {{ test.parametrized.target }}(*args, **kwargs) == expect
""")


out_file = pathlib.Path(plan["tests"][0]["file_path"])
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(PYTEST_TEMPLATE.render(test=plan["tests"][0]), encoding="utf-8")

print("Generated:", out_file)
