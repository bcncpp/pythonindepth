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