from __future__ import annotations

import sys
import types
from pathlib import Path


def test_recovered_solution_embedded_tester(capsys) -> None:
    tkinter_stub = types.ModuleType("tkinter")
    tkinter_stub.PhotoImage = object
    tkinter_stub.Toplevel = object
    tkinter_stub.Label = object
    tkinter_stub.Tk = object
    sys.modules["tkinter"] = tkinter_stub

    repository_path = Path(__file__).resolve().parents[1]
    assignment_path = repository_path / "assignment"
    solution_path = repository_path / "solution"
    sys.path.insert(0, str(assignment_path))
    sys.path.insert(0, str(solution_path))
    try:
        import hw6 as recovered_hw6

        recovered_hw6.test()
        captured = capsys.readouterr()
        assert captured.out == ""
    finally:
        sys.path.remove(str(solution_path))
        sys.path.remove(str(assignment_path))
        sys.modules.pop("hw6", None)
        sys.modules.pop("matrix", None)
        sys.modules.pop("huffman", None)
