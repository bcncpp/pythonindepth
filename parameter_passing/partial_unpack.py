def show(e, rest):
    print("Element: {0} - Rest: {1}".format(e, rest))


first, *rest = [1, 2, 3, 4, 5]
show(first, rest)

*rest, last = range(6)
show(last, rest)

print()

first, *middle, last = range(6)
print(first)
print(middle)
print(last)

print()

first, last, *empty = 1, 2
print(first)
print(last)
print(empty)
