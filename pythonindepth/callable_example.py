from collections import defaultdict

class CallCount:
    def __init__(self, initial_counts=None):
        self._counts = defaultdict(int, initial_counts or {})

    def __call__(self, argument):
        """Increment the call count for the given argument."""
        self._counts[argument] += 1
        return self._counts[argument]

    def get_count(self, argument):
        """Get the current count for a given argument."""
        return self._counts.get(argument, 0)

    def __repr__(self):
        """Return a string representation of the CallCount instance."""
        return f"CallCount({dict(self._counts)})"

    def reset(self, argument=None):
        """Reset the count for a specific argument or all counts."""
        if argument is None:
            self._counts.clear()
        else:
            self._counts[argument] = 0

if __name__ == "__main__":
    