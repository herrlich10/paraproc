#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
import numpy as np
import paraproc

if __name__ == '__main__':
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