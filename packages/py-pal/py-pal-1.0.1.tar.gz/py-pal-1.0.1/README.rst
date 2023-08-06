========
Overview
========

.. start-badges

|version| |wheel| |supported-versions| |supported-implementations|

.. |version| image:: https://img.shields.io/pypi/v/py-pal.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/py-pal

.. |wheel| image:: https://img.shields.io/pypi/wheel/py-pal.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/py-pal

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/py-pal.svg
    :alt: Supported versions
    :target: https://pypi.org/project/py-pal

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/py-pal.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/py-pal

.. end-badges

The *Python Performance Analysis Library* (*py-pal*) is a profiling tool for the Python programming language.
Further details can be found in the documentation at https://py-pal.readthedocs.io.


Installation
============

Requirements
------------
- An installation of the CPython implementation of the Python programming language of version greater or equal to 3.7
    - For instance: https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe
- A compiler for the C/C++ programming language:
    - On Microsoft Windows, we use the *Buildtools für Visual Studio 2019*:
        https://visualstudio.microsoft.com/de/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16
    - On Linux, any C compiler supported by Cython e.g. g++

Install py-pal via pip by running:
----------------------------------
This project requires CPython and a C compiler to run. Install CPython >= 3.7, then install py-pal by running:


    pip install py-pal
    
or

    python -m pip install py-pal

Development Environment
=======================

To set up an environment for developing the py-pal module, the requirements mentioned in the section *Installation*
must be met. Then

1. Clone this repository locally with git

2. Navigate to the cloned repository

3. Create a virtual environment

    python -m venv .venv
    
4. Activate the virtual environment

    On Microsoft Windows run: .venv\\Scripts\\activate.bat
    On Linux run: source venv/bin/activate

5. Install the dependencies for the development environment

    pip install -r dev-requirements.txt
    
    or

    python -m pip install -r dev-requirements

Building the *py-pal* module
----------------------------

    python setup.py develop

With this command, the C extensions are compiled using Cython. Also, it packages all necessary files together and
installs them in the current virtual environment.

Note, any change to a cython file (.pyx) requires recompilation, i.e. the above command must be executed again.

*Attention*, if it is not possible to install Cython by this command, the cython files (.pyx) are not taken into
account. This results in the circumstance that the corresponding C/C++ files are not generated and thus, the old C/C++
files get used to build the C extensions. Directly speaking, changes to the cython files will have no effect because
they are not processed!

Run all regular tests from the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    pytest tests
   
Run all Cython tests from the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    pytest tests_cython
    
Run all regular and Cython tests together from the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    pytest tests tests_cython
    
Command line usage of the py-pal module
=======================================

    python -m py_pal <target-module/file>

or

    py-pal <target-module/file>

There are multiple aliases to the same command: `py-pal`, `py_pal` and `pypal`
    
See the help message:

    py-pal -h

Programmatic usage of the py-pal module
=======================================

The *profile* decorator:

.. sourcecode:: python

    from py_pal.core import profile

    @profile
    def test():
        pass

By using the *profile* decorator, it is possible to annotate Python functions such that only the annotated Python
functions will be profiled. It acts similar to a whitelist filter.

Another possibility is to use the context manager protocol:

.. sourcecode:: python

    from py_pal.estimator import AllArgumentEstimator
    from py_pal.tracer import Tracer

    with Tracer() as t:
        pass

    estimator = AllArgumentEstimator(t)
    res = estimator.export()

    # Do something with the resulting DataFrame
    print(res)


The most verbose way to use the *py-pal* API:

.. sourcecode:: python

    from py_pal.estimator import AllArgumentEstimator
    from py_pal.tracer import Tracer


    t = Tracer()
    t.trace()

    # Your function
    pass

    t.stop()
    estimator = AllArgumentEstimator(t)
    res = estimator.export()

    # Do something with the resulting DataFrame
    print(res)

All examples instantiate a tracer object that is responsible for collecting the data. After execution, the collected
data is passed to the analysis module. Finally, an estimate of the asymptotic runtime of the functions contained in the
code is obtained.

Modes
-----
In the current version py-pal offers only the **profiling mode**. Although ``py_pal.datagen`` offers some functions for
generating inputs, py-pal must be combined with appropriate test cases to realize a **performance testing mode**. An
automatic detection and generation of appropriate test inputs does not exist at the moment.

Limitations
-----------
The profiling approach implemented by the py-pal modules does not distinguish between different threads executing a
Python function. Actually it is a major problem to profile a Python script which makes use of threads. The bytecode
counting strategy will increase all counters of Python functions on the current call stack no matter what threads is
executing it. Thus, the data points will not be accurate to what really happened during the profiled execution of the
script.

Licensing Notes
===============
This work integrates some code from the `big_O <https://github.com/pberkes/big_O>`_ project.
More specifically, most code in ``py_pal.complexity``, ``py_pal.datagen`` and
``py_pal.estimator.Estimator.infer_complexity`` is adapted from bigO.
