# Streamlit App Testing Framework (Preview) Demo

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sfc-gh-jcarroll/st-testing-demo/tree/update-api?quickstart=1)

This repo demonstrates the capabilities and usage of Streamlit's new testing framework. The framework enables
developers to:

- Run your app as a headless script
- Inspect and make assertions about the output content via the DOM in object-attribute style
- Programmatically modify the input values on various widgets, re-run the app, and inspect the output

The testing framework works well with [unittest.TestCase](https://docs.python.org/3/library/unittest.html#test-cases)
and [pytest](https://docs.pytest.org/en/7.3.x/) or similar tools. The testing framework ships with
core Streamlit (and in fact is used heavily in Streamlit's internal unit testing) -
the functionality shown here can be installed from the provided whl.

The example is built on the existing [sophisticated_palette app](https://github.com/syasini/sophisticated_palette)
originally built by @syasini and hosted on Streamlit Community Cloud: https://sophisticated-palette.streamlit.app/

**⚠️ Important Note ⚠️: The testing framework API is not currently documented nor guaranteed to be stable.**
This repo is shared for evaluation and gathering feedback about the feature. We have been using it
internally and expect to stabilize and document the API in the coming months, HOWEVER we discourage
any large scale adoption or production usage that would be painful to adapt to API changes in future versions.

## A simple example

A simple example that demonstrates the anatomy of a unit test and the key features of the unit testing framework

```python
import unittest
from streamlit.testing.v1 import AppTest

class TestSuite(unittest.TestCase):
    def test_sidebar(self):
        """Simple test of the sidebar controlling the palettes rendered"""

        # Load and run the script from a file path
        at = AppTest.from_file("app.py").run()

        # No exceptions were rendered in the app output
        assert not at.exception

        # Five color pickers are rendered on the first run
        assert len(at.color_picker) == 5

        # You can also query a widget by key to modify it or check the value
        assert at.number_input(key="sample_size").value == 500

        # Set the value of the first number input in the sidebar
        # (palette size) to 2, and re-run the app
        at.sidebar.number_input[0].set_value(2).run()

        # Two color pickers are rendered in the second run
        assert len(at.color_picker) == 2
```

Read the fuller documentation on the preview [here](#TODO-add-link).

See `test_app.py` for the tests and some further explanation.

## Run it using GitHub Codespaces

TODO: Add info on codespaces

## Run it locally

I recommend installing to a venv and then running the test suite with pytest.

```sh
git clone https://github.com/AnOctopus/st-testing-demo.git
cd st-testing-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Using it with CI

The testing framework just uses pytest, so any CI tools that work with python should just work. You can see
a Github Action workflow in this repo that runs the tests using
[GitHub's python starter workflow](https://github.com/actions/starter-workflows/blob/main/ci/python-app.yml)
with zero modifications, and it works great.

You can view the [Github Actions configuration for this repository](https://github.com/AnOctopus/st-testing-demo/blob/main/.github/workflows/python-app.yml#L37-L39),
and [recent CI runs including the test execution](https://github.com/AnOctopus/st-testing-demo/actions/workflows/python-app.yml).

## 🎈 Let us know what you think! 🎈

- TODO: Add links to feedback places
