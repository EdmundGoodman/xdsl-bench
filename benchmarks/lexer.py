#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Benchmark the xDSL lexer on MLIR files."""

import timeit
from pathlib import Path

from xdsl.utils.lexer import Input
from xdsl.utils.mlir_lexer import MLIRLexer, MLIRTokenKind

BENCHMARKS_DIR = Path(__file__).parent
MLIR_FILES: dict[str, Path] = {
    "apply_pdl_extra_file": Path(
        "xdsl/tests/filecheck/transforms/apply-pdl/apply_pdl_extra_file.mlir"
    ),
    "rvscf_lowering_emu": Path(
        "xdsl/tests/filecheck/with-riscemu/rvscf_lowering_emu.mlir"
    ),
}


def lex_input(lexer_input: Input) -> None:
    """Lex an xDSL input."""
    lexer = MLIRLexer(lexer_input)
    while lexer.lex().kind is not MLIRTokenKind.EOF:
        pass


def lex_file(mlir_file: Path) -> None:
    """Lex a mlir file."""
    contents = mlir_file.read_text()
    lexer_input = Input(contents, mlir_file)
    lex_input(lexer_input)


def time_lexer__apply_pdl_extra_file() -> None:
    """Time lexing the `apply_pdl_extra_file.mlir` file."""
    return lex_file(BENCHMARKS_DIR.parent / MLIR_FILES["apply_pdl_extra_file"])


def time_lexer__rvscf_lowering_emu() -> None:
    """Time lexing the `rvscf_lowering_emu.mlir` file."""
    return lex_file(BENCHMARKS_DIR.parent / MLIR_FILES["rvscf_lowering_emu"])


def time_lexer_all() -> None:
    """Time lexing all `.mlir` files in xDSL's `tests/` directory ."""
    mlir_files = (BENCHMARKS_DIR.parent / "xdsl/tests").rglob("*.mlir")
    for mlir_file in mlir_files:
        lex_file(Path(mlir_file))


if __name__ == "__main__":
    import cProfile

    TEST_NAME = Path(__file__).stem

    # Time lexing all .mlir files for a single number on performance
    print(
        "File 'apply_pdl_extra_file.mlir' lexed in "
        f"{timeit.timeit(time_lexer__apply_pdl_extra_file, number=1)}s"
    )
    print(f"All test .mlir files lexed in {timeit.timeit(time_lexer_all, number=1)}s")

    # Profile lexing specific .mlir files
    MLIR_NAME = "apply_pdl_extra_file"
    ## End-to-end
    output_prof = f"{BENCHMARKS_DIR.parent}/profiles/{TEST_NAME}__{MLIR_NAME}.prof"
    cProfile.run(f"time_lexer__{MLIR_NAME}()", output_prof)
    print(f"Profile written to '{output_prof}'!")
    ## Lexing only
    mlir_file = BENCHMARKS_DIR.parent / MLIR_FILES[MLIR_NAME]
    lexer_input = Input(mlir_file.read_text(), mlir_file)
    output_prof = (
        f"{BENCHMARKS_DIR.parent}/profiles/{TEST_NAME}__{MLIR_NAME}__lex_only.prof"
    )
    cProfile.run("lex_input(lexer_input)", output_prof)
    print(f"Profile written to '{output_prof}'!")