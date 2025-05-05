### Open/Close Principle

The Open/Closed Principle (OCP) is one of the five SOLID principles of object-oriented design. It states that a class (or module) should be open for extension, meaning it can accommodate new functionality, but closed for modification, meaning you shouldn’t have to modify existing code to extend its behavior. This principle encourages the design of flexible, maintainable code where new functionality can be added without altering existing implementations.
Bad Example: Violating the Open/Closed Principle

Here’s an example that violates the Open/Closed Principle. Suppose we have a PaymentProcessor class that processes payments of different types (credit card, PayPal, etc.).
```python
class PaymentProcessor:
    def process_payment(self, payment_type, amount):
        if payment_type == "credit_card":
            self.process_credit_card(amount)
        elif payment_type == "paypal":
            self.process_paypal(amount)
        else:
            raise ValueError("Unsupported payment type")

    def process_credit_card(self, amount):
        print(f"Processing credit card payment of {amount}")

    def process_paypal(self, amount):
        print(f"Processing PayPal payment of {amount}")
```
### Why is this bad?

- Modifying the class for new payment types: Every time we need to add a new payment type (e.g., Bitcoin, Apple Pay, etc.), we must modify the PaymentProcessor class by adding more elif conditions.

This violates OCP because we are modifying the existing class rather than extending its behavior. If the PaymentProcessor class is used in many parts of a system, modifying it each time we add a new payment type increases the risk of breaking other parts of the system.

Good Example: Following the Open/Closed Principle

Now, let's refactor the code to follow OCP. We’ll use polymorphism to allow for new payment types to be added without modifying the PaymentProcessor class.
```python
from abc import ABC, abstractmethod

# Base class for payment types
class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount):
        pass

# Concrete implementation for credit card payment
class CreditCardPayment(PaymentMethod):
    def process(self, amount):
        print(f"Processing credit card payment of {amount}")

# Concrete implementation for PayPal payment
class PayPalPayment(PaymentMethod):
    def process(self, amount):
        print(f"Processing PayPal payment of {amount}")

# Concrete implementation for Bitcoin payment
class BitcoinPayment(PaymentMethod):
    def process(self, amount):
        print(f"Processing Bitcoin payment of {amount}")

# PaymentProcessor class is now closed to modification and open for extension
class PaymentProcessor:
    def process_payment(self, payment_method: PaymentMethod, amount):
        payment_method.process(amount)
```
## Why is this good?

- No modification of existing code: If we need to add a new payment type, we can simply create a new class that implements the PaymentMethod interface. We don’t have to modify the PaymentProcessor class at all.
- Open for extension, closed for modification: The PaymentProcessor is closed for modification because we don’t need to touch it for new functionality (new payment methods). However, it is open for extension because new payment types can be easily added by creating new classes that implement the PaymentMethod interface.
- Polymorphism: The process_payment method works with any subclass of PaymentMethod, allowing for easy expansion with different payment types.

### Key Takeaways

- Bad Example: Modifying an existing class to add new functionality, which leads to tightly coupled and harder-to-maintain code.

- Good Example: Using abstraction and polymorphism to extend functionality by adding new classes without modifying existing ones. This ensures that the system is flexible, maintainable, and scalable.

By following the Open/Closed Principle, we create a system that is more maintainable, easier to extend, and less prone to errors when new requirements emerge.

### Conclusion:

As you might have noticed, this principle is closely related to the effective use of polymorphism. We want to work towards designing abstractions that respect a polymorphic contract that the client can use, to a structure that is generic enough that extending the model is possible, as long as the polymorphic relationship is preserved.

This principle tackles an important problem in software engineering: **maintainability**. The perils of not following the OCP are ripple effects and problems in the software where a single change triggers changes all over the code base, or risks breaking other parts of the code.

One important final note is that, in order to achieve this design in which we don't change the code to extend behavior, we need to be able to create proper closure against the abstractions we want to protect (in this example, new types of events). This is not always possible in all programs, as some abstractions might collide (for example, we might have a proper abstraction that provides closure against a requirement but doesn't work for other types of requirements). In these cases, we need to be selective and apply a strategy that provides the best closure for the types of requirements that require being the most extensible.