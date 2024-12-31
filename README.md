[![](https://github.com/kaelzhang/python-env-get/actions/workflows/python.yml/badge.svg)](https://github.com/kaelzhang/python-env-get/actions/workflows/python.yml)
[![](https://codecov.io/gh/kaelzhang/python-env-get/branch/master/graph/badge.svg)](https://codecov.io/gh/kaelzhang/python-env-get)
[![](https://img.shields.io/pypi/v/env-get.svg)](https://pypi.org/project/env-get/)
[![](https://img.shields.io/pypi/l/env-get.svg)](https://github.com/kaelzhang/python-env-get)

<!-- [![Conda version](https://img.shields.io/conda/vn/conda-forge/env-get)](https://anaconda.org/conda-forge/env-get) -->

# env-get

Manage and retrieve env variables in Python.

## Install

```sh
$ pip install env-get
```

## Usage

```py
from env_get import env, EnvRequiredError

port = env('SERVER_PORT', env.integer, 80)
```

## env(key, converter, defaults) -> Any

```py
def Converter(v: Any, key: str, is_default: bool) -> Any:
```

- **key** `str`: The environment variable key.
- **converter** `Optional[Converter | List[Converter]]` A converter function or a list of converter functions.
- **defaults** `Opitonal[Any]` The optional default value if the environment variable is not found.

Returns `Any` the retrieved env variable.

### Built-in Converter Functions

- **`env.boolean`**: Converts the value to a boolean. Treats `'true'`, `'1'`, `'Y'`, `'y'`, `'yes'`, and `True` as `True`.
- **`env.integer`**: Converts the value to an integer. Returns `0` if conversion fails.
- **`env.required`**: Ensures that the environment variable is set. Raises a `EnvRequiredError` if not.

## Examples

### Boolean Conversion

```py
debug_mode = env('DEBUG_MODE', env.boolean, False)
```

### Integer Conversion

```py
port = env('PORT', env.integer, 8080)
```

### Required Variable

```py
from env_get import env, EnvRequiredError

try:
    api_key = env('API_KEY', env.required)
except RangeError as e:
    print(e)  # Output: env "API_KEY" is required
```

### Handling Multiple Converters

You can apply multiple converters by passing a list of converter functions.

```py
value = env('SOME_VAR', [env.required, env.integer], 10)
```

## License

[MIT](LICENSE)
