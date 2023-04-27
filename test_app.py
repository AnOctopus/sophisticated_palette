from streamlit.testing.script_interactions import InteractiveScriptTests
from streamlit.web.bootstrap import _fix_matplotlib_crash

# Fix the issue with tkinter, until this is called for you by the framework
_fix_matplotlib_crash()


def get_sorted_colors(script_result):
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
        script = self.script_from_filename("app.py")
        sr = script.run()
        assert not sr.exception

    def test_palette_size(self):
        script = self.script_from_filename("app.py")
        sr = script.run()

        sr2 = sr.sidebar.number_input[0].set_value(2).run()
        assert len(sr2.color_picker) == 2

        sr3 = sr2.sidebar.number_input[0].set_value(15).run()
        assert len(sr3.color_picker) == 15

    def test_selected_colors(self):
        script = self.script_from_filename("app.py")
        sr = script.run()
        colors = get_sorted_colors(sr)

        sr2 = sr.get("tab")[0].selectbox[0].select_index(1).run()
        colors2 = get_sorted_colors(sr2)
        assert colors != colors2

    def test_load_url(self):
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
