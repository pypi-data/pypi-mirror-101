#!/usr/bin/env python
"""
    uniquethreadlocal.py             Nat Goodspeed
    Copyright (C) 2021               Nat Goodspeed

NRG 2021-04-06
"""

from __future__ import print_function
from functools import partial
import threading

class UniqueThreadLocal(object):
    """
    To safely access boto3 proxy objects for Amazon SQS queues, we need those
    proxy objects to be thread-local: a different proxy object for each thread
    that wants to reference a given queue. But threading.local() is a global
    namespace: any attribute stored on threading.local() references the same
    object regardless of where the threading.local() reference itself is
    stored, be it a module attribute, a class attribute or an instance attribute.

    Naturally, every instance of SQueue must be able to reference a
    *different* underlying SQS queue.

    This class is a proxy for threading.local() that can be stored as an
    instance attribute of a class. Every access to an instance attribute on
    PerInstanceThreadLocal turns into an access to the corresponding attribute
    on threading.local() for an attribute made unique by suffixing with
    id(self). We could store the id of this PerInstanceThreadLocal's parent
    object, but why bother? All that matters is that every instance of
    PerInstanceThreadLocal references a distinct set of thread-local objects.
    """
    # Since every reference to threading.local() is to the same object, store
    # it as a class attribute rather than as an instance attribute.
    _local = threading.local()

    def __getattr__(self, attr):
        return getattr(self._local, self._name(self, attr))

    def __setattr__(self, attr, value):
        setattr(self._local, self._name(self, attr), value)

    @staticmethod
    def _name(obj, attr):
        return attr + str(id(obj))

    # make a unique exception that we know for sure will never be raised
    class NeverRaised(Exception):
        pass

    def property_for(self, parent, attr, factory=None):
        """
        Usage:

        class SomeClass(object):
            def __init__(self):
                self.local = UniqueThreadLocal()
                # makes SomeClass.counter both instance-local and thread-local
                self.local.property_for(self, 'counter', int)
        """
        # If caller omits 'factory', it means each thread is responsible for
        # setting attr before referencing it -- so don't catch AttributeError.
        catch = self.NeverRaised if factory is None else AttributeError
        def getter(parent):
            # The essential characteristic of Python threading.local() access
            # is that, when a new thread attempts to access a given attribute,
            # it's not (yet) there -- so the getter must find-or-create it.
            # Setting a property on the parent's class in __init__() means we
            # can't bind self -- because the second __init__() call would
            # replace that property with one that binds the second instance!
            # So replicate the logic in __getattr__(), using the parent for
            # the unique id instead of self.
            try:
                return getattr(self._local, self._name(parent, attr))
            except catch:
                return factory()
        def setter(parent, value):
            # But setting a property should be straightforward.
            setattr(self._local, self._name(parent, attr), value)
        # property is set on the *class*, not the instance
        setattr(parent.__class__, attr, property(getter, setter))
