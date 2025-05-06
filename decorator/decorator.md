## Class Decorator.
1. Reusability and DRY Principle

    - Reusability is one of the main benefits of decorators. Instead of rewriting the same logic in multiple places, you can write it once in a decorator and apply it to multiple classes. This avoids redundancy (DRY—Don't Repeat Yourself). For example, a decorator that enforces logging or validation rules across various classes or event types ensures that your code remains concise and clean.

    Example: You could apply a logging decorator that logs class method invocations for every event class in your system, without needing to write this logging logic in each class itself.

2. Simplification of Classes

    Smaller or simpler classes can be enhanced later on. Decorators allow you to keep the class focused on its core functionality (e.g., a simple LoginEvent class), and apply additional logic such as serialization, validation, or logging separately.
    This improves separation of concerns—each class can focus on its primary task, and its "enhancements" (such as serialization) are applied through decorators.

3. Easier to Maintain
    Easier to maintain transformation logic: If you apply some transformation or enhancement (like serialization or logging) using decorators, this logic is kept separate from the class's core implementation. This keeps your classes clean and makes the logic easier to change or update.

    Decorators are simpler and more maintainable compared to using metaclasses, which can quickly become complex and difficult to understand.

    Example: If you wanted to change how events are serialized (perhaps to a different format), you could modify the decorator's serialize() method rather than altering each class individually.

### Cons of Using Decorators for Classes

    - Increased Complexity

        While decorators help in keeping classes smaller, it can add complexity when debugging. It may be difficult to trace where specific behavior is coming from because decorators operate "behind the scenes."
        For example, if you have multiple decorators stacked on top of each other, it can be harder to figure out which decorator is responsible for certain behavior, especially when exceptions are raised.

    - Hidden Logic
        Sometimes, decorators can obscure the behavior of a class. Developers might not immediately know that a class is being modified or enhanced by a decorator, leading to confusion or misuse.
        The decorator-based transformation might not be immediately obvious when inspecting the class, making it harder for new developers to understand the code's full behavior.

    - Potential for Overuse
        Overusing decorators can make code harder to follow. If you apply too many decorators to classes, it may reduce the clarity of how a class behaves.
        Decorators should be used judiciously to avoid making the codebase more difficult to navigate.

### Comparison with Metaclasses

    - Metaclasses: These are more powerful but can be complex and hard to maintain. They allow for manipulation of class creation itself, which can lead to confusion if not used carefully.

        - Metaclasses can alter class inheritance, method definitions, and behavior before the class is created.

        - Downside: They can be difficult to debug and may make the class logic harder to understand.

    - Decorators: While more lightweight than metaclasses, they allow you to wrap or modify the behavior of classes and their methods in a simpler and more modular way. This makes decorators easier to understand and maintain compared to metaclasses.


Let's take an example. We've a LoginEvent and we want to serialize it. The serialization is always a crosscut concern.

```python
from datetime import datetime
from dataclasses import dataclass

class LoginEventSerializer:
    def __init__(self, event):
        self.event = event

    def serialize(self) -> dict:
        return {
            "username": self.event.username,
            "password": "**redacted**",
            "ip": self.event.ip,
            "timestamp": self.event.timestamp.strftime("%Y-%m-%d %H:%M"),
        }

@dataclass
class LoginEvent:
    SERIALIZER = LoginEventSerializer
    username: str
    password: str
    ip: str
    timestamp: datetime

    def serialize(self) -> dict:
        return self.SERIALIZER(self).serialize()

if __name__ == "__main__":
    # Creating instance of Login Event
    event = LoginEvent(
        username="usr",
        password="pwd",
        ip="1.0.0.0",
        timestamp=datetime.now()
    )

    # Serialize the instance and print
    serialized = event.serialize()
    print(serialized)
```

As the time passes we found in our code bases the following issues:

- *Too many classes*: As the number of events grows, the number of serialization classes will grow in the same order of magnitude, because they are mapped one to one. The solution is not flexible enough: If we need to reuse parts of the components (for example, if we need to hide the password in another type of event that also has it), we'll have to extract this into a function, but also call it repeatedly from multiple classes, meaning that we are not reusing that much code after all.

- *Boilerplate*: The serialize() method will have to be present in all event classes, calling the same code. Although we can extract this into another class (creating a mixin), it doesn't seem like a good use of inheritance.

We need to separate the serialization in one place and  the resposability to  the classes we want to support the serialization.
A class decorator is perfect for this task. So we proceed to refactor the code in the following:


```python
from dataclasses import dataclass
from datetime import datetime
from functools import wraps

def serializable_login_event(cls):
    def serialize(self) -> dict:
        return {
            "username": self.username,
            "password": "**redacted**",  # Do not log sensitive data
            "ip": self.ip,
            "timestamp": getattr(self, "timestamp", None),
        }
    cls.serialize = serialize
    return cls

@serializable_login_event
@dataclass
class LoginEvent:
    username: str
    password: str
    ip: str
    timestamp: datetime = datetime.now()

# Usage
event = LoginEvent(username="john_doe", password="secret", ip="192.168.0.1")
print(event.serialize())
```

## Key Concepts: Decorators and Function Nesting

### Basic Decorator Structure:
 A decorator is essentially a higher-order function that takes a function as input, does something with it (like modifying its behavior), and then returns the modified function.
 The decorator is applied to a function using the @ syntax, which is shorthand for passing the function to the decorator.
 When you want to pass parameters to a decorator, you need another level of indirection. The first function in the chain accepts the parameters and returns a decorator function. The decorator then wraps the original function, applying the changes, and finally, the wrapped function is returned.

### Multiple Levels of Nesting:
  - Level 1: A function that takes parameters (e.g., the number of retries).
  - Level 2: The decorator function itself that wraps the original function.
  - Level 3: The wrapped function (the one that gets modified).

```python
import time
import functools
# Level 1: Function that accepts parameters (number of retries)
def retry(retries=3, delay=1):
    # Level 2: The actual decorator function
    def decorator(func):
        # Level 3: The wrapped function with retry logic
        @functools.wraps(func)  # Keeps original function's signature and metadata
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)  # Try to run the original function
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")
                    if attempts < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)  # Wait before retrying
                    else:
                        print("Max retries reached. Giving up.")
                        raise e  # After retries are exhausted, raise the exception
        return wrapper
    return decorator

# Example function that could fail
@retry(retries=5, delay=2)
def some_function():
    print("Trying to do something risky...")
    # Simulating a failure
    raise ValueError("Something went wrong!")

# Calling the function
try:
    some_function()
except Exception as e:
    print(f"Function failed with error: {e}")

```
This might lead to much nesting. There's a different way of implementing decorators, which instead of using nested functions uses objects. We'll explore that now. An alternative way might be to have a class to define a decorator and put the decorator magic in **__call**, 
so we've a callable object.
```python
from functools import wraps
from typing import Optional, Sequence

from log import logger

_DEFAULT_RETRIES_LIMIT = 3

class ControlledException(Exception):
    """A generic exception on the program's domain."""

class WithRetry:
    def __init__(
        self,
        retries_limit: int = _DEFAULT_RETRIES_LIMIT,
        allowed_exceptions: Optional[Sequence[Exception]] = None,
    ) -> None:
        self.retries_limit = retries_limit
        self.allowed_exceptions = allowed_exceptions or (ControlledException,)

    def __call__(self, operation):
        @wraps(operation)
        def wrapped(*args, **kwargs):
            last_raised = None
            for _ in range(self.retries_limit):
                try:
                    return operation(*args, **kwargs)
                except self.allowed_exceptions as e:
                    logger.warning(
                        "retrying %s due to %s", operation.__qualname__, e
                    )
                    last_raised = e
            raise last_raised

        return wrapped
```
The decorator is pretty much obvious:
```python
@WithRetry(retries_limit=5)
def run_with_custom_retries_limit(task):
    return task.run()
```

Now we want to add decorators with default values.
### Key Concepts
- Decorator with Parameters: You want the decorator to accept parameters (like x and y), but at the same time, you want to ensure it works without parameters as well (default values should be used).
    1. functools.wraps: Ensures that the decorated function retains its original name, docstring, and other attributes.
    2. functools.partial: It's not strictly needed here because you're already handling parameters in the decorator directly, but it can be useful for pre-filling arguments in other cases.

### Corrected and Optimized Code
Let me explain your code with some improvements:
```python
from functools import wraps

DEFAULT_X = 1
DEFAULT_Y = 2

# Creating the decorator function
def decorator(function=None, *, x=DEFAULT_X, y=DEFAULT_Y): 
    if function is None:  # called as `@decorator(x=3, y=4)`
        def decorated(function):
            @wraps(function)
            def wrapped(*args, **kwargs):
                # Pass parameters with default values
                return function(x, y)
            return wrapped
    else:  # called as `@decorator`
        @wraps(function)
        def wrapped(*args, **kwargs):
            # Pass parameters with default values
            return function(x, y)
        
    return wrapped

# Applying the decorator with parameters
@decorator(x=3, y=4)
def my_function(x, y):
    print("result =", x + y)
    return x + y

my_function()  # 7
```

1. Handling function=None:
   This allows the decorator to be applied both with parameters (@decorator(x=3, y=4)) and without (@decorator). When function=None, the decorator must return another function (decorated) that will later accept the actual function and apply the logic.

2. wrapped Function:
    The wrapped function should accept arbitrary arguments (*args and **kwargs), even though you're only passing x and y here. This ensures that the decorator remains flexible if you need to pass more arguments to the decorated function in the future.
    The decorator still applies the default values (x=DEFAULT_X, y=DEFAULT_Y) when no arguments are provided by the user.

3. @wraps(function):
    This is important to preserve the original function's signature and metadata (name, docstring, etc.) after the decorator wraps it.

### Behavior of the Code

    With Parameters (@decorator(x=3, y=4)): When you apply the decorator with parameters, those parameters are passed directly to the decorated function. With Defaults (@decorator): When the decorator is used without parameters, the defaults (DEFAULT_X=1, DEFAULT_Y=2) are used.

#### Final Thoughts
    - **functools.partial**: In this case, functools.partial is not strictly needed, because you're already handling the parameters inside the decorator function itself. However, partial can be useful if you need to pre-set specific arguments of a function and pass the rest dynamically. 
Decorator Design: This approach works well because it provides flexibility—allowing the decorator to function both with and without parameters.


    