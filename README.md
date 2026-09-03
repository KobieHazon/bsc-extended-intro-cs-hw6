# Extended Introduction to Computer Science - Homework 6

A 2018 CS BSc Python assignment covering recursive combinatorial generation, Karp-Rabin rolling fingerprints, Huffman-code optimality checks, LZ compression answers, image-matrix transformations, and repetition-code decoding.

## Algorithms

- Generate k-sized subsets lazily, including filtered generation by required element.
- Detect cyclic string rotations with rolling fingerprints and direct containment.
- Build and apply Huffman codes, compute weighted code lengths, and compare a proposed code against an optimal Huffman construction.
- Preserve the recovered LZ answer triples from the written part of the assignment.
- Flip, segment, dilate, and edge-detect grayscale matrices.
- Decode binary transmissions encoded with an m-repetition code.

## Setup

```bash
git clone https://github.com/KobieHazon/bsc-extended-intro-cs-hw6.git
cd bsc-extended-intro-cs-hw6
uv sync --dev
```

The maintained package supports Python 3.12 or newer and has no runtime dependencies. The preserved recovered solution imports the original matrix display helper, which expects Python `tkinter`; the maintained package only imports Tk when `Matrix.display()` is called.

## Usage

```bash
uv run extended-intro-hw6 combinations 1,2,3,4 2
uv run extended-intro-hw6 rotation amirrub rubamir
uv run extended-intro-hw6 weighted-length 0,11,10 5,1,3
uv run extended-intro-hw6 decode 000011111111 4
```

The commands print the generated combinations, `True`, `13`, and `011`.

## Testing

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

The tests cover the recovered embedded tester, generator ordering, rotation examples, rolling fingerprints, Huffman compression round trips, optimal-code checks, matrix arithmetic and image operations, repetition-code decoding, and command-line behavior.

## Repository Structure

- `assignment/matrix.py`: supplied matrix helper preserved in its original form
- `assignment/huffman.py`: supplied Huffman helper preserved in its original form
- `assignment/printree.py`: supplied binary-tree printing helper preserved in its original form
- `solution/hw6.py`: my recovered submitted Python solution
- `solution/written-answers.pdf`: my exported written answers with PDF metadata reduced to the author's name
- `src/extended_intro_hw6/`: maintained algorithms and command-line interface
- `tests/`: portable pytest regression suite, including the recovered embedded tester

## Implementation notes

The recovered source combines my implementations with a distributed assignment scaffold and lecture helper code. Scaffold comments remain in the historical solution commit and are not presented as authored work.

## License

No repository-wide license is declared because the repository combines original work with supplied material whose reuse terms were not recorded.
