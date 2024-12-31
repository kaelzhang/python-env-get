import os
from typing import (
    Any, Callable, List, Optional, Union,
    Protocol, cast
)


Converter = Callable[[Any, str, bool], Any]
Converters = Optional[Union[Converter, List[Converter]]]

class EnvFunction(Protocol):
    def __call__(
        self,
        key: str,
        converter: Converters = None,
        defaults: Any = None
    ) -> Any:
        ...

    boolean: Converter
    integer: Converter
    required: Converter


def make_array(obj: Union[Converter, List[Converter]]) -> List[Converter]:
    """
    Ensure the converter is a list.

    Args:
        obj: A single converter or a list of converters.

    Returns:
        A list of converters.
    """
    if isinstance(obj, list):
        return obj
    return [obj]


def _env(
    key: str,
    converter: Converters = None,
    defaults: Any = None
) -> Any:
    """
    Retrieve and convert an environment variable.

    Args:
        key: The environment variable key.
        converter: A converter function or a list of converter functions.
        defaults: The default value if the environment variable is not found.

    Returns:
        The converted environment variable value.
    """
    env_vars = os.environ
    is_default = key not in env_vars
    value = defaults if is_default else env_vars[key]

    if converter is None:
        return value

    converters = make_array(converter)

    for conv in converters:
        value = conv(value, key, is_default)

    return value


def boolean_converter(v: Any, key: str, is_default: bool) -> bool:
    """
    Convert a value to boolean.

    Args:
        v: The value to convert.
        key: The environment variable key.
        is_default: Indicates if the default value is used.

    Returns:
        The boolean representation of the value.
    """
    return v in ('True', 'true', '1', 'Y', 'y', 'yes', True)


def integer_converter(v: Any, key: str, is_default: bool) -> int:
    """
    Convert a value to integer.

    Args:
        v: The value to convert.
        key: The environment variable key.
        is_default: Indicates if the default value is used.

    Returns:
        The integer representation of the value, or 0 if conversion fails.
    """
    try:
        return int(v)
    except (ValueError, TypeError):
        return 0


class EnvRequiredError(Exception):
    """Exception raised when a required environment variable is missing."""
    def __init__(self, message: str, code: str = 'ENV_REQUIRED'):
        super().__init__(message)
        self.code = code


def required_converter(v: Any, key: str, is_default: bool) -> Any:
    """
    Ensure that the environment variable is set.

    Args:
        v: The value to check.
        key: The environment variable key.
        is_default: Indicates if the default value is used.

    Returns:
        The value if it exists.

    Raises:
        EnvRequiredError: If the environment variable is required but not set.
    """
    if is_default:
        raise EnvRequiredError(f'env "{key}" is required')
    return v


env = cast(EnvFunction, _env)

# Attach converters to env function
env.boolean = boolean_converter
env.integer = integer_converter
env.required = required_converter
