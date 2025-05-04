# Handle Exception at the Right Level of Abstraction

Proper exception handling is a critical part of building robust and maintainable systems. However, it's essential to handle exceptions at the correct level of abstraction to ensure the code is both secure and maintainable. Handling exceptions at the wrong level can obscure important details or expose sensitive information to the user.

### The Bad Example: Mixing Concerns and Losing Abstraction

In the following code, the exception handling is done incorrectly by mixing concerns in a single block. There are also issues with the re-raising of exceptions and the loss of context, which can confuse developers trying to debug issues.

```python
import logging
import time

from base import Connector, Event

logger = logging.getLogger(__name__)

class DataTransport:
    """An example of an object handling exceptions of different levels."""
    _RETRY_BACKOFF: int = 5
    _RETRY_TIMES: int = 3

    def __init__(self, connector: Connector) -> None:
        self._connector = connector
        self.connection = None

    def deliver_event(self, event: Event):
        try: 
            self.connect()
            data = event.decode()  # ❌ Decoding before sending is fine, but mixing concerns in one block blurs responsibility.
            self.send(data)
        except ConnectionError as e:
            logger.info("connection error detected: %s", e)
            raise  # ❌ Re-raising without context loses the abstraction boundary. Use `raise ... from ...`.
        except ValueError as e:
            logger.error("%r contains incorrect data: %s", event, e)
            raise  # ❌ Again, no chaining or domain-specific exception used.

    def connect(self):
        for _ in range(self._RETRY_TIMES):
            try:
                self.connection = self._connector.connect()
            except ConnectionError as e:
                logger.info(
                    "%s: attempting new connection in %is", e, self._RETRY_BACKUP,  # ❌ Typo: _RETRY_BACKOFF used inconsistently as _RETRY_BACKUP
                )
                time.sleep(self._RETRY_BACKOFF)
            else: 
                return self.connection
        raise ConnectionError(f"Couldn't connect after {self._RETRY_TIMES} times")  # ❌ Generic exception message, no context.

    def send(self, data: bytes):
        return self.connection.send(data)  # ❌ No exception handling; failure here could be opaque to `deliver_event`.
```

## Why This Code Is Bad

- *Mixing concerns*: The method deliver_event both decodes the event and sends it. These are two separate concerns and should ideally be handled in different methods.

- *Re-raising exceptions without context*: Re-raising exceptions without adding context using ```raise ... from ...``` loses important information about where the exception originated. This makes debugging harder.

- *Lack of domain-specific exceptions*: Generic exceptions like ```ConnectionError``` and ```ValueError`` are raised directly in business logic, but they lack meaning in the context of the application.

- *Inconsistent error handling*: The connect method raises a generic ConnectionError without enough context, while the send method does not handle exceptions at all.

## The Fixed Version: Properly Handling Exceptions with Context

In this improved version, we fix the above issues by handling exceptions at the appropriate level of abstraction. We introduce custom exception classes that convey more meaningful information about specific problems and make use of exception chaining for better context.

```python
import logging
import time

from base import Connector, Event

logger = logging.getLogger(__name__)

class ConnectionFailedError(Exception):
    """Raised when all connection retries fail."""

class EventDeliveryError(Exception):
    """Raised when an event could not be delivered."""

class EventDecodeError(Exception):
    """Raised when an event cannot be decoded."""

class DataTransport:
    """Handles transport of events with clear exception boundaries."""
    _RETRY_BACKOFF: int = 5
    _RETRY_TIMES: int = 3

    def __init__(self, connector: Connector) -> None:
        self._connector = connector
        self.connection = None

    def deliver_event(self, event: Event):
        try:
            self.connect()
            data = self.decode_event(event)
            self.send(data)
        except (ConnectionFailedError, EventDecodeError) as e:
            raise EventDeliveryError("Failed to deliver event") from e

    def connect(self):
        for attempt in range(1, self._RETRY_TIMES + 1):
            try:
                self.connection = self._connector.connect()
                return self.connection
            except ConnectionError as e:
                logger.info(
                    "Attempt %d failed: %s. Retrying in %d seconds...",
                    attempt, e, self._RETRY_BACKOFF
                )
                time.sleep(self._RETRY_BACKOFF)
        raise ConnectionFailedError(
            f"All {self._RETRY_TIMES} connection attempts failed."
        )

    def decode_event(self, event: Event) -> bytes:
        try:
            return event.decode()
        except ValueError as e:
            logger.error("Failed to decode event %r: %s", event, e)
            raise EventDecodeError("Event could not be decoded") from e

    def send(self, data: bytes):
        try:
            self.connection.send(data)
        except Exception as e:
            logger.error("Sending failed: %s", e)
            raise

```

## Why the Fixed Version is Better

- *Separation of concerns*: The responsibilities of connecting, decoding, and sending data are handled in separate methods.

- *Chained exceptions*: When an exception is raised, the context of the original exception is preserved, making debugging easier.

- *Custom domain-specific exceptions*: We define exceptions like ConnectionFailedError and EventDecodeError that are more meaningful in the context of the application. This improves the clarity of error handling and makes it easier to understand what went wrong.

- *Error propagation*: The deliver_event method catches exceptions from different layers and raises a higher-level exception (EventDeliveryError) to indicate that something went wrong during the delivery process. This is more maintainable and readable.


## Security Implications: Don't Expose Tracebacks to Users

When handling exceptions, it's important not to expose sensitive details, such as tracebacks, to the end user. Exposing this information can create a security risk by revealing internal structure, file paths, or other potentially sensitive data.

Here's a bad example where an exception message is directly shown to the user:
```python
def process_user_input(data):
    try:
        # some risky operation
        result = int(data)
        return f"Processed value: {result}"
    except Exception as e:
        # ❌ BAD: Exposes internal details to the user
        return f"An error occurred: {e}"
```

## Why this is bad:

- Exposing internal details: The error message includes information about the internal exception, such as class names or system configurations.

- Security risk: This can lead to attackers gaining insight into your application's internals, which can be exploited.

- Poor user experience: A technical stack trace is not helpful for non-technical users and could confuse or frustrate them.



## Handle Specific Exceptions in Your Domain

A generic except clause that catches all exceptions is harmful. It silences all errors, and you lose control over the flow. Instead, handle specific exceptions that you know can happen and propagate them with context.

For example, if you're working with a dictionary and want to handle the absence of a key:
```python
class InternalDataError(Exception):
    """Exception related to our domain problem."""

def process(data_dictionary, record_id):
    try:
        return data_dictionary[record_id]
    except KeyError as e:
        raise InternalDataError("Record not present") from e
```
This approach provides better clarity and control over the exceptions that occur, making your code more maintainable and secure.

