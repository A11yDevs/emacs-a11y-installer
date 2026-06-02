from importlib import resources


def test_packaged_resources_are_discoverable_with_importlib_resources():
    root = resources.files("emacs_a11y.resources").joinpath("a11y-emacs")
    assert root.joinpath("early-init.el").is_file()
    assert root.joinpath("init.el").is_file()
    assert root.joinpath("lisp").is_dir()
