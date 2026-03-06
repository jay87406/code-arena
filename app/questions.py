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
    solution_code: str
    tests: tuple[TestCase, ...]
    tags: tuple[str, ...]


def _q(
    qid: str,
    title: str,
    description: str,
    starter_code: str,
    solution_code: str,
    tests: tuple[TestCase, ...],
    tags: tuple[str, ...],
) -> Question:
    return Question(
        qid=qid,
        title=title,
        description=description,
        function_name="solve",
        starter_code=starter_code,
        solution_code=solution_code,
        tests=tests,
        tags=tags,
    )


def _base_questions() -> list[Question]:
    return [
        _q(
            qid="np_mean_axis0",
            title="Numpy: 欄平均",
            description="回傳 2D numpy 陣列每一欄的平均值 (axis=0)。",
            starter_code="def solve(arr):\n    pass\n",
            solution_code="def solve(arr):\n    return arr.mean(axis=0)\n",
            tests=(
                TestCase(args=([[1, 2], [3, 4]],), expected=[2.0, 3.0]),
                TestCase(args=([[2, 4, 6], [1, 3, 5]],), expected=[1.5, 3.5, 5.5]),
            ),
            tags=("numpy", "array", "easy"),
        ),
        _q(
            qid="np_normalize",
            title="Numpy: 0-1 正規化",
            description="把一維陣列正規化到 0~1。若 max == min，回傳全 0。",
            starter_code="def solve(arr):\n    pass\n",
            solution_code=(
                "def solve(arr):\n"
                "    lo = arr.min()\n"
                "    hi = arr.max()\n"
                "    if hi == lo:\n"
                "        return np.zeros_like(arr, dtype=float)\n"
                "    return (arr - lo) / (hi - lo)\n"
            ),
            tests=(
                TestCase(args=([1, 2, 3],), expected=[0.0, 0.5, 1.0]),
                TestCase(args=([5, 5, 5],), expected=[0.0, 0.0, 0.0]),
            ),
            tags=("numpy", "math", "easy"),
        ),
        _q(
            qid="np_clip",
            title="Numpy: 數值裁切",
            description="把陣列中的值裁切在 [low, high] 區間內。",
            starter_code="def solve(arr, low, high):\n    pass\n",
            solution_code="def solve(arr, low, high):\n    return np.clip(arr, low, high)\n",
            tests=(
                TestCase(args=([1, 5, 10], 3, 8), expected=[3, 5, 8]),
                TestCase(args=([-2, 0, 4], -1, 2), expected=[-1, 0, 2]),
            ),
            tags=("numpy", "array", "easy"),
        ),
        _q(
            qid="lc_two_sum_core",
            title="LeetCode: Two Sum",
            description="給 nums 與 target，回傳兩個索引 i,j 使 nums[i]+nums[j]==target。",
            starter_code="def solve(nums, target):\n    pass\n",
            solution_code=(
                "def solve(nums, target):\n"
                "    seen = {}\n"
                "    for i, x in enumerate(nums):\n"
                "        y = target - x\n"
                "        if y in seen:\n"
                "            return [seen[y], i]\n"
                "        seen[x] = i\n"
            ),
            tests=(
                TestCase(args=([2, 7, 11, 15], 9), expected=[0, 1]),
                TestCase(args=([3, 2, 4], 6), expected=[1, 2]),
            ),
            tags=("leetcode", "hashmap", "easy"),
        ),
        _q(
            qid="lc_valid_parentheses_core",
            title="LeetCode: Valid Parentheses",
            description="輸入只含 ()[]{} 的字串，判斷括號是否合法配對。",
            starter_code="def solve(s):\n    pass\n",
            solution_code=(
                "def solve(s):\n"
                "    pair = {')': '(', ']': '[', '}': '{'}\n"
                "    st = []\n"
                "    for ch in s:\n"
                "        if ch in '([{':\n"
                "            st.append(ch)\n"
                "        else:\n"
                "            if not st or st[-1] != pair[ch]:\n"
                "                return False\n"
                "            st.pop()\n"
                "    return not st\n"
            ),
            tests=(
                TestCase(args=("()[]{}",), expected=True),
                TestCase(args=("(]",), expected=False),
            ),
            tags=("leetcode", "stack", "easy"),
        ),
        _q(
            qid="lc_max_subarray_core",
            title="LeetCode: Maximum Subarray",
            description="回傳最大連續子陣列和。",
            starter_code="def solve(nums):\n    pass\n",
            solution_code=(
                "def solve(nums):\n"
                "    best = cur = nums[0]\n"
                "    for x in nums[1:]:\n"
                "        cur = max(x, cur + x)\n"
                "        best = max(best, cur)\n"
                "    return best\n"
            ),
            tests=(
                TestCase(args=([-2, 1, -3, 4, -1, 2, 1, -5, 4],), expected=6),
                TestCase(args=([1],), expected=1),
            ),
            tags=("leetcode", "dp", "medium"),
        ),
        _q(
            qid="ai_softmax_core",
            title="AI: Softmax",
            description="輸入 logits，回傳 softmax 機率（請使用數值穩定作法）。",
            starter_code="def solve(logits):\n    pass\n",
            solution_code=(
                "def solve(logits):\n"
                "    z = logits - np.max(logits)\n"
                "    e = np.exp(z)\n"
                "    return e / e.sum()\n"
            ),
            tests=(
                TestCase(args=([1.0, 2.0, 3.0],), expected=[0.090031, 0.244728, 0.665241]),
                TestCase(args=([1000.0, 1000.0],), expected=[0.5, 0.5]),
            ),
            tags=("ai", "numpy", "medium"),
        ),
        _q(
            qid="ai_sigmoid_core",
            title="AI: Sigmoid",
            description="輸入 numpy 陣列 x，回傳 sigmoid(x)=1/(1+exp(-x))。",
            starter_code="def solve(x):\n    pass\n",
            solution_code="def solve(x):\n    return 1.0 / (1.0 + np.exp(-x))\n",
            tests=(
                TestCase(args=([0.0, 1.0],), expected=[0.5, 0.7310586]),
                TestCase(args=([-1.0, 2.0],), expected=[0.2689414, 0.8807971]),
            ),
            tags=("ai", "numpy", "easy"),
        ),
        _q(
            qid="ai_mse_core",
            title="AI: MSE Loss",
            description="給 y_true 與 y_pred，回傳 mean squared error。",
            starter_code="def solve(y_true, y_pred):\n    pass\n",
            solution_code="def solve(y_true, y_pred):\n    return np.mean((y_true - y_pred) ** 2)\n",
            tests=(
                TestCase(args=([1.0, 2.0], [1.0, 3.0]), expected=0.5),
                TestCase(args=([0.0, 0.0], [1.0, -1.0]), expected=1.0),
            ),
            tags=("ai", "numpy", "easy"),
        ),
    ]


def _gen_numpy_scale_questions() -> list[Question]:
    out: list[Question] = []
    for k in range(2, 27):
        out.append(
            _q(
                qid=f"np_scale_{k}",
                title=f"Numpy: 陣列放大 x{k}",
                description=f"把 1D numpy 陣列每個元素都乘上 {k}。",
                starter_code="def solve(arr):\n    pass\n",
                solution_code=f"def solve(arr):\n    return arr * {k}\n",
                tests=(
                    TestCase(args=([1, 2, 3],), expected=[1 * k, 2 * k, 3 * k]),
                    TestCase(args=([-1, 0, 4],), expected=[-1 * k, 0, 4 * k]),
                ),
                tags=("numpy", "array", "easy"),
            )
        )
    return out


def _gen_numpy_threshold_questions() -> list[Question]:
    out: list[Question] = []
    for t in range(0, 20):
        arr1 = [t - 1, t, t + 1, t + 2]
        arr2 = [t + 3, t - 3, t + 1]
        exp1 = sum(1 for x in arr1 if x > t)
        exp2 = sum(1 for x in arr2 if x > t)
        out.append(
            _q(
                qid=f"np_count_gt_{t}",
                title=f"Numpy: 計算大於 {t} 的數量",
                description=f"回傳陣列中嚴格大於 {t} 的元素個數。",
                starter_code="def solve(arr):\n    pass\n",
                solution_code=f"def solve(arr):\n    return int((arr > {t}).sum())\n",
                tests=(
                    TestCase(args=(arr1,), expected=exp1),
                    TestCase(args=(arr2,), expected=exp2),
                ),
                tags=("numpy", "array", "easy"),
            )
        )
    return out


def _gen_sliding_window_questions() -> list[Question]:
    out: list[Question] = []
    arrays = [
        [1, 3, -1, -3, 5, 3, 6, 7],
        [2, 1, 5, 1, 3, 2],
        [4, 2, 1, 7, 8, 1, 2, 8],
        [5, -2, 3, 4, -1, 2, 1],
        [10, 2, -10, 5, 20],
        [0, 0, 0, 0, 1],
        [9, 8, 7, 6, 5, 4],
        [1, -1, 1, -1, 1, -1, 1],
        [3, 3, 3, 3, 3],
        [7, 2, 5, 10, 8],
        [2, 4, 6, 8, 10, 12],
        [11, -4, 13, -5, 2, 9],
        [1, 2, 3, 4, 5, 6, 7],
        [8, -1, 3, 4, -6, 7, 2],
        [6, 1, 3, 2, 5, 4, 8],
    ]
    windows = [3, 2, 4, 3, 2, 3, 2, 3, 4, 2, 5, 3, 4, 2, 3]

    for i, (nums, w) in enumerate(zip(arrays, windows), start=1):
        def max_win_sum(a: list[int], k: int) -> int:
            best = sum(a[:k])
            cur = best
            for idx in range(k, len(a)):
                cur += a[idx] - a[idx - k]
                if cur > best:
                    best = cur
            return best

        ans1 = max_win_sum(nums, w)
        nums2 = list(reversed(nums))
        ans2 = max_win_sum(nums2, w)

        out.append(
            _q(
                qid=f"lc_window_max_sum_{i}",
                title=f"LeetCode 類型: 固定窗口最大和 #{i}",
                description="給 nums 與整數 k，回傳長度 k 的連續子陣列最大和。",
                starter_code="def solve(nums, k):\n    pass\n",
                solution_code=(
                    "def solve(nums, k):\n"
                    "    cur = sum(nums[:k])\n"
                    "    best = cur\n"
                    "    for i in range(k, len(nums)):\n"
                    "        cur += nums[i] - nums[i - k]\n"
                    "        best = max(best, cur)\n"
                    "    return best\n"
                ),
                tests=(
                    TestCase(args=(nums, w), expected=ans1),
                    TestCase(args=(nums2, w), expected=ans2),
                ),
                tags=("leetcode", "sliding-window", "medium"),
            )
        )
    return out


def _gen_longest_consecutive_questions() -> list[Question]:
    out: list[Question] = []
    cases = [
        [100, 4, 200, 1, 3, 2],
        [0, 3, 7, 2, 5, 8, 4, 6, 0, 1],
        [9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6],
        [1, 2, 0, 1],
        [10, 30, 20, 40],
        [5, 2, 99, 3, 4, 1, 100],
        [15, 16, 17, 20, 21],
        [-2, -1, 0, 1, 2, 10],
        [50, 51, 52, 53, 10],
        [6, 7, 8, 1, 2, 3, 4],
        [12, 11, 10, 9, 8],
        [3, 10, 2, 1, 20],
        [1, 9, 3, 10, 4, 20, 2],
        [1000, 1001, 2, 3, 4, 5],
        [13, 14, 15, 1, 2, 3],
    ]

    def longest(nums: list[int]) -> int:
        st = set(nums)
        best = 0
        for x in st:
            if x - 1 not in st:
                y = x
                while y in st:
                    y += 1
                best = max(best, y - x)
        return best

    for i, nums in enumerate(cases, start=1):
        nums2 = nums + [9999]
        out.append(
            _q(
                qid=f"lc_longest_consecutive_{i}",
                title=f"LeetCode: Longest Consecutive Sequence #{i}",
                description="回傳最長連續整數序列長度，要求 O(n) 想法。",
                starter_code="def solve(nums):\n    pass\n",
                solution_code=(
                    "def solve(nums):\n"
                    "    st = set(nums)\n"
                    "    best = 0\n"
                    "    for x in st:\n"
                    "        if x - 1 not in st:\n"
                    "            y = x\n"
                    "            while y in st:\n"
                    "                y += 1\n"
                    "            best = max(best, y - x)\n"
                    "    return best\n"
                ),
                tests=(
                    TestCase(args=(nums,), expected=longest(nums)),
                    TestCase(args=(nums2,), expected=longest(nums2)),
                ),
                tags=("leetcode", "hashset", "medium"),
            )
        )
    return out


def _gen_product_except_self_questions() -> list[Question]:
    out: list[Question] = []
    cases = [
        [1, 2, 3, 4],
        [-1, 1, 0, -3, 3],
        [2, 3, 4, 5],
        [5, 6, 7, 8],
        [1, 1, 1, 1],
        [9, 3, 2, 1],
        [4, 0, 2, 0],
        [10, -2, -3, 4],
        [8, 5, 2, 6],
        [3, 7, 11, 2],
        [6, 1, 9, 3],
        [2, 2, 2, 3],
        [7, 8, 9, 10],
        [12, 5, 4, 3],
        [1, 4, 2, 8],
    ]

    def pes(nums: list[int]) -> list[int]:
        n = len(nums)
        left = [1] * n
        right = [1] * n
        for i in range(1, n):
            left[i] = left[i - 1] * nums[i - 1]
        for i in range(n - 2, -1, -1):
            right[i] = right[i + 1] * nums[i + 1]
        return [left[i] * right[i] for i in range(n)]

    for i, nums in enumerate(cases, start=1):
        nums2 = nums[::-1]
        out.append(
            _q(
                qid=f"lc_product_except_self_{i}",
                title=f"LeetCode: Product of Array Except Self #{i}",
                description="回傳 output[i] = 陣列中除了 nums[i] 外其餘元素乘積，不可用除法。",
                starter_code="def solve(nums):\n    pass\n",
                solution_code=(
                    "def solve(nums):\n"
                    "    n = len(nums)\n"
                    "    out = [1] * n\n"
                    "    pref = 1\n"
                    "    for i in range(n):\n"
                    "        out[i] = pref\n"
                    "        pref *= nums[i]\n"
                    "    suf = 1\n"
                    "    for i in range(n - 1, -1, -1):\n"
                    "        out[i] *= suf\n"
                    "        suf *= nums[i]\n"
                    "    return out\n"
                ),
                tests=(
                    TestCase(args=(nums,), expected=pes(nums)),
                    TestCase(args=(nums2,), expected=pes(nums2)),
                ),
                tags=("leetcode", "array", "medium"),
            )
        )
    return out


def _gen_python_transform_questions() -> list[Question]:
    out: list[Question] = []
    for n in range(1, 21):
        out.append(
            _q(
                qid=f"py_square_plus_{n}",
                title=f"Python: 平方再加 {n}",
                description=f"回傳新 list，對每個元素 x 計算 x*x+{n}。",
                starter_code="def solve(nums):\n    pass\n",
                solution_code=f"def solve(nums):\n    return [x * x + {n} for x in nums]\n",
                tests=(
                    TestCase(args=([1, 2, 3],), expected=[1 + n, 4 + n, 9 + n]),
                    TestCase(args=([-1, 0, 4],), expected=[1 + n, 0 + n, 16 + n]),
                ),
                tags=("python", "list", "easy"),
            )
        )
    return out


def _build_bank() -> tuple[Question, ...]:
    questions: list[Question] = []
    questions.extend(_base_questions())
    questions.extend(_gen_numpy_scale_questions())
    questions.extend(_gen_numpy_threshold_questions())
    questions.extend(_gen_sliding_window_questions())
    questions.extend(_gen_longest_consecutive_questions())
    questions.extend(_gen_product_except_self_questions())
    questions.extend(_gen_python_transform_questions())
    return tuple(questions)


QUESTION_BANK: tuple[Question, ...] = _build_bank()
