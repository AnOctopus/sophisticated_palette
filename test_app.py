from streamlit.testing.script_interactions import InteractiveScriptTests
from streamlit.web.bootstrap import _fix_matplotlib_crash

# Fix the issue with tkinter, until this is called for you by the framework
_fix_matplotlib_crash()


def get_sorted_colors(script_result):
    """
    Comparing the selected colors is a good heuristic for things changing correctly, so we want it to be easy to get the colors from a script run.
    """
    colors = {
        k: script_result.session_state[k]
        for k in script_result.session_state
        if k.startswith("col_")
    }
    sorted_colors = {
        k: colors[k] for k in sorted(colors, key=lambda k: int(k.split("_")[-1]))
    }
    return sorted_colors


class AppTest(InteractiveScriptTests):
    def test_smoke(self):
        """Basic smoke test"""
        script = self.script_from_filename("app.py")
        sr = script.run()
        # Supported elements are primarily exposed as properties on the script
        # results object, which returns a sequence of that element.
        assert not sr.exception

    def test_palette_size(self):
        script = self.script_from_filename("app.py")
        sr = script.run()

        # It is easier to find the widget we want by first selecting the
        # sidebar, then querying within that.
        sr2 = sr.sidebar.number_input[0].set_value(2).run()
        assert len(sr2.color_picker) == 2

        # For widgets that don't yet have high level interaction methods, we
        # can fall back to the primitive `set_value`.
        sr3 = sr2.sidebar.number_input[0].set_value(15).run()
        assert len(sr3.color_picker) == 15

    def test_selected_colors(self):
        """Changing the source image should change the colors it picks"""
        script = self.script_from_filename("app.py")
        sr = script.run()
        colors = get_sorted_colors(sr)

        # Elements that don't have explicit implementations yet, like `tab`,
        # are still parsed and can be queried using `.get`.
        sr2 = sr.get("tab")[0].selectbox[0].select_index(1).run()
        colors2 = get_sorted_colors(sr2)
        assert colors != colors2

    def test_load_url(self):
        """We can load an image from a URL"""
        script = self.script_from_filename("app.py")
        sr = script.run()
        colors = get_sorted_colors(sr)

        sr2 = (
            sr.get("tab")[2]
            .text_input[0]
            # streamlit logo
            .input(
                "https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png"
            )
            .run()
        )
        assert not sr2.exception
        colors2 = get_sorted_colors(sr2)
        assert colors != colors2

    def test_seed(self):
        """Changing the seed will probably change the colors selected"""
        script = self.script_from_filename("app.py")
        sr = script.run()
        colors = get_sorted_colors(sr)

        sr2 = sr.run()
        colors2 = get_sorted_colors(sr2)
        assert colors == colors2

        sr3 = sr2.sidebar.number_input[2].set_value(0).run()
        colors3 = get_sorted_colors(sr3)
        assert colors != colors3

    def test_model(self):
        """Changing the model will probably change the selected colors."""
        script = self.script_from_filename("app.py")
        sr = script.run()
        colors_kmeans = get_sorted_colors(sr)

        sr2 = sr.sidebar.selectbox[0].select_index(1).run()
        colors_bisect = get_sorted_colors(sr2)
        assert colors_kmeans != colors_bisect

        sr3 = sr2.sidebar.selectbox[0].select_index(2).run()
        colors_gaussian = get_sorted_colors(sr3)
        assert colors_bisect != colors_gaussian

        sr4 = sr3.sidebar.selectbox[0].select_index(3).run()
        colors_mini = get_sorted_colors(sr4)
        assert colors_gaussian != colors_mini
