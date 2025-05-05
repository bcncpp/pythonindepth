
Dependency Inversion Principle.

As stated DIP **high-level modules should not depend on low-level modules, but both should depend on abstractions**.
In simpler terms, it promotes the use of interfaces or protocols to reduce tight coupling between different components and
enforce a clear separation of modules.

### Bad Example: Violating the Dependency Inversion Principle
Suppose you have to process a lot of events from an external application and send them to the system log **syslog**.
Your collegue has implemented a high-level class EventProcessor that processes events and writes them directly to a SyslogWriter. That tightly couples the processor to a specific logging mechanism.
```python
class SyslogWriter:
    def write(self, message: str):
        print(f"[syslog] {message}")

class EventProcessor:
    def __init__(self):
        self.logger = SyslogWriter()  # Direct dependency on a low-level module

    def process(self, event: str):
        # Some processing logic...
        self.logger.write(f"Processed event: {event}")
```
Since you know SOLID you notic that:

- EventProcessor is a high-level module responsible for event logic.
- It is directly tied to SyslogWriter, a low-level module.


There is no abstraction, so you can’t easily:

- Swap in a different logging mechanism (e.g., Kafka, file, cloud logger).
- Unit test EventProcessor in isolation (you'd have to mock SyslogWriter).

This violates DIP because the high-level class is not independent of the concrete implementation and the result is not a modular system.
So you propose the fix:

1. create a common interface (abstraction).

```python
from abc import ABC, abstractmethod

class EventLogger(ABC):
    @abstractmethod
    def write(self, message: str):
        """Write a log message"""
        pass
```
Since a new requirement has been issue, store the logs also in Kafka, you extend the EventLogger providing specific implementation.

```python
class SyslogWriter(EventLogger):
    def write(self, message: str):
        print(f"[syslog] {message}")

class KafkaLogger(EventLogger):
    def write(self, message: str):
        print(f"[kafka] {message}")

```
Now the event processor uses the interface EventLogger and you can inject the dependency.

```python
class EventProcessor:
    def __init__(self, logger: EventLogger):
        self.logger = logger

    def process(self, event: str):
        # Event processing logic...
        self.logger.write(f"Processed event: {event}")
```

The mental model here is A (*EventProcessor*) and B (*SyslogWriter*) collaborate. A works with an instance of B, but as it turns out, our module doesn't control B directly (it might be an external library, or a module maintained by another team, and so on). 
If our code heavily depends on B, when this changes the code will break. To prevent this, we have to invert the dependency: Make B have to adapt to A. This is done by presenting an interface and forcing our lscode not to depend on the concrete implementation of B, but rather on the interface we have defined. It is then B's responsibility to comply with that interface.
