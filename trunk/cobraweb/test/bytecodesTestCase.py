import unittest
from core.bytecodes import Bytecodes
from core.bytecodes import Bytecode
from core.bytecodes import BytecodeParser

class BytecodesTestCase(unittest.TestCase):
    def setUp(self):
        self.bytecodes = Bytecodes()
        self.bytecodeParser = BytecodeParser()
        pass
    
    def tearDown(self):
        pass
    
    def testGetBytecode(self):
        line = '  7           0 LOAD_CONST               0 (None)'
        expect = Bytecode('7', '0', 'LOAD_CONST', '0', '(None)')
        self.assertBytecodeEqual(expect, self.bytecodeParser.parse('$', line))
        
        line = '22 LOAD_CONST3               0 (None)'
        expect = Bytecode('', '22', 'LOAD_CONST3', '0', '(None)')
        self.assertBytecodeEqual(expect, self.bytecodeParser.parse('$', line))
        
        line = '22 RETURN_VALUE               0'
        expect = Bytecode('', '22', 'RETURN_VALUE', '0', '')
        self.assertBytecodeEqual(expect, self.bytecodeParser.parse('$', line))
        
        line = '22 RETURN_VALUE'
        expect = Bytecode('', '22', 'RETURN_VALUE', '', '')
        self.assertBytecodeEqual(expect, self.bytecodeParser.parse('$', line))
        
    def assertBytecodeEqual(self, this, that):
        self.assertEqual(this.lineNum, that.lineNum)
        self.assertEqual(this.opOffset, that.opOffset)
        self.assertEqual(this.opCode, that.opCode)
        self.assertEqual(this.opArg, that.opArg)
        self.assertEqual(this.const, that.const)        
        
def suite():
    suite = unittest.makeSuite(BytecodesTestCase, 'test')
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')