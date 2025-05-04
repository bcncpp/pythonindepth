
Iteration works in Python by its own protocol (namely the iterator protocol). 
When we try to iterate an object in the form for e in myobject:..., what Python checks at a very high level are these two things, in order:
- Whether the object contains one of the iterator methods—__next__ or __iter__.
- Whether the object is a sequence and has __len__ and __getitem__.
```python

from datetime import timedelta

class DateRangeIterable:
    """An iterable that contains its own iterator object."""

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        return self

    def __next__(self):
        if self._present_day >= self.end_date:
            raise StopIteration()
        today = self._present_day
        self._present_day += timedelta(days=1)
        return today
```