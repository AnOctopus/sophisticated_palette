# Streamlit Unit Testing Framework (Preview) Demo

This repo demonstrates the capabilities and usage of Streamlit's new testing framework. The framework enables
developers to:

- Run your app as a headless script
- Inspect and make assertions about the output content via the DOM in object-attribute style
- Programmatically modify the input values on various widgets, re-run the app, and inspect the output

The testing framework extends [unittest.TestCase](https://docs.python.org/3/library/unittest.html#test-cases)
and thus can be run simply using [pytest](https://docs.pytest.org/en/7.3.x/) or similar tools. The testing
framework ships with core Streamlit (and in fact is used heavily in Streamlit's internal unit testing) -
the functionality shown here can be installed from [streamlit-nightly](https://pypi.org/project/streamlit-nightly/)
or versions >= 1.23.

The example is built on the existing [sophisticated_palette app](https://github.com/syasini/sophisticated_palette)
originally built by @syasini and hosted on Streamlit Community Cloud: https://sophisticated-palette.streamlit.app/

**⚠️ Important Note ⚠️: The testing framework API is not currently documented nor guaranteed to be stable.**
This repo is shared for evaluation and gathering feedback about the feature. We have been using it
internally and expect to stabilize and document the API in the coming months, HOWEVER we discourage
any large scale adoption or production usage that would be painful to adapt to API changes in future versions.

## A simple example

A simple example that demonstrates the anatomy of a unit test and the key features of the unit testing framework

```python
# Everything is exposed via InteractiveScriptTests
from streamlit.testing.script_interactions import InteractiveScriptTests

class AppTest(InteractiveScriptTests):
    def test_sidebar(self):
        """Simple test of the sidebar controlling the palettes rendered"""

        # Load and run the script from a file path
        script = self.script_from_filename("app.py")
        sr = script.run()

        # No exceptions were rendered in the app output
        assert not sr.exception

        # Five color pickers are rendered on the first run
        assert len(sr.color_picker) == 5

        # You can also query a widget by key to modify it or check the value
        assert sr.get_widget("sample_size").value == 500

        # Set the value of the first number input in the sidebar
        # (palette size) to 2, and re-run the app
        sr2 = sr.sidebar.number_input[0].set_value(2).run()

        # Two color pickers are rendered in the second run
        assert len(sr2.color_picker) == 2
```

The best documentation currently on the capabilites and API is
[the code itself](https://github.com/streamlit/streamlit/tree/develop/lib/streamlit/testing).

See `test_app.py` for the tests and some further explanation.

## Run it yourself

I recommend installing to a venv and then running the test suite with pytest.

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## 🎈 Let us know what you think! 🎈
