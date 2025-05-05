# Loosely Coupled vs. Highly Coupled Systems

In software design, two critical concepts that significantly impact the maintainability, flexibility, and scalability of your system are cohesion and coupling. Mastering both leads to more modular, robust code that's easier to work with and extend.

## 🔍 Understanding the Concepts

## Cohesion
Cohesion means that an object or module should have a small, well-defined responsibility. Highly cohesive classes do one thing and do it well—like Unix commands. They are easier to reuse, test, and reason about.

### Coupling

Coupling refers to the degree of dependency between two modules or classes. High coupling means parts are tightly connected and dependent on each other's inner workings—making change difficult and error-prone.

Problems with high coupling:
- ❌ Low code reuse
- ❌ Ripple effects on change
- ❌ Blurred abstraction boundaries

### ✅ Loosely Coupled Example: Constructor Injection

```python
class UserService:
    """Handles user-related operations."""
    
    def __init__(self, email_service):
        self.email_service = email_service
    
    def create_user(self, user):
        # Logic to create user
        self.email_service.send_welcome_email(user.email)

class EmailService:
    """Handles sending emails."""
    
    def send_welcome_email(self, email):
        print(f"Sending welcome email to {email}")

# Usage
email_service = EmailService()
user_service = UserService(email_service)
user_service.create_user(user={"email": "user@example.com"})
```
#### Why it's loosely coupled:

- UserService does not directly create EmailService—it uses an abstraction.

- The classes have clear, cohesive roles.

- Easier to test and replace dependencies.

### ✅ Loosely Coupled Example 2: Observer Pattern

A common way to achieve loose coupling is with event-driven programming, using the Observer Pattern.

```python
class EventPublisher:
    """Manages subscribers and notifies them of events."""
    
    def __init__(self):
        self.subscribers = []
    
    def subscribe(self, listener):
        self.subscribers.append(listener)
    
    def publish(self, event):
        for listener in self.subscribers:
            listener.notify(event)

class EmailNotifier:
    def notify(self, event):
        print(f"[EmailNotifier] Received event: {event}")

class Logger:
    def notify(self, event):
        print(f"[Logger] Logged event: {event}")

# Usage
publisher = EventPublisher()
publisher.subscribe(EmailNotifier())
publisher.subscribe(Logger())

publisher.publish("user_registered")
```
#### Why this is loosely coupled:
 
 - Publishers don't need to know what subscribers do.
 - Subscribers can be added or removed without changing the publisher.
 - Each class is cohesive and does one job.

### ❌ Highly Coupled Example

```python 
class UserService:
    """Handles user-related operations."""
    
    def create_user(self, user):
        email_service = EmailService()
        email_service.send_welcome_email(user.email)

class EmailService:
    """Handles sending emails."""
    
    def send_welcome_email(self, email):
        print(f"Sending welcome email to {email}")

# Usage
user_service = UserService()
user_service.create_user(user={"email": "user@example.com"})
```
#### Why this is highly coupled:

- UserService is tightly bound to EmailService.
- Cannot easily test UserService without EmailService.
- Code is harder to reuse or extend.


## Coupling and function arguments

One subtle indicator of tight coupling is the number of arguments a function signature takes.
The more arguments a function has, the more likely it is to be tightly coupled to its caller. Let’s dive deeper into this concept, exploring why this is the case and how we can address it with better design choices.

## 📌 The Problem with Too Many Parameters

Let's take two functions, f1 and f2. Suppose f2 takes five parameters. The larger the number of parameters f2 has, the harder it is for the calling function (f1) to gather all the required information and correctly call f2.

In this case, the tight coupling occurs because f1 must have knowledge of the parameters f2 needs, making the system less abstract and more fragile.
### 🚨 Why Too Many Arguments Are a Problem

1. Leaky Abstraction

The more parameters a function requires, the more likely it is that the caller (f1) will need to know the internal details of the called function (f2). This breaks the abstraction barrier. A clean abstraction is supposed to hide internal complexities, but with many parameters, the caller ends up being responsible for knowing or managing them all. This makes f2 a leaky abstraction, because f1 can deduce how f2 works internally based on the data it passes.
Example: Leaky Abstraction

```python
def f2(param1, param2, param3, param4, param5):
    # Function logic depends on all 5 parameters
    result = param1 + param2 - param3 * param4 / param5
    return result

def f1():
    # f1 has to know about the 5 parameters to call f2 correctly
    result = f2(10, 20, 30, 40, 50)
    print(result)
```

In this example:

- f1 has to pass the correct arguments in the correct order, making it difficult to change f2 without altering f1 accordingly.

- If f2 is only used in f1, it will be hard to reuse it elsewhere. The signature is too specific and not generalized for other use cases.

2. Hard to Reuse

The more parameters a function requires, the harder it becomes to reuse. If f2 is heavily dependent on a complex set of inputs, the caller (f1) needs to match all the parameters exactly. This rigid dependency makes it nearly impossible to use f2 in a different context or with different arguments without significant overhead.

### 🛠️ How to Fix This: Reducing the Number of Parameters

Instead of forcing functions to depend on a large number of parameters, we can encapsulate those parameters into objects or data structures that contain all the required information. This improves cohesion and reduces coupling. The key is to simplify the function signatures by using data structures that represent groups of related parameters.
#### 🧑‍💻 Example of Loosely Coupled Functions

Instead of having a function f2 that takes five parameters, let's encapsulate them into a single object or dictionary. By doing this, we reduce the number of arguments and make the code more reusable.
Solution: Using a Data Object

```python

class Params:
    """Represents the parameters needed by f2."""
    def __init__(self, param1, param2, param3, param4, param5):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4
        self.param5 = param5

class Processor:
    """A class responsible for processing the parameters."""
    @staticmethod
    def f2(params: Params):
        result = params.param1 + params.param2 - params.param3 * params.param4 / params.param5
        return result

class Caller:
    """Caller function that uses Processor to handle parameters."""
    def f1(self):
        params = Params(10, 20, 30, 40, 50)
        result = Processor.f2(params)
        print(result)

# Usage
caller = Caller()
caller.f1()
```

## Why is this better?

 - f2 no longer needs to depend on multiple arguments directly. It only takes one argument—params, an encapsulated object that holds the data.
 - This reduces the coupling between f1 and f2. Now, f1 only needs to create the Params object and pass it to f2.
 -  If we need to change how the parameters are passed to f2, we only need to modify the Params class and the Processor class, not every caller of f2.

###  Key Takeaways
1. Reducing the Number of Arguments
When you have a function with many parameters, it usually signals tight coupling with its caller. By grouping related parameters into a class or data structure, you reduce the complexity of the function signature and make it easier to maintain.

2. Leaky Abstractions

Functions that depend on a large number of parameters are often leaky abstractions. The caller often ends up understanding the internal workings of the function, which reduces modularity.

3. Reusability and Flexibility
With fewer arguments and a clear abstraction, you improve the reusability of the function. If the function signature is small and simple, 
it's easier to plug the function into other contexts without major changes.
4. Maintainability
By encapsulating parameters, you make the code easier to modify without introducing changes in multiple places. This leads to a more maintainable codebase.


## 🎯 Conclusion
- High Cohesion + Low Coupling = Better Design
- Aspect	Good Design (✅)	Bad Design (❌)
- Cohesion	One clear responsibility	Many unrelated duties
- Coupling	Uses interfaces, patterns	Instantiates dependencies directly

Use patterns like Dependency Injection and Observer to decouple responsibilities. Design each class or module to do one thing well, and make it easy to change, test, and reuse.

