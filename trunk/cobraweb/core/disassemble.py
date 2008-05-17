#coding=utf-8
if __name__ == '__main__':
    import sys
    sys.path.append('..')
    
import re
import sdis
from scopestack import ScopeStack
from scope import Scope
import sys
import StringIO
from bytecodes import Bytecodes

class Disassemble(object):
    def __init__(self):
        self.indentTag = None
        self.pattern = re.compile(r"""\s+(?P<name>[_a-zA-Z0-9]+)\s*(\(|:)""")
        self.scopeStack = ScopeStack()
        self.preScope = Scope()
        self.bytecodes = Bytecodes()
    #
    #处理缩进的方法
    #
    def getIndent(self, line):
        for index, char in enumerate(line):
            if char == ' ' or char == '\t':
                continue
            return line[:index]
        return line
        
    def isIndented(self, line):
        return line[0] == ' ' or line[0] == '\t'

    def getIndentTag(self, source):
        for lineNum, line in source.items():
            if not self.indentTag and self.isIndented(line):
                self.indentTag = self.getIndent(line)
                return
            
    def getIndentLevel(self, line):
        if not self.indentTag:
            return 0
        indent = self.getIndent(line)
        return indent.count(self.indentTag)
    
    #
    #处理scope name的方法
    #
    def getScopeName(self, line):
        #必须处理'def   f  (  a  ):  '这样的定义方式，所以最好的方案是使用re
        matchObj = self.pattern.search(line)
        if not matchObj:
            return None
        return matchObj.group('name')
    
    def getScope(self, line):
        scope = Scope()
        scope.name = self.getScopeName(line)
        scope.indentLevel = self.getIndentLevel(line)
        return scope
    
    def containScopeTag(self, line):
        stripedLine = line.strip()
        return stripedLine.startswith('def') or stripedLine.startswith('class')

    def enterNewScope(self, curScope):
        if curScope.indentLevel > self.preScope.indentLevel:
            return True
        else:
            return False

    def exitLastScope(self, curScope):
        if curScope.indentLevel < self.preScope.indentLevel:
            return True
        else:
            return False
    
    #
    #解析源文件的方法
    #
    def dis(self, scopeName=None):
        oldStdout = sys.stdout
        output = StringIO.StringIO()
        sys.stdout = output
        sdis.dis(scopeName)
        sys.stdout = oldStdout
        content = output.getvalue()
        output.close()
        if scopeName:
            return content.split('\n')[1:]
        else:
            return content.split('\n')[:]
    
    def parseDis(self, bytecodes):
        for bytecode in bytecodes:
            if not bytecode:
                continue
            matchObj = self.bytecodePattern.search(bytecode)
            if not matchObj:
                print 'can not parse'
            print'%s\t%s\t%s\t\t%s\t%s' % (matchObj.group('lineNum'), matchObj.group('opOffset'), matchObj.group('opCode'), matchObj.group('opArg'), matchObj.group('const'))
            
        
    def readPyFile(self, fileName):
        lines = open(fileName).readlines()
        #在.py文件中，第一行的行号应该为1，而不是0，所以这里需要插入一个占位的值
        lines.insert(0, '*')
        pySource = dict(enumerate(lines))
        return pySource
    
    def getDesassembledSource(self, source):
        result = []
        for lineNum, line in source.items():
            if not line.strip():
                result.append('')
                continue
            
            if lineNum == 0:
                continue
            
            indentLevel = self.getIndentLevel(line)
            if not self.indentTag:
                preSpace = '##'
            else:
                preSpace = self.indentTag * indentLevel + '##'
            
            result.append(line.rstrip())
            bytecodes4line = self.bytecodes.getBytecodes4Line(lineNum)
            for bytecode in bytecodes4line:
                result.append(preSpace + bytecode.__str__())
        return '\r\n'.join(result)
                
    def recognizeScope(self, source):
        self.getIndentTag(source)
        for lineNum, line in source.items():
            if self.containScopeTag(line):
                curScope = self.getScope(line)
                self.scopeStack.popUntil(curScope)
                self.scopeStack.push(curScope)
                scopeName = '%s' % self.scopeStack
                #scopeName形式为$.A.func
                #而dis工具只能解析形式为A.func的字符串
                self.bytecodes.parseDisResult(scopeName, self.dis(scopeName[2:]))
                source[lineNum] = line.rstrip() + (" #%s" % scopeName)
        #处理module本身的字节码指令序列
        #$是module自身的scopeName
        self.bytecodes.parseDisResult('$', self.dis())
            
    def parsePyFile(self, fileName):
        pySource = self.readPyFile(fileName)
        sdis.read(fileName)
        self.recognizeScope(pySource)
        return self.getDesassembledSource(pySource)
        
if __name__ == '__main__':
    disassemble = Disassemble()
    print disassemble.parsePyFile('demo.py')
