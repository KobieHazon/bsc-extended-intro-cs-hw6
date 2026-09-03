from __future__ import annotations

import pytest

from extended_intro_hw6 import (
    Matrix,
    ascii2bit_stream,
    build_huffman_tree,
    char_count,
    choose_sets_gen,
    choose_sets_gen_specific,
    compress,
    decode,
    decompress,
    dilate,
    edges,
    generate_code,
    huffman_roundtrip,
    is_rotated_1,
    is_rotated_2,
    majority,
    optimal,
    reverse_dict,
    segment,
    text_fingerprint,
    upside_down,
    weighted_length,
)


def test_choose_sets_gen_matches_recovered_order() -> None:
    assert list(choose_sets_gen([1, 2, 3, 4], 2)) == [
        [1, 2],
        [1, 3],
        [1, 4],
        [2, 3],
        [2, 4],
        [3, 4],
    ]


def test_choose_sets_specific_filters_by_element() -> None:
    assert list(choose_sets_gen_specific([1, 2, 3], 2, 3)) == [[1, 3], [2, 3]]
    assert list(choose_sets_gen_specific([1, 2, 3], 0, 1)) == []


def test_rotation_detectors() -> None:
    examples = [
        ("amirrub", "rubamir", True),
        ("amirrub", "gilamir", False),
        ("amirrub", "ubamirr", True),
        ("abcd", "bcad", False),
        ("", "", True),
    ]
    for source, candidate, expected in examples:
        assert is_rotated_1(source, candidate) is expected
        assert is_rotated_2(source, candidate) is expected


def test_text_fingerprint_rolls_windows() -> None:
    text = "abcdef"
    assert text_fingerprint(text, 3) == [
        text_fingerprint(text[index : index + 3], 3)[0] for index in range(4)
    ]


def test_huffman_roundtrip_and_weighted_length() -> None:
    code = generate_code(build_huffman_tree(char_count("aabcd")))
    compressed = compress("bad", code)
    assert decompress(compressed, reverse_dict(code)) == "bad"
    assert huffman_roundtrip("aabcd", "bad")[1] == "bad"
    assert ascii2bit_stream("A") == "1000001"
    assert weighted_length(["0", "11", "10"], [5, 1, 3]) == 13
    assert optimal(["0", "11", "10"], [5, 1, 3]) is True
    assert optimal(["0", "11", "10"], [3, 1, 5]) is False


def test_matrix_image_operations() -> None:
    image = Matrix(4, 4, 0)
    image[0, 0] = 20
    image[1, 0] = 60

    flipped = upside_down(image)
    assert flipped.rows[2][0] == 60
    assert flipped.rows[3][0] == 20

    segmented = segment(image, 10)
    assert segmented.rows == [
        [255, 0, 0, 0],
        [255, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    dilated = dilate(segmented, 1)
    assert dilated.rows == [
        [255, 0, 0, 0],
        [255, 255, 0, 0],
        [0, 255, 0, 0],
        [0, 0, 0, 0],
    ]
    assert edges(image, 1, 10) == dilated - segmented


def test_matrix_arithmetic_and_shape_validation() -> None:
    left = Matrix(2, 2, 2)
    right = Matrix(2, 2, 3)
    assert (left + right).rows == [[5, 5], [5, 5]]
    assert (left * right).rows == [[12, 12], [12, 12]]
    with pytest.raises(ValueError):
        _ = left * Matrix(3, 3)


def test_decode_repetition_code() -> None:
    assert majority("11100") == "1"
    assert majority("1100") is None
    assert decode("000011111111", 4) == "011"
    assert decode("0110", 2) is None
    with pytest.raises(ValueError):
        decode("0011", 0)
