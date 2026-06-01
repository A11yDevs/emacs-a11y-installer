from emacs_a11y.cli.interactive import build_context_tree
from emacs_a11y.models.interactive_cli import InteractiveSessionState


def test_context_tree_contains_root_and_doctor():
    contexts = build_context_tree()
    assert "root" in contexts
    assert "doctor" in contexts
    assert contexts["doctor"].parent == "root"


def test_session_push_and_pop():
    contexts = build_context_tree()
    state = InteractiveSessionState(context_stack=["root"], contexts=contexts)
    state.push("doctor")
    assert state.current_context.name == "doctor"
    assert state.pop() is True
    assert state.current_context.name == "root"
    assert state.pop() is False
