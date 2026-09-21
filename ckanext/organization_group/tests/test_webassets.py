from pathlib import Path


WEBASSETS_FILE = (
    Path(__file__).parents[1] / "public" / "statics" / "webassets.yml"
)


def test_webassets_do_not_reference_obsolete_jquery_ui_bundle():
    assert "vendor/jquery.ui.core" not in WEBASSETS_FILE.read_text()

