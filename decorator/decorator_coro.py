import inspect
from functools import wraps
import time
import asyncio

def timing(callable):
    if inspect.iscoroutinefunction(callable):
        @wraps(callable)
        async def wrapped(*args, **kwargs):
            start = time.time()
            result = await callable(*args, **kwargs)
            latency = time.time() - start
            return {"latency": latency, "result": result}
        return wrapped
    else:
        @wraps(callable)
        def wrapped(*args, **kwargs):
            start = time.time()
            result = callable(*args, **kwargs)
            latency = time.time() - start
            return {"latency": latency, "result": result}
        return wrapped

@timing
def func2():
    time.sleep(0.1)
    return 42

@timing
async def coro2():
    await asyncio.sleep(0.1)
    return 42

if __name__ == "__main__":
    print(func2())  # Works as expected

    # Proper way to run the async function
    result = asyncio.run(coro2())
    print(result)

