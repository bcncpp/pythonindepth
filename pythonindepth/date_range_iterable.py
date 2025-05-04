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

class GeneratorDateRangeContainerIterable:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __iter__(self):
        current_day = self.start_date
        while current_day < self.end_date:
            yield current_day
            current_day += timedelta(days=1)

if __name__=="__main__":
    from datetime import date
    for day in DateRangeIterable(date(2018, 1, 1), date(2018, 1, 5)):
        print(day)