from bisect import bisect_left
from typing import Iterable

class Bag:
    def __init__(self, input: Iterable = ()):
        self._sorted_list = sorted(input)

    def __contains__(self, x):
        # Use binary search for O(log n) lookup
        idx = bisect_left(self._sorted_list, x)
        return idx < len(self._sorted_list) and self._sorted_list[idx] == x
    
