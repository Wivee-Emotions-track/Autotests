import time
import wrapt

from log import logger


def repeat_until_true(steps: int = 5, delay: int = 1, error_msg: str = None):
    """
        Repeatedly calls a function until it returns a truthy value or the maximum number of attempts is reached.

        Args:
            steps (int): The number of times to attempt calling the function. Default is 5.
            delay (int): The delay (in seconds) between each attempt. Default is 1 second.
            error_msg (str, optional): The error message to be raised in case all attempts fail.

        Raises:
            TimeoutError: Raised if the function does not return a truthy value after the specified number of attempts.

        Returns:
            The result of the wrapped function if it returns a truthy value within the allowed attempts.
        """
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        for _ in range(steps):
            value = wrapped(*args, **kwargs)
            if value:
                return value
            time.sleep(delay)
        if error_msg:
            raise TimeoutError(error_msg)
        else:
            raise TimeoutError

    return wrapper

def retry_on_exception(steps: int = 3, delay: int = 1, exceptions=(Exception,)):
    """
        Retries a function call if it raises an exception from the specified exceptions.

        Args:
            steps (int): The number of times to retry the function. Default is 3.
            delay (int): The delay (in seconds) between each retry attempt. Default is 1 second.
            exceptions (tuple): A tuple of exception classes to catch and retry on. Default is (Exception,).

        Raises:
            Exception: Re-raises the caught exception after all retry attempts fail.

        Returns:
            The result of the wrapped function if it succeeds within the allowed retries.
        """
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        for attempt in range(steps):
            try:
                return wrapped(*args, **kwargs)  # Try to execute the function
            except exceptions as e:
                if attempt + 1 == steps:  # Last attempt, raise exception
                    raise
                print(f"Error: {type(e).__name__} — attempt "
                      f"{attempt + 1}/{steps}, retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
    return wrapper

def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Method {func.__name__}: {execution_time:.2f} seconds")
        return result
    return wrapper