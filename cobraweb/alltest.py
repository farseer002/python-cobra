# -*- encoding:gbk -*-

import unittest
import sys

import test.scopestackTestCase
import test.disassembleTestCase
import test.bytecodesTestCase
    
testSuites = [
test.scopestackTestCase.suite, 
test.disassembleTestCase.suite, 
test.bytecodesTestCase.suite, 
]

for suite in testSuites:
    unittest.TextTestRunner(verbosity=2).run(suite())    