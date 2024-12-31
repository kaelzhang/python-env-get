import pytest
from env_get import env, EnvRequiredError

# Define the test cases
CASES = [
    # BOOLEAN tests
    ("BOOLEAN_A not set, no default", 'BOOLEAN_A', env.boolean, None, False, {}),
    ("BOOLEAN_B set to 'true'", 'BOOLEAN_B', env.boolean, None, True, {'BOOLEAN_B': 'true'}),
    ("BOOLEAN_C set to '1'", 'BOOLEAN_C', env.boolean, None, True, {'BOOLEAN_C': '1'}),
    ("BOOLEAN_D set to 'N'", 'BOOLEAN_D', env.boolean, None, False, {'BOOLEAN_D': 'N'}),
    ("BOOLEAN_D set to 'N' with default=True", 'BOOLEAN_D', env.boolean, True, False, {'BOOLEAN_D': 'N'}),
    ("BOOLEAN_E not set with default=True", 'BOOLEAN_E', env.boolean, True, True, {}),

    # INTEGER tests
    ("INTEGER_A set to '1'", 'INTEGER_A', env.integer, None, 1, {'INTEGER_A': '1'}),
    ("INTEGER_B not set", 'INTEGER_B', env.integer, None, 0, {}),
    ("INTEGER_C not set", 'INTEGER_C', env.integer, None, 0, {}),
    ("INTEGER_C not set with default=1", 'INTEGER_C', env.integer, 1, 1, {}),
    ("INTEGER_D not set with default=1", 'INTEGER_D', env.integer, 1, 1, {}),

    # NORMAL string tests
    ("NORMAL_A set to 'a'", 'NORMAL_A', None, None, 'a', {'NORMAL_A': 'a'}),
    ("NORMAL_A set to 'a' with converter=None", 'NORMAL_A', None, None, 'a', {'NORMAL_A': 'a'}),
    ("NORMAL_B set to empty string", 'NORMAL_B', None, None, '', {'NORMAL_B': ''}),
    ("NORMAL_B set to empty string with converter=None", 'NORMAL_B', None, None, '', {'NORMAL_B': ''}),
    ("NORMAL_C not set with default='foo'", 'NORMAL_C', None, 'foo', 'foo', {}),
    ("NORMAL_C not set with converter=None and default='foo'", 'NORMAL_C', None, 'foo', 'foo', {}),

    # Converter as list
    ("BOOLEAN_B with list converter [env.boolean]", 'BOOLEAN_B', [env.boolean], None, True, {'BOOLEAN_B': 'true'}),
    ("INTEGER_A with list converter [env.integer]", 'INTEGER_A', [env.integer], None, 1, {'INTEGER_A': '1'}),
    ("EXISTS set to 'true' with [env.required, env.boolean]", 'EXISTS', [env.required, env.boolean], None, True, {'EXISTS': 'true'}),
]

@pytest.mark.parametrize("test_name, env_key, converter, default, expected_result, setup_env", CASES)
def test_env(monkeypatch, test_name, env_key, converter, default, expected_result, setup_env):
    """Parametrized test for the env function.

    Args:
        monkeypatch: Pytest fixture for modifying environment variables.
        test_name: Description of the test case.
        env_key: The environment variable key to retrieve.
        converter: The converter function or list of converters to apply.
        default: The default value if the environment variable is not set.
        expected_result: The expected result after conversion.
        setup_env: Dictionary of environment variables to set for this test case.
    """
    # Clear all relevant environment variables to ensure test isolation
    all_env_vars = [
        'BOOLEAN_A', 'BOOLEAN_B', 'BOOLEAN_C', 'BOOLEAN_D', 'BOOLEAN_E',
        'INTEGER_A', 'INTEGER_B', 'INTEGER_C', 'INTEGER_D',
        'NORMAL_A', 'NORMAL_B', 'NORMAL_C',
        'EXISTS', 'NOT_EXISTS'
    ]
    for var in all_env_vars:
        monkeypatch.delenv(var, raising=False)

    # Set the necessary environment variables for this test case
    for key, value in setup_env.items():
        monkeypatch.setenv(key, value)

    result = env(env_key, converter, default)

    # Assert that the result matches the expected value
    assert result == expected_result, f"Test '{test_name}' failed: expected {expected_result}, got {result}"

def test_env_required_exception(monkeypatch):
    """Test that EnvRequiredError is raised when a required environment variable is missing.

    Ensures that attempting to retrieve a required environment variable that is not set
    raises the appropriate `EnvRequiredError` with the correct error code and message.
    """
    # Ensure 'NOT_EXISTS' is not set
    monkeypatch.delenv('NOT_EXISTS', raising=False)

    # Attempt to retrieve 'NOT_EXISTS' with the required converter
    with pytest.raises(EnvRequiredError) as exc_info:
        env('NOT_EXISTS', env.required)

    # Assert that the exception has the correct error code
    assert exc_info.value.code == 'ENV_REQUIRED', "Exception code mismatch"

    # Optionally, check the exception message
    assert str(exc_info.value) == 'env "NOT_EXISTS" is required', "Exception message mismatch"
