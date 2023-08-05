What's New in Py-PAL 1.0.0
==========================

- More thorough testing from different combinations of requirements and Python versions.
- Bug fixes

What's New in Py-PAL 0.2.1
==========================
Refactoring
-----------

The `estimator` module was refactored which introduces a slight change to the API.
Classes inheriting from `Estimator` now only specify how to transform the collected data with respect to the arguments
of the function.

Instead of `ComplexityEstimator` you should use the `AllArgumentEstimator` class. Additionally there is the `SeparateArgumentEstimator` which is experimental.



What's New in Py-PAL 0.1.6
==========================

More accurate Data Collection
-----------------------------

The `Tracer` is enhanced by measuring builtin function calls with `AdvancedOpcodeMetric`.

Opcodes resembling a function call .e.g `FUNCTION_CALL` are filtered for built in function calls.
If the called function is found in the complexity mapping a synthetic Opcode weight gets assigned.
A builtin function call is evaluated using its argument and a pre-defined runtime complexity e.g. O(n log n) for
`sort()`.

- The feature is enabled by default
- The calculation produces a performance overhead and can be disabled by providing a `OpcodeMetric` instance to the `Tracer`
- The `AdvancedOpcodeMetric` instance assigned to the `Tracer` provides statistics about how many builtin function calls were observed and how many were found in the complexity map

Bugfixes
--------

- Cleaning data after normalization introduced wrong data points