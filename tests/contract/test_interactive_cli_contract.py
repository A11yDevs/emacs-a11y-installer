from emacs_a11y.cli.interactive import build_context_tree


def test_root_and_doctor_command_surface_contract():
    contexts = build_context_tree()

    root = {command.name for command in contexts["root"].commands}
    doctor = {command.name for command in contexts["doctor"].commands}

    assert {"help", "doctor", "back", "exit"}.issubset(root)
    assert {"help", "run", "json", "explain", "back", "exit"}.issubset(doctor)
