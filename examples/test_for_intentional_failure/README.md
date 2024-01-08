# Intentional failure example
In this example, we use MoPyRegtest to define regression tests that are intended to fail. 

Basically, the test definition goes exactly like e.g. shown in the 
[example in the folder test_user_defined_metrics](/examples/test_user_defined_metrics/test_user_defined_metrics.py).
However, we now tell MoPyRegtest that the call to `compare_result` is supposed to raise an `AssertionError`. This is
done with `unittest.TestCase.assertRaises` like

```python
self.assertRaises(AssertionError, tester.compare_result,
                  reference_result=str(reference_folder / "SineNoisy_res.csv"),
                  validated_cols=["y"], tol=1e-5, fill_in_method="interpolate")
```

See [test_for_intentional_failure.py](/examples/test_for_intentional_failure/test_for_intentional_failure.py). 
Running this file like 

```bash
python3 test_for_intentional_failure.py
```

will tell us that the test has passed, despite the reference result and the actual simulation result differing 
in the default metric by more than the specified `tol=1e-5`.