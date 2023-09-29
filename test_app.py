import unittest
from streamlit.testing.v1 import AppTest
from streamlit.web.bootstrap import _fix_matplotlib_crash

# Fix the issue with tkinter, until this is called for you by the framework
_fix_matplotlib_crash()

def get_sorted_colors(at: AppTest):
    """
    Comparing the selected colors is a good heuristic for things changing correctly, so we want it to be easy to get the colors from a script run.
    """
    colors = {
        k: at.session_state[k]
        for k in at.session_state
        if k.startswith("col_")
    }
    sorted_colors = {
        k: colors[k] for k in sorted(colors, key=lambda k: int(k.split("_")[-1]))
    }
    return sorted_colors


class StreamlitTestSuite(unittest.TestCase):
    def test_smoke(self):
        """Basic smoke test"""
        at = AppTest.from_file("app.py", default_timeout=10).run()
        # Supported elements are primarily exposed as properties on the script
        # results object, which returns a sequence of that element.
        assert not at.exception

    def test_palette_size(self):
        at = AppTest.from_file("app.py", default_timeout=10).run()
        # TODO: Fix sidebar
        # It is easier to find the widget we want by first selecting the
        # sidebar, then querying within that.
        # at.sidebar.number_input[0].set_value(2).run()
        at.number_input[0].set_value(2).run()
        
        assert len(at.color_picker) == 2

        # You can also query a widget by key to modify it or check the value
        assert at.number_input(key="sample_size").value == 500
        at.number_input(key="sample_size").set_value(450)

        # For widgets that don't yet have high level interaction methods, we
        # can fall back to the primitive `set_value`.
        #at.sidebar.number_input[0].set_value(15).run()
        at.number_input[0].set_value(15).run()
        assert len(at.color_picker) == 15
        assert at.number_input(key="sample_size").value == 450

    def test_selected_colors(self):
        """Changing the source image should change the colors it picks"""
        at = AppTest.from_file("app.py", default_timeout=10).run()
        colors = get_sorted_colors(at)

        # Elements that don't have explicit implementations yet, like `tab`,
        # are still parsed and can be queried using `.get`.
        at.get("tab")[0].selectbox[0].select_index(1).run()
        colors2 = get_sorted_colors(at)
        assert colors != colors2

    def test_load_url(self):
        """We can load an image from a URL"""
        at = AppTest.from_file("app.py", default_timeout=10).run()
        colors = get_sorted_colors(at)

        ST_LOGO_URL = "https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png"
        at.get("tab")[2].text_input[0].input(ST_LOGO_URL).run()
        assert not at.exception
        colors2 = get_sorted_colors(at)
        assert colors != colors2

    def test_seed(self):
        """Changing the seed will probably change the colors selected"""
        at = AppTest.from_file("app.py", default_timeout=10).run()
        colors = get_sorted_colors(at)

        at.run()
        colors2 = get_sorted_colors(at)
        assert colors == colors2

        #at.sidebar.number_input[2].set_value(0).run()
        at.number_input[2].set_value(0).run()
        colors3 = get_sorted_colors(at)
        assert colors != colors3

    def test_model(self):
        """Changing the model will probably change the selected colors."""
        at = AppTest.from_file("app.py", default_timeout=10).run()
        colors_kmeans = get_sorted_colors(at)

        # TODO: Note changed index to 1 since it checks main before sidebar
        #at.sidebar.selectbox[0].select_index(1).run()
        at.selectbox[1].select_index(1).run()
        colors_bisect = get_sorted_colors(at)
        assert colors_kmeans != colors_bisect

        # You can also select a value explicitly
        #at.sidebar.selectbox[0].select_index(2).run()
        at.selectbox[1].select("GaussianMixture").run()
        colors_gaussian = get_sorted_colors(at)
        assert colors_bisect != colors_gaussian

        #at.sidebar.selectbox[0].select_index(3).run()
        at.selectbox[1].select_index(3).run()
        colors_mini = get_sorted_colors(at)
        assert colors_gaussian != colors_mini
