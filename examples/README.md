# Examples

For detailed documentation on all features, see [doc/usage.md](/doc/usage.md).

## Manual test definitions

| Example | Description |
|---------|-------------|
| [test_Modelica_Electrical_Analog_Examples](test_Modelica_Electrical_Analog_Examples/) | Regression tests with default and custom metrics |
| [test_user_defined_metrics](test_user_defined_metrics/) | User-defined comparison metrics |
| [test_for_intentional_failure](test_for_intentional_failure/) | Testing that a comparison *fails* as expected |

## Automatic test generation

| Example | Description |
|---------|-------------|
| [generate_tests/gentests_modelica_blocks_sources.py](generate_tests/gentests_modelica_blocks_sources.py) | Generate regression tests from a script |
| [generate_tests/gentests_simulation_check.py](generate_tests/gentests_simulation_check.py) | Generate simulation-only tests from a script |

See [generate_tests/README.md](generate_tests/README.md) for CLI and script usage.