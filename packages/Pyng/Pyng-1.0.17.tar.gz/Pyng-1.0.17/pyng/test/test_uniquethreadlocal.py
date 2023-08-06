#!/usr/bin/env python
"""
    test_uniquethreadlocal.py        Nat Goodspeed
    Copyright (C) 2021               Nat Goodspeed

NRG 2021-04-06
"""

from __future__ import print_function

from pyng.threads.uniquethreadlocal import UniqueThreadLocal
import threading

class MyClass(object):
    def __init__(self, name):
        self.name = name
        self.local = UniqueThreadLocal()
        self.local.property_for(self, 'counter', int)
        self.local.property_for(self, 'queue')
        self.local.property_for(self, 'collect', list)

    def __str__(self):
        return self.name

class MyQueue(MyClass):
    def __init__(self, name):
        super(MyQueue, self).__init__(name)
        self.queue = []

def printattr(obj, attr):
    try:
        print('{}: {}.{} = {!r}'
              .format(threading.current_thread().name, obj, attr, getattr(obj, attr)))
    except AttributeError:
        print('{}: {}.{} not set'.format(threading.current_thread().name, obj, attr))

if __name__ == '__main__':
    obj0 = MyClass('obj0')
    obj1 = MyClass('obj1')
    q0 = MyQueue('q0')
    printattr(obj0, 'counter')
    obj0.counter += 1
    printattr(obj0, 'counter')
    obj1.counter = 'obj1.counter'
    printattr(obj1, 'counter')
    th = threading.Thread(target=printattr, args=(obj0, 'counter'))
    th.start()
    th.join()
    th = threading.Thread(target=printattr, args=(obj0, 'queue'))
    th.start()
    th.join()
    # implicitly create a list attribute
    collector = obj0.collect
    # modify the list without explicitly assigning
    collector.append('a')
    # verify that the object-local attribute shows that modification
    assert len(obj0.collect) == 1
    # but no other object's does
    assert not len(obj1.collect)
