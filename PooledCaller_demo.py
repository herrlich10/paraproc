#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
import os
import paraproc

if __name__ == '__main__':
    def my_job():
        print(os.getpid())

    pc = paraproc.PooledCaller()
    for k in range(5):
        pc.check_call(my_job)
    for k in range(5):
        pc.check_call('echo $$', shell=True) # For linux/mac
    pc.wait()