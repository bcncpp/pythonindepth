
A contract is a construction that enforces some rules that must be honored during the communication between software components. A contract mainly entails preconditions and postconditions, but in some cases, invariants, 
and side effects are also described:

- Preconditions: We can say that these are all the checks the code will perform before running. It will check for all the conditions that have to be made before the function can proceed. In general, it's implemented by validating the dataset provided in the parameters passed, but nothing should stop us from running all sorts of validations (for example, validating a set in a database, a file, or another method that was called before) if we consider that their side effects are overshadowed by the importance of such validations. Note that this imposes a constraint on the caller.
- Postconditions: These are opposite of preconditions. Here, the validations are done after the function call is returned. Postcondition validations are run to validate what the caller is expecting from this component.
- Invariants: Optionally, it would be a good idea to document, in the docstring of a function, the invariants, the things that are kept constant while the code of the function is running, as an expression of the logic of the function to be correct.
- Side effects: Optionally, we can mention any side effects of our code in the docstring.

The reason why we might design by contract is that if errors occur, they must be easy to spot (and by noticing whether it was either the precondition or postcondition that failed, we will find the culprit much more easily) so that they can be quickly corrected. More importantly, 
we want critical parts of the code to avoid being executed under the wrong assumptions. 

The idea is that preconditions bind the client 
(they have an obligation to meet them if they want to run some part of the code), whereas postconditions 
bind the component in relation to some guarantees that the client can verify and enforce.

For Python, in particular, since it is dynamically typed, this also means that sometimes we need to check for the exact type of data that is provided. This is not exactly the same as type checking. 
The mypy tool would do this, but verifies the exact values that are needed.
Part of these checks can be detected early on by using static analysis tools, such as mypy, 
but these checks are not enough. 
A function should have proper validation for the information that it is going to handle