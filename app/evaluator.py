from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any

import numpy as np

from .questions import Question


SAFE_BUILTINS = {
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "len": len,
    "range": range,
    "enumerate": enumerate,
    "list": list,
    "tuple": tuple,
    "set": set,
    "dict": dict,
    "float": float,
    "int": int,
    "str": str,
    "zip": zip,
}

FORBIDDEN_AST = (
    ast.Import,
    ast.ImportFrom,
    ast.Global,
    ast.Nonlocal,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.Raise,
    ast.Lambda,
    ast.ClassDef,
    ast.Delete,
)


@dataclass
class EvalResult:
    ok: bool
    passed: int
    total: int
    message: str


def _to_runtime_arg(value: Any) -> Any:
    if isinstance(value, list):
        return np.array(value)
    return value


def _to_compare_value(value: Any) -> Any:
    if isinstance(value, list):
        return np.array(value)
    return value


def _compare(actual: Any, expected: Any) -> bool:
    if isinstance(expected, np.ndarray):
        if not isinstance(actual, np.ndarray):
            actual = np.array(actual)
        return np.allclose(actual, expected)
    return actual == expected


def _validate_ast(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN_AST):
            raise ValueError(f"forbidden syntax: {type(node).__name__}")


def evaluate_submission(code: str, question: Question) -> EvalResult:
    try:
        tree = ast.parse(code)
        _validate_ast(tree)

        env = {"np": np, "__builtins__": SAFE_BUILTINS}
        exec(compile(tree, filename="submission.py", mode="exec"), env, env)

        if question.function_name not in env or not callable(env[question.function_name]):
            return EvalResult(False, 0, len(question.tests), f"請定義函式 {question.function_name}()")

        func = env[question.function_name]
        passed = 0

        for i, test in enumerate(question.tests, start=1):
            args = tuple(_to_runtime_arg(arg) for arg in test.args)
            expected = _to_compare_value(test.expected)
            actual = func(*args)
            if _compare(actual, expected):
                passed += 1
            else:
                return EvalResult(False, passed, len(question.tests), f"第 {i} 組測資未通過")

        return EvalResult(True, passed, len(question.tests), "全部測資通過")
    except Exception as exc:
        return EvalResult(False, 0, len(question.tests), f"執行錯誤: {exc}")

