## Interface segregation principle

The interface segregation principle (ISP) provides some guidelines for an idea that we have covered repeatedly already: that interfaces should be small. In object-oriented terms, an interface is represented by the set of methods and properties an object exposes. That is to say that all the messages that an object is able to receive or interpret constitute its interface, and this is what other clients can request. 

### Interfaces should be smaller.

```python

from abc import ABCMeta, abstractmethod 

class YAMLEventParser(metaclass=ABCMeta):
    @abstractmethod
    def from_xml(xml_data: str):
        """Parse an event from a source in XML representation."""

class JSONEventParser(metaclass=ABCMeta):
    @abstractmethod
    def from_json(json_data: str):
        """Parse an event from a source in JSON format."""

    
class EventParser(YAMLEventParser, JSONEventParser):
    """An event parser that can create an event from source data either in XML or JSON format.
    """

    def from_xml(xml_data):
        pass

    def from_json(json_data: str):
        pass

```

## How small can be?
A base class (abstract or not) defines an interface for all the other classes to extend it. The fact that this should be as small as possible has to be understood in terms of cohesion—it should only do one thing. That doesn't mean it must necessarily have one method. In the previous example, it was by coincidence that both methods were doing disjointed things; hence it made sense to separate them into different classes.
to