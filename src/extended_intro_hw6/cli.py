"""Command-line interface for selected Homework 6 algorithms."""

from __future__ import annotations

import argparse

from .exercises import choose_sets_gen, decode, is_rotated_1, lz_Qa, lz_Qb, lz_Qc, weighted_length


def csv_values(value: str) -> list[str]:
    return [item for item in value.split(",") if item]


def integer_list(value: str) -> list[int]:
    try:
        return [int(item) for item in value.split(",") if item]
    except ValueError as error:
        raise argparse.ArgumentTypeError("values must be comma-separated integers") from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    combinations_parser = subparsers.add_parser("combinations")
    combinations_parser.add_argument("values", type=csv_values)
    combinations_parser.add_argument("k", type=int)

    rotation_parser = subparsers.add_parser("rotation")
    rotation_parser.add_argument("source")
    rotation_parser.add_argument("candidate")

    weight_parser = subparsers.add_parser("weighted-length")
    weight_parser.add_argument("code_words", type=csv_values)
    weight_parser.add_argument("weights", type=integer_list)

    decode_parser = subparsers.add_parser("decode")
    decode_parser.add_argument("transmission")
    decode_parser.add_argument("repetition", type=int)

    subparsers.add_parser("lz-answers")
    return parser


def cli() -> None:
    arguments = build_parser().parse_args()
    try:
        if arguments.command == "combinations":
            result = list(choose_sets_gen(arguments.values, arguments.k))
        elif arguments.command == "rotation":
            result = is_rotated_1(arguments.source, arguments.candidate)
        elif arguments.command == "weighted-length":
            result = weighted_length(arguments.code_words, arguments.weights)
        elif arguments.command == "decode":
            result = decode(arguments.transmission, arguments.repetition)
        else:
            result = [lz_Qa(), lz_Qb(), lz_Qc()]
        print(result)
    except ValueError as error:
        raise SystemExit(f"error: {error}") from error


if __name__ == "__main__":
    cli()
