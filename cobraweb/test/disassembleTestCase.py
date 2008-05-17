import unittest
    
from core.disassemble import Disassemble
from core.scope import Scope

class DisassembleTestCase(unittest.TestCase):
    def setUp(self):
        self.disassemble = Disassemble()
    
    def tearDown(self):
        pass
    
    def testGetIndent(self):
        source = "\tpass"
        expect = '\t'
        self.assertEqual(expect, self.disassemble.getIndent(source))
        
        source = "   pass"
        expect = '   '
        self.assertEqual(expect, self.disassemble.getIndent(source))
        
        source = " \t pass"
        expect = ' \t '
        self.assertEqual(expect, self.disassemble.getIndent(source))
        
    def testGetIndentTag(self):
        sourceTemplate = "def f():\n%(indent)si = 0\n%(indent)sdef g():\n%(indent)s%(indent)spass"
        
        expect = '\t'
        source = sourceTemplate % {'indent':expect}
        source = dict(enumerate(source .split('\n')))
        self.disassemble.getIndentTag(source)
        self.assertEqual(expect, self.disassemble.indentTag)
        
        self.disassemble.indentTag = None
        expect = ' \t  '
        source = sourceTemplate % {'indent':expect}
        source = dict(enumerate(source .split('\n')))
        self.disassemble.getIndentTag(source)
        self.assertEqual(expect, self.disassemble.indentTag)
        
    def testGetIndentLevel(self):
        self.disassemble.indentTag = '\t'
        line = 'def f():'
        self.assertEqual(0, self.disassemble.getIndentLevel(line))
        line = '\tpass'
        self.assertEqual(1, self.disassemble.getIndentLevel(line))
        line = '\t\tpass'
        self.assertEqual(2, self.disassemble.getIndentLevel(line))
        
        self.disassemble.indentTag = ' \t '
        line = 'def f():'
        self.assertEqual(0, self.disassemble.getIndentLevel(line))
        line = ' \t pass'
        self.assertEqual(1, self.disassemble.getIndentLevel(line))
        line = ' \t  \t pass'
        self.assertEqual(2, self.disassemble.getIndentLevel(line))
        
    def testGetScope(self):
        expect = Scope()
        self.disassemble.indentTag = '\t  '
        
        line = '\t  def f():'
        expect.name = 'f'
        expect.indentLevel = 1
        self.assertEqual(True, self.disassemble.containScopeTag(line))
        actual = self.disassemble.getScope(line)
        self.assertEqual(expect.name, actual.name)
        self.assertEqual(expect.indentLevel, actual.indentLevel)
        
        line = '\t  class A  ( object ):'
        expect.name = 'A'
        expect.indentLevel = 1
        self.assertEqual(True, self.disassemble.containScopeTag(line))
        actual = self.disassemble.getScope(line)
        self.assertEqual(expect.name, actual.name)
        self.assertEqual(expect.indentLevel, actual.indentLevel)
        
    def testEnterAndExitScope(self):
        scope = Scope()
        self.disassemble.indentTag = '\t  '
        
        line = '\t  def f():'
        curScope = self.disassemble.getScope(line)
        self.assertEqual(False, self.disassemble.exitLastScope(curScope))
        self.assertEqual(True, self.disassemble.enterNewScope(curScope))
        
        self.disassemble.preScope = curScope
        line = 'class A_B  ():'
        curScope = self.disassemble.getScope(line)
        self.assertEqual(False, self.disassemble.enterNewScope(curScope))
        self.assertEqual(True, self.disassemble.exitLastScope(curScope))

        
def suite():
    suite = unittest.makeSuite(DisassembleTestCase, 'test')
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')