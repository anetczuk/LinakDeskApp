# MIT License
#
# Copyright (c) 2017 Arkadiusz Netczuk <dev.arnet@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


import unittest

import logging

import linakdeskapp.logger as logger


_LOGGER = logging.getLogger(__name__)
consoleHandler = logger.createStdOutHandler()
_LOGGER.addHandler( consoleHandler )


'''
Observations:
    1. object generator lives within inner scope of 'with' statement
    2. returned object ('as') from generator lives outside of 'with' inner scope
    3. '__enter__' and '__exit__' are called on generator
'''


class Counter(object):

    def __init__(self):
        self.constructor = 0
        self.enter = 0
        self.execute = 0
        self.exit = 0
        self.destructor = 0


class ObjectA(object):

    counter = None

    def __init__(self):
        # _LOGGER.warn("__init__: %r %r", self, ObjectA.counter)
        ObjectA.counter.constructor += 1

    def __enter__(self):
        # _LOGGER.warn("__enter__: %r %r", self, ObjectA.counter)
        ObjectA.counter.enter += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # _LOGGER.warn("__exit__: %r %r", self, ObjectA.counter)
        ObjectA.counter.exit += 1

    def __del__(self):
        # _LOGGER.warn("__del__: %r %r", self, ObjectA.counter)
        ObjectA.counter.destructor += 1

    def execute(self):
        ObjectA.counter.execute += 1


class ObjectGenerator(object):

    counter = None

    def __init__(self):
        # _LOGGER.warn("__init__: %r %r", self, ObjectGenerator.counter)
        ObjectGenerator.counter.constructor += 1

    def __enter__(self):
        # _LOGGER.warn("__enter__: %r %r", self, ObjectGenerator.counter)
        ObjectGenerator.counter.enter += 1
        return ObjectA()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # _LOGGER.warn("__exit__: %r %r", self, ObjectGenerator.counter)
        ObjectGenerator.counter.exit += 1

    def __del__(self):
        # _LOGGER.warn("__del__: %r %r", self, ObjectGenerator.counter)
        ObjectGenerator.counter.destructor += 1

    def execute(self):
        ObjectGenerator.counter.execute += 1

    @staticmethod
    def insideFunction():
        # _LOGGER.warn("insideFunction before: %r", ObjectGenerator.counter)
        with ObjectGenerator() as obj:
            # _LOGGER.warn("obj: %r", obj)
            obj.execute()
        # _LOGGER.warn("insideFunction after: %r", ObjectGenerator.counter)


class SelfGenerator(object):

    counter = None

    def __init__(self):
        # _LOGGER.warn("__init__: %r %r", self, SelfGenerator.counter)
        SelfGenerator.counter.constructor += 1

    def __enter__(self):
        # _LOGGER.warn("__enter__: %r %r", self, SelfGenerator.counter)
        SelfGenerator.counter.enter += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # _LOGGER.warn("__exit__: %r %r", self, SelfGenerator.counter)
        SelfGenerator.counter.exit += 1

    def __del__(self):
        # _LOGGER.warn("__del__: %r %r", self, SelfGenerator.counter)
        SelfGenerator.counter.destructor += 1

    def execute(self):
        SelfGenerator.counter.execute += 1

    @staticmethod
    def insideFunction():
        # _LOGGER.warn("insideFunction before: %r", SelfGenerator.counter)
        with SelfGenerator() as obj:
            # _LOGGER.warn("obj: %r", obj)
            obj.execute()
        # _LOGGER.warn("insideFunction after: %r", SelfGenerator.counter)


class ObjectGeneratorTest(unittest.TestCase):

    def setUp(self):
        ObjectGenerator.counter = Counter()
        ObjectA.counter = Counter()
        # _LOGGER.warn("setUp")

    def tearDown(self):
        # _LOGGER.warn("tearDown")
        pass

    def test_byConstructor(self):
        with ObjectGenerator() as obj:
            obj.execute()

        genCounter = ObjectGenerator.counter
        self.assertEqual(genCounter.constructor, 1)
        self.assertEqual(genCounter.enter, 1)
        self.assertEqual(genCounter.execute, 0)
        self.assertEqual(genCounter.exit, 1)
        self.assertEqual(genCounter.destructor, 1)

        objCounter = ObjectA.counter
        self.assertEqual(objCounter.constructor, 1)
        self.assertEqual(objCounter.enter, 0)
        self.assertEqual(objCounter.execute, 1)
        self.assertEqual(objCounter.exit, 0)
        self.assertEqual(objCounter.destructor, 0)      ## object alive

    def test_insideFunction(self):
        ObjectGenerator.insideFunction()

        genCounter = ObjectGenerator.counter
        self.assertEqual(genCounter.constructor, 1)
        self.assertEqual(genCounter.enter, 1)
        self.assertEqual(genCounter.execute, 0)
        self.assertEqual(genCounter.exit, 1)
        self.assertEqual(genCounter.destructor, 1)

        objCounter = ObjectA.counter
        self.assertEqual(objCounter.constructor, 1)
        self.assertEqual(objCounter.enter, 0)
        self.assertEqual(objCounter.execute, 1)
        self.assertEqual(objCounter.exit, 0)
        self.assertEqual(objCounter.destructor, 1)      ## object destroyed


class SelfGeneratorTest(unittest.TestCase):

    def setUp(self):
        SelfGenerator.counter = Counter()
        ObjectA.counter = Counter()
        # _LOGGER.warn("setUp")

    def tearDown(self):
        # _LOGGER.warn("tearDown")
        pass

    def test_byConstructor(self):
        with SelfGenerator() as obj:
            obj.execute()

        genCounter = SelfGenerator.counter
        self.assertEqual(genCounter.constructor, 1)
        self.assertEqual(genCounter.enter, 1)
        self.assertEqual(genCounter.execute, 1)
        self.assertEqual(genCounter.exit, 1)
        self.assertEqual(genCounter.destructor, 0)      ## generator alive

    def test_insideFunction(self):
        SelfGenerator.insideFunction()

        genCounter = SelfGenerator.counter
        self.assertEqual(genCounter.constructor, 1)
        self.assertEqual(genCounter.enter, 1)
        self.assertEqual(genCounter.execute, 1)
        self.assertEqual(genCounter.exit, 1)
        self.assertEqual(genCounter.destructor, 1)      ## generator destroyed
