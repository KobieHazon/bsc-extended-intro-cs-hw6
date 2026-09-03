from __future__ import annotations

import subprocess
import sys


def run_cli(*arguments: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "extended_intro_hw6.cli", *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def test_combinations_cli() -> None:
    assert run_cli("combinations", "1,2,3", "2") == "[['1', '2'], ['1', '3'], ['2', '3']]"


def test_rotation_cli() -> None:
    assert run_cli("rotation", "amirrub", "rubamir") == "True"


def test_weighted_length_cli() -> None:
    assert run_cli("weighted-length", "0,11,10", "5,1,3") == "13"


def test_decode_cli() -> None:
    assert run_cli("decode", "000011111111", "4") == "011"
