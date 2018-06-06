.. image:: https://img.shields.io/pypi/v/paraproc.svg
   :target: https://pypi.python.org/pypi/paraproc

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/herrlich10/paraproc/blob/master/LICENSE.txt

Overview
========
Paraproc is a simple library that helps you easily parallelize your computation
(over independent chunks of data) across multiple processes in Python, especially 
when you want to mix callings to external command line programs and hand brew 
Python functions together in your data processing pipeline.

Under the hood, it combines subprocess and multiprocessing, and uses a process pool
to schedule the jobs. It also provides a numpy.ndarray interface to access 
shared-memory across multiple processes.

Paraproc supports both Python 2 and 3, with numpy as the only external dependency. 
It is contained in only one Python file, so it can be easily copied into your project. 
(The copyright and license notice must be retained.)

Code snippets that demonstrate the basic usage of the library can be found later
in this documentation, and in the demo_*.py files.

Bugs can be reported to https://github.com/herrlich10/paraproc. 
The code can also be found there.

Quick starts
============
Execute commands in parallel
----------------------------
You can run both Python codes and command line programs in parallel:

.. code:: python

    import os
    import paraproc
    def my_job():
        print(os.getpid())

    pc = paraproc.PooledCaller()
    for k in range(5):
        pc.check_call(my_job) 
    for k in range(5):
        pc.check_call('echo $$', shell=True) # For linux/mac
    pc.wait()

The ``pc.check_call()`` method will return immediatedly. The actual execution of 
the queued commands are delayed until you call ``pc.wait()``.

Use shared-memory
-----------------
You can load large data in shared-memory, and read or write them 
as a normal numpy array from multiple processes:

.. code:: python

    import numpy as np
    import paraproc
    def slow_operation(k, x):
        x.acquire()
        x[:100000,:] += 1 # Write access
        res = np.mean(x) # Read access
        x.release()
        print('#{0}: mean = {1}'.format(k, res))
    
    a = paraproc.SharedMemoryArray.from_array(np.random.rand(1000000,500)) # About 4 GB
    pc = paraproc.PooledCaller()
    for k in range(pc.pool_size):
        pc.check_call(slow_operation, k, a)
    pc.wait()

The data in ``a`` is shared in memory across all children processes and 
never copied even with write accesses.