import unittest

from core.scopestack import ScopeStack
from core.scope import Scope

class ScopestackTestCase(unittest.TestCase):
    def setUp(self):
        self.stack = ScopeStack()
        pass
    
    def tearDown(self):
        pass
    
    def testNewStack(self):
        expect = '$'
        self.assertEqual(expect, '%s' % self.stack)
        
    def testPushAndPop(self):
        s = self.stack
        
        s.push(Scope('A', 0))
        s.push(Scope('__init__', 1))
        expect = '$.A.__init__'
        self.assertEqual(expect, '%s' % s)
        
        s.popUntil()
        s.push(Scope('f', 0))
        expect = '$.f'
        self.assertEqual(expect, '%s' % s)        
        
        s.push(Scope('g', 1))
        expect = '$.f.g'
        self.assertEqual(expect, '%s' % s)
        
        
def suite():
    suite = unittest.makeSuite(ScopestackTestCase, 'test')
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')