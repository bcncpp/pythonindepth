#  Type Hints.
Starting from Python 3.5, in Python has been introduced the concept of gradual type system
keeping the language a dynamically typed language. We've the so called type hints.
A gradual type system:
- is optional. We can use or not, so the type checker should not emit warnings for code that has no type hints.
- does not catch errors at runtime. It's the developer responsibility to use linters and type-checkers for detecting errors.
- does not improve the performance. At the moment we do not in Python use the hints to perform better translation to bytecode.
Type checkers that we can use: s pytype,  Pyright, Pyre, Mypy.
We use Mypy.

```
#!/usr/bin/env python3
def rotate_string(s: str, count: int) -> str:
    tmp = [ x for x in s]
    for i in range(0, len(s)):
        tmp[(i+count) % len(tmp)] = s[i]
    return ''.join(tmp)
if __name__=="__main__":
    print(rotate_string("alabama", 1))
```
This is the complete typing, let's try to play a bit with it.  Suppose we want to to check the
typing with mypy.
```
jo@DESKTOP:~/python/mypy$ mypy --disallow-incomplete-defs rotate_0.py 
Success: no issues found in 1 source file
```

Ok let remove the typing hints:
```
#!/usr/bin/env python3 
def rotate_string(s : str, count):
    tmp = [ x for x in s]
    for i in range(0, len(s)):
        tmp[(i+count) % len(tmp)] = s[i]
    return ''.join(tmp)
if __name__=="__main__":
    print(rotate_string("alabama", 1))
```

```
jozoppi@DESKTOP-T9826C8:~/python/mypy$ mypy --disallow-incomplete-defs rotate_1.py 
messages_test_bug.py:3: error: Function is missing a return type annotation
messages_test_bug.py:3: error: Function is missing a type annotation for one or more arguments
Found 2 errors in 1 file (checked 1 source file)

```

Now we want to use the same index count for rotating the merge of two strings where the second might be present or not
```
#!/usr/bin/env python3

from typing import Optional
def rotate_string(count: int, s: str, s1: Optional[str]=None)->str:
    tmp = [ x for x in s]
    z = s
    if s1:
        for y in s1:
            tmp.append(y)
        z = z + s1
    for i in range(0, len(z)):
        tmp[(i+count) % len(z)] = z[i]
    return ''.join(tmp)
if __name__=="__main__":
    print(rotate_string(1,"alabama", "batonrouge"))
    print(rotate_string(1,"alabama"))
```
In this second case we see the optional parameter.

In a gradual type system, we have the interplay of two different views of types:
- Duck typing.  In Python duck typing is only enforced at runtime, when operations on objects are attempted
- Nominal typing.  Objects and variables have types. But objects only exist at runtime, and the type checker only cares about the source code where variables (including parameters) are annotated with type hints.

Let's clarify with an example.
```
#!/usr/bin/env python3
class Animal:
  pass
class Human:
    def eat(self)->str:
        return "Eat!"
    def speak(self)->str:
        return "Speak!"
class Employee(Human):
    def work(self):
        return "Work!"
class Manager(Human):
    def work(self):
        return "Work hard!"
# duck typing
def lifecycle(human):
    print(human.eat())
    print(human.speak())
    print(human.work())
# nominal typing
def lifecycle_employee(human: Employee)-> str:
    print(human.eat()) 
    print(human.speak())
    print(human.work())
if __name__=="__main__":
    m = Manager()
    e = Employee()
    print("Duck typing test")
    lifecycle(m)
    lifecycle(e)
    print("Nominal typing test")
    lifecycle_employee(m)
    lifecycle_employee(e)

```

Let's lunch this example:

```
jozoppi@DESKTOP:~/python/mypy$ ./ducknominaltyping.py 
Duck typing test
Eat!
Speak!
Work hard!
Eat!
Speak!
Work!
Nominal typing test
Eat!
Speak!
Work hard!
Eat!
Speak!
Work!
jozoppi@DESKTOP:~/python/mypy$ mypy ./ducknominaltyping.py
message_test_03.py:24: error: Missing return statement
message_test_03.py:37: error: Argument 1 to "lifecycle_employee" has incompatible type "Manager"; expected "Employee"
Found 2 errors in 1 file (checked 1 source file)
jozoppi@DESKTOP:~/python/mypy$
```

Work well but if we use the checker we've so called nominal typing check and avoid any misinterpreation at runtime.
```
    annotation for one or more arguments
```

Pretty much any Python type can be used in type hints, but there are restrictions and recommendations. In addition, the typing module introduced special constructs with semantics that are sometimes surprising.

This section covers all the major types you can use with annotations:

- typing.Any;
- Simple types and classes;
- typing.Optional and typing.Union;
- Generic collections, including tuples and mappings;
- Abstract Base Classes;
- Generic iterables;
- Parameterized generics and TypeVar;
- typing.Protocols—the key to static duck typing;
- typing.Callable;
- typing.NoReturn—a good way to end this list.
We’ll cover each of these in turn, starting with a type that is strange, apparently useless, but crucially important.


Typing Any.

```
def mul2(x):
    return x * 2
```
Is equivalent to :
```
def mul2(x: Any)->Any:
    return x * 2
```

```
#!/usr/bin/env python3
def is_divisible(x: object, y: object) -> object:
    for k in range(0, x):
        z = k * y 
        if z == x:
            return True
        elif z > x:
            break
    return False
if __name__=="__main__":
    print(is_divisible(99,3)) 
```

```
jozoppi@DESKTOP-T9826C8:~/python/mypy$ mypy --disallow-incomplete-defs divisible.py
divisible.py:3: error: No overload variant of "range" matches argument types "int", "object"
divisible.py:3: note: Possible overload variants:
divisible.py:3: note:    def __init__(self, SupportsIndex) -> range
divisible.py:3: note:    def __init__(self, SupportsIndex, SupportsIndex, SupportsIndex = ...) -> range
Found 1 error in 1 file (checked 1 source file)
jozoppi@DESKTOP-T9826C8:~/python/mypy$
```


Classes and OOP.




We call Liskov Substitution Principle is used to  defined is-sub-type-of  in terms of supported operations: if an object of type T2 substitutes an object of type T1 and the program still behaves correctly, then T2 is subtype-of T1.

```
class Base:
    def __init__(self, value : str)->None:
        self._value = value
    @property
    def value(self) ->str:
        return self._value
   
class SubClass(Base):
    def __init__(self, value): 
        super().__init__(value)
def show(b: Base) -> str:
    return b.value   
if __name__=="__main__":
    b = SubClass("Hello")
    print(show(b))

```

Consistent-With.
In a gradual type system, there is another relationship: consistent-with, which applies wherever subtype-of applies, with special provisions for type Any.

In a gradual type system The rules for consistent-with are:

1. Given T1 and a subtype T2, then T2 is consistent-with T1 (Liskov substitution).
2. Every type is consistent-with Any: you can pass objects of every type to an argument declared of type Any.
3. Any is consistent-with every type: you can always pass an object of type Any where an argument of another type is expected.


Simple types.




Simple types like int, float, str, bytes may be used directly in type hints.
Here is the case we've rules 'consistent-with':
- int is consistent-with float
- float is consistent-with complex, so also int it's.

Optional and Union hints
```

#!/usr/bin/env python3
from typing import Any
from typing import Optional
def show_results(count: int, singular: str, plural: Optional[str] = None) -> Optional[str]:
    pass
```

```
from typing import Union
def parse_token(token: str) -> Union[str, float]:
    try:
        return float(token)
    except ValueError:
        return token
```

Type hints in typing

```
list        collections.deque        abc.Sequence  abc.MutableSequence
set        abc.Container            abc.Set        abc.MutableSet
frozenset  abc.Collection
```

collection
type hint equivalent
list
typing.List
set
typing.Set
frozenset
typing.FrozenSet
collections.deque
typing.Deque
collections.abc.MutableSequence
typing.MutableSequence
collections.abc.Sequence
typing.Sequence
collections.abc.Set
typing.AbstractSet
collections.abc.MutableSet
typing.MutableSet

Tuple:
```
tuple[int,float]  -
# named tuple
from typing import NamedTuple
stuff: tuple[Any, ...]
stuff: tuple[int,...]

```

Generic mapping types are annotated as MappingType[KeyType, ValueType]. T

```
from typing import Dict
typing.Dict < Python 3.9
dict >=Python 3.9
```

```
Iterable
from collections.abc import Iterable
FromTo = tuple[str, str]  1
def zip_replace(text: str, changes: Iterable[FromTo]) -> str:  2
    for from_, to in changes:
        text = text.replace(from_, to)
    return text
Iterator
from collections.abc import Iterator

RE_WORD = re.compile(r'\w+')
STOP_CODE = sys.maxunicode + 1

def tokenize(text: str) -> Iterator[str]:  1
    """return iterable of uppercased words"""
    for match in RE_WORD.finditer(text):
        yield match.group().upper()
```

Read this:
```
https://www.python.org/dev/peps/pep-0544/
are similar to interfaces in go.
```