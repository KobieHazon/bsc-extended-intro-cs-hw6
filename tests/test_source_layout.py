"""Run the CLI both as a flat source file and as an installed module."""

import subprocess
import sys
from pathlib import Path


def test_flat_source_cli(tmp_path):
    script = Path(__file__).resolve().parents[1] / "src" / "extended_intro_hw6_cli.py"
    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "usage:" in result.stdout and "decode" in result.stdout


def test_installed_module_cli(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "extended_intro_hw6_cli", "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "usage:" in result.stdout and "decode" in result.stdout
