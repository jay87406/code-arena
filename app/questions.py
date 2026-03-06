from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TestCase:
    args: tuple[Any, ...]
    expected: Any


@dataclass(frozen=True)
class Question:
    qid: str
    title: str
    description: str
    function_name: str
    starter_code: str
    tests: tuple[TestCase, ...]
    tags: tuple[str, ...]


QUESTION_BANK: tuple[Question, ...] = (
    Question(
        qid="np_mean_axis0",
        title="欄平均",
        description="回傳 2D numpy 陣列每一欄的平均值 (axis=0)。",
        function_name="solve",
        starter_code="def solve(arr):\n    # arr is a 2D numpy array\n    pass\n",
        tests=(
            TestCase(args=([ [1, 2], [3, 4] ],), expected=[2.0, 3.0]),
            TestCase(args=([ [2, 4, 6], [1, 3, 5] ],), expected=[1.5, 3.5, 5.5]),
        ),
        tags=("numpy", "array"),
    ),
    Question(
        qid="np_normalize",
        title="0-1 正規化",
        description="把一維陣列正規化到 0~1。若 max == min，回傳全 0。",
        function_name="solve",
        starter_code="def solve(arr):\n    # arr is a 1D numpy array\n    pass\n",
        tests=(
            TestCase(args=([1, 2, 3],), expected=[0.0, 0.5, 1.0]),
            TestCase(args=([5, 5, 5],), expected=[0.0, 0.0, 0.0]),
        ),
        tags=("numpy", "math"),
    ),
    Question(
        qid="np_row_sums",
        title="列加總",
        description="回傳 2D 陣列每一列的總和。",
        function_name="solve",
        starter_code="def solve(arr):\n    # arr is a 2D numpy array\n    pass\n",
        tests=(
            TestCase(args=([ [1, 2, 3], [4, 5, 6] ],), expected=[6, 15]),
            TestCase(args=([ [0, 0], [7, 8], [1, 1] ],), expected=[0, 15, 2]),
        ),
        tags=("numpy", "array"),
    ),
    Question(
        qid="py_even_filter",
        title="偶數過濾",
        description="回傳 list 中的所有偶數，保留原本順序。",
        function_name="solve",
        starter_code="def solve(nums):\n    # nums is a Python list[int]\n    pass\n",
        tests=(
            TestCase(args=([1, 2, 3, 4],), expected=[2, 4]),
            TestCase(args=([9, 7, 5],), expected=[]),
        ),
        tags=("python", "list"),
    ),
    Question(
        qid="py_word_count",
        title="字詞統計",
        description="輸入字串，回傳每個單字出現次數 dict（以空白切詞）。",
        function_name="solve",
        starter_code="def solve(text):\n    # text is a Python string\n    pass\n",
        tests=(
            TestCase(args=("a b a",), expected={"a": 2, "b": 1}),
            TestCase(args=("numpy numpy python",), expected={"numpy": 2, "python": 1}),
        ),
        tags=("python", "dict"),
    ),
    Question(
        qid="np_clip",
        title="數值裁切",
        description="把陣列中的值裁切在 [low, high] 區間內。",
        function_name="solve",
        starter_code="def solve(arr, low, high):\n    # arr is a 1D numpy array\n    pass\n",
        tests=(
            TestCase(args=([1, 5, 10], 3, 8), expected=[3, 5, 8]),
            TestCase(args=([-2, 0, 4], -1, 2), expected=[-1, 0, 2]),
        ),
        tags=("numpy", "math"),
    ),
    Question(
        qid="np_diag_sum",
        title="對角線加總",
        description="回傳方陣主對角線元素總和。",
        function_name="solve",
        starter_code="def solve(arr):\n    # arr is a 2D square numpy array\n    pass\n",
        tests=(
            TestCase(args=([ [1, 2], [3, 4] ],), expected=5),
            TestCase(args=([ [5, 0, 0], [0, 6, 0], [0, 0, 7] ],), expected=18),
        ),
        tags=("numpy", "array"),
    ),
    Question(
        qid="py_reverse_words",
        title="反轉單字順序",
        description="把字串中的單字順序反轉後輸出（空白分隔）。",
        function_name="solve",
        starter_code="def solve(text):\n    # text is a Python string\n    pass\n",
        tests=(
            TestCase(args=("i love numpy",), expected="numpy love i"),
            TestCase(args=("hello",), expected="hello"),
        ),
        tags=("python", "string"),
    ),
)

