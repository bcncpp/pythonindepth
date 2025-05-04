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

## 🎯 Conclusion
- High Cohesion + Low Coupling = Better Design
- Aspect	Good Design (✅)	Bad Design (❌)
- Cohesion	One clear responsibility	Many unrelated duties
- Coupling	Uses interfaces, patterns	Instantiates dependencies directly

Use patterns like Dependency Injection and Observer to decouple responsibilities. Design each class or module to do one thing well, and make it easy to change, test, and reuse.