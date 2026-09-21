"""Algorithms from Extended Introduction to Computer Science Homework 6."""

from __future__ import annotations

from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass
from typing import TypeVar

__all__ = [
    "Matrix",
    "ascii2bit_stream",
    "build_huffman_tree",
    "char_count",
    "choose_sets_gen",
    "choose_sets_gen_specific",
    "clean_non_ascii",
    "compress",
    "corpus",
    "decode",
    "decompress",
    "dilate",
    "edges",
    "fingerprint",
    "generate_code",
    "huffman_roundtrip",
    "is_rotated_1",
    "is_rotated_2",
    "items",
    "local_operator",
    "lz_Qa",
    "lz_Qb",
    "lz_Qc",
    "majority",
    "optimal",
    "reverse_dict",
    "segment",
    "text2bit_stream",
    "text_fingerprint",
    "upside_down",
    "weighted_length",
]

T = TypeVar("T")


def choose_sets_gen(values: Sequence[T], k: int) -> Generator[list[T], None, None]:
    """Yield all k-sized selections from values, preserving the order."""

    if k < 0:
        raise ValueError("k must be non-negative")
    if k == 0:
        yield []
        return
    if len(values) < k:
        return

    first, rest = values[0], values[1:]
    for combination in choose_sets_gen(rest, k - 1):
        yield [first, *combination]
    yield from choose_sets_gen(rest, k)


def choose_sets_gen_specific(
    values: Sequence[T], k: int, element: T
) -> Generator[list[T], None, None]:
    """Yield k-sized selections from values that contain element."""

    for combination in choose_sets_gen(values, k):
        if element in combination:
            yield combination


def fingerprint(text: str, basis: int = 2**16, r: int = 2**32 - 3) -> int:
    """Compute a Karp-Rabin fingerprint with Horner's method."""

    partial_sum = 0
    for character in text:
        partial_sum = (partial_sum * basis + ord(character)) % r
    return partial_sum


def text_fingerprint(text: str, m: int, basis: int = 2**16, r: int = 2**32 - 3) -> list[int]:
    """Compute rolling fingerprints for all windows of length m in text."""

    if m <= 0:
        raise ValueError("m must be positive")
    if len(text) < m:
        return []

    fingerprints = [fingerprint(text[:m], basis, r)]
    b_power = pow(basis, m - 1, r)
    for start in range(1, len(text) - m + 1):
        previous = fingerprints[start - 1]
        current = (
            (previous - ord(text[start - 1]) * b_power) * basis + ord(text[start + m - 1])
        ) % r
        fingerprints.append(current)
    return fingerprints


def is_rotated_1(source: str, candidate: str, basis: int = 2**16, r: int = 2**32 - 3) -> bool:
    """Return whether candidate is a cyclic rotation of source using rolling hashes."""

    if len(source) != len(candidate):
        return False
    if not source:
        return True

    doubled_candidate = candidate + candidate[:-1]
    target_fingerprint = fingerprint(source, basis, r)
    for start, value in enumerate(text_fingerprint(doubled_candidate, len(source), basis, r)):
        if value == target_fingerprint and doubled_candidate[start : start + len(source)] == source:
            return True
    return False


def is_rotated_2(source: str, candidate: str) -> bool:
    """Return whether candidate is a cyclic rotation of source by direct containment."""

    return len(source) == len(candidate) and source in candidate + candidate


def text2bit_stream(text: str) -> str:
    return "".join(bin(ord(character))[2:].zfill(8) for character in text)


def ascii2bit_stream(text: str) -> str:
    """Translate ASCII text to a 7-bit binary representation."""

    return "".join(bin(ord(character))[2:].zfill(7) for character in text)


HuffmanTree = str | list["HuffmanTree"]


def char_count(text: str) -> dict[str, int]:
    """Count characters in text."""

    counts: dict[str, int] = {}
    for character in text:
        counts[character] = counts.get(character, 0) + 1
    return counts


def extract_min(queue: list[tuple[HuffmanTree, int]]) -> tuple[HuffmanTree, int]:
    """Remove and return the queue pair with minimal weight."""

    minimum = min(queue, key=lambda pair: pair[1])
    queue.remove(minimum)
    return minimum


def build_huffman_tree(counts: dict[str, int]) -> HuffmanTree:
    """Build a Huffman tree from character counts."""

    if not counts:
        raise ValueError("counts must not be empty")

    queue: list[tuple[HuffmanTree, int]] = list(counts.items())
    while len(queue) > 1:
        left, left_count = extract_min(queue)
        right, right_count = extract_min(queue)
        queue.append(([left, right], left_count + right_count))
    root, _weight = extract_min(queue)
    return root


def generate_code(tree: HuffmanTree, prefix: str = "") -> dict[str, str]:
    """Generate a Huffman codebook from a Huffman tree."""

    if isinstance(tree, str):
        return {tree: prefix or "0"}
    left, right = tree
    codebook: dict[str, str] = {}
    codebook.update(generate_code(left, prefix + "0"))
    codebook.update(generate_code(right, prefix + "1"))
    return codebook


def compress(text: str, encoding: dict[str, str]) -> str:
    """Compress text using a character-to-code encoding dictionary."""

    return "".join(encoding[character] for character in text)


def reverse_dict(dictionary: dict[str, str]) -> dict[str, str]:
    """Reverse an encoding dictionary."""

    return {value: key for key, value in dictionary.items()}


def decompress(bits: str, decoding: dict[str, str]) -> str:
    """Decompress a bit stream using a code-to-character decoding dictionary."""

    prefix = ""
    result: list[str] = []
    for bit in bits:
        prefix += bit
        if prefix in decoding:
            result.append(decoding[prefix])
            prefix = ""
    if prefix:
        raise ValueError("bits ended in the middle of a code word")
    return "".join(result)


def clean_non_ascii(text: str) -> str:
    """Remove non-ASCII characters from text."""

    return "".join(character for character in text if ord(character) < 128)


def weighted_length(code_words: Sequence[str], weights: Sequence[int]) -> int:
    """Return the weighted sum of code-word lengths."""

    if len(code_words) != len(weights):
        raise ValueError("code_words and weights must have the same length")
    return sum(len(code_words[index]) * weights[index] for index in range(len(weights)))


def optimal(code_words: Sequence[str], weights: Sequence[int]) -> bool:
    """Return whether the given code has optimal weighted length for the weights."""

    if len(code_words) != len(weights):
        raise ValueError("code_words and weights must have the same length")

    corpus_text = "".join(chr(index) * weight for index, weight in enumerate(weights))
    generated = generate_code(build_huffman_tree(char_count(corpus_text)))
    generated_words = [generated[chr(index)] for index in range(len(weights))]
    return weighted_length(code_words, weights) == weighted_length(generated_words, weights)


def corpus() -> str:
    return "aabcd"


def lz_Qa() -> tuple[str, int, int]:
    return ("abcde", 40, 40)


def lz_Qb() -> tuple[str, int, int]:
    return ("wood would a wo", 114, 120)


def lz_Qc() -> tuple[str, int, int]:
    return ("a d a d  a a a", 86, 84)


@dataclass
class Matrix:
    """A rectangular numeric matrix with light image-processing helpers."""

    rows: list[list[int | float | complex]]

    def __init__(self, n: int, m: int, value: int | float | complex = 0) -> None:
        if n <= 0 or m <= 0:
            raise ValueError("matrix dimensions must be positive")
        self.rows = [[value] * m for _row in range(n)]

    def dim(self) -> tuple[int, int]:
        return len(self.rows), len(self.rows[0])

    def __repr__(self) -> str:
        if len(self.rows) > 10 or len(self.rows[0]) > 10:
            return "Matrix too large, specify submatrix"
        return f"<Matrix {self.rows}>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Matrix) and self.rows == other.rows

    def copy(self) -> "Matrix":
        n, m = self.dim()
        duplicate = Matrix(n, m)
        duplicate.rows = [row.copy() for row in self.rows]
        return duplicate

    def __getitem__(self, key: tuple[int | slice, int | slice]) -> int | float | complex | "Matrix":
        row, column = key
        if isinstance(row, int) and isinstance(column, int):
            return self.rows[row][column]
        if isinstance(row, slice) and isinstance(column, slice):
            result = Matrix(1, 1)
            result.rows = [source_row[column] for source_row in self.rows[row]]
            return result
        return NotImplemented

    def __setitem__(self, key: tuple[int | slice, int | slice], value: object) -> None:
        row, column = key
        if isinstance(row, int) and isinstance(column, int):
            if not isinstance(value, (int, float, complex)):
                raise TypeError("matrix entries must be numeric")
            self.rows[row][column] = value
            return
        if isinstance(row, slice) and isinstance(column, slice):
            if not isinstance(value, Matrix):
                raise TypeError("slice assignment requires a Matrix")
            n, m = value.dim()
            selected_rows = self.rows[row]
            if len(selected_rows) != n or len(selected_rows[0][column]) != m:
                raise ValueError("assigned matrix dimensions do not match slice")
            for selected_row, value_row in zip(selected_rows, value.rows, strict=True):
                selected_row[column] = value_row
            return
        raise TypeError("matrix indices must be integers or slices")

    def entrywise_op(self, other: "Matrix", op: Callable[[object, object], object]) -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.dim() != other.dim():
            raise ValueError("matrix dimensions must match")
        n, m = self.dim()
        result = Matrix(n, m)
        for row in range(n):
            for column in range(m):
                result[row, column] = op(self[row, column], other[row, column])
        return result

    def __add__(self, other: "Matrix") -> "Matrix":
        return self.entrywise_op(other, lambda left, right: left + right)

    def __sub__(self, other: "Matrix") -> "Matrix":
        return self.entrywise_op(other, lambda left, right: left - right)

    def __neg__(self) -> "Matrix":
        n, m = self.dim()
        return Matrix(n, m) - self

    def __mul__(self, other: object) -> "Matrix":
        if isinstance(other, Matrix):
            return self.multiply_by_matrix(other)
        if isinstance(other, (int, float, complex)):
            return self.multiply_by_scalar(other)
        return NotImplemented

    __rmul__ = __mul__

    def multiply_by_scalar(self, value: int | float | complex) -> "Matrix":
        n, m = self.dim()
        return self.entrywise_op(Matrix(n, m, value), lambda left, right: left * right)

    def multiply_by_matrix(self, other: "Matrix") -> "Matrix":
        n, m = self.dim()
        other_n, other_m = other.dim()
        if m != other_n:
            raise ValueError("left matrix columns must match right matrix rows")
        result = Matrix(n, other_m)
        for row in range(n):
            for column in range(other_m):
                result[row, column] = sum(
                    self[row, inner] * other[inner, column] for inner in range(m)
                )
        return result

    def save(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as output:
            n, m = self.dim()
            print(n, m, file=output)
            for row in self.rows:
                print(" ".join(str(entry) for entry in row), file=output)

    @staticmethod
    def load(filename: str) -> "Matrix":
        with open(filename, encoding="utf-8") as source:
            n, m = [int(value) for value in source.readline().split()]
            result = Matrix(n, m)
            for row in range(n):
                loaded_row = [int(value) for value in source.readline().split()]
                if len(loaded_row) != m:
                    raise ValueError("matrix file row width does not match header")
                result.rows[row] = loaded_row
        return result

    def display(self, title: str | None = None, zoom: int | None = None) -> None:
        """Display the matrix as a grayscale image when Tk is available."""

        try:
            import tkinter
        except ModuleNotFoundError as error:
            raise RuntimeError("matrix display requires a Python build with tkinter") from error

        height, width = self.dim()
        pixels = " ".join(
            "{" + " ".join("#" + f"{int(pixel):02x}" * 3 for pixel in row) + "}"
            for row in self.rows
        )
        root = tkinter.Tk()
        root.withdraw()
        image = tkinter.PhotoImage(width=width, height=height)
        image.put(pixels)
        if zoom is not None:
            if zoom <= 0:
                raise ValueError("zoom must be positive")
            if zoom > 1:
                image = image.zoom(zoom)
            elif zoom < 1:
                image = image.subsample(zoom)
        window = tkinter.Toplevel(master=root)
        window.title("Matrix" if title is None else title)
        label = tkinter.Label(master=window, image=image)
        label.image = image
        label.pack()
        window.protocol("WM_DELETE_WINDOW", root.destroy)
        root.mainloop()


def upside_down(image: Matrix) -> Matrix:
    n, m = image.dim()
    result = Matrix(n, m)
    for row in range(n):
        for column in range(m):
            result[row, column] = image[n - row - 1, column]
    return result


def items(matrix: Matrix) -> list[object]:
    """Flatten matrix elements into a list."""

    n, m = matrix.dim()
    return [matrix[row, column] for row in range(n) for column in range(m)]


def local_operator(matrix: Matrix, op: Callable[[list[object]], object], k: int = 1) -> Matrix:
    """Apply op to each centered (2k+1)-by-(2k+1) neighborhood."""

    if k < 0:
        raise ValueError("k must be non-negative")
    n, m = matrix.dim()
    result = matrix.copy()
    for row in range(k, n - k):
        for column in range(k, m - k):
            result[row, column] = op(
                items(matrix[row - k : row + k + 1, column - k : column + k + 1])
            )
    return result


def segment(image: Matrix, threshold: int | float) -> Matrix:
    """Binary segmentation of image by threshold."""

    n, m = image.dim()
    result = Matrix(n, m)
    for row in range(n):
        for column in range(m):
            result[row, column] = 255 if image[row, column] >= threshold else 0
    return result


def dilate(image: Matrix, k: int = 1) -> Matrix:
    return local_operator(image, lambda values: 255 if 255 in values else 0, k)


def edges(image: Matrix, k: int, threshold: int | float) -> Matrix:
    segmented = segment(image, threshold)
    return dilate(segmented, k) - segmented


def majority(binary_string: str) -> str | None:
    ones = binary_string.count("1")
    if ones > len(binary_string) / 2:
        return "1"
    if ones < len(binary_string) / 2:
        return "0"
    return None


def decode(transmission: str, m: int) -> str | None:
    """Decode an m-repetition binary transmission, returning None on ties."""

    if m <= 0:
        raise ValueError("m must be positive")
    decoded = ""
    for index in range(len(transmission) // m):
        bit = majority(transmission[index * m : index * m + m])
        if bit is None:
            return None
        decoded += bit
    return decoded


def huffman_roundtrip(corpus_text: str, text: str) -> tuple[str, str]:
    """Compress and decompress text using a Huffman code derived from corpus_text."""

    code = generate_code(build_huffman_tree(char_count(corpus_text)))
    compressed = compress(text, code)
    decompressed = decompress(compressed, reverse_dict(code))
    return compressed, decompressed
