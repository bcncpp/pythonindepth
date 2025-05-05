from typing import Final

DEFAULT_TIMEOUT: Final[float]

def function(**kwargs):
    print(kwargs)

function(key="value")
## bad code
def function(**kwargs): # wrong
    timeout = kwargs.get("timeout", DEFAULT_TIMEOUT)
    print(timeout)

## better
def function(timeout, **kwargs): 
    print(timeout)
