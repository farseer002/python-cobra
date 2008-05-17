#coding=utf-8
import re

class Bytecode(object):
    def __init__(self, lineNum='', opOffset='', opCode='', opArg='', const=''):
        #matchObj是正则表达式search的结果
        self.lineNum = lineNum
        self.opOffset = opOffset
        self.opCode = opCode
        self.opArg = opArg
        self.const = const
        #scopePos维护字节码指令的全局位置，由scope.opOffset组成
        self.scopePos = None
        
    def __str__(self):
        space = '\t'
        l = []
        if self.lineNum:
            l.append(self.lineNum)
        else:
            l.append(' ')
        l.append(space)
        l.append(self.opOffset)
        l.append(space)
        l.append(self.opCode)
        l.append(space)
        l.append(space)
        if self.opArg:
            l.append(self.opArg)
        else:
            l.append(' ')
        l.append(space)
        if self.const:
            l.append(self.const)
        else:
            l.append(' ')
        l.append('%s#%s' % (space, self.scopePos))
        return ''.join(l)

class BytecodeParser(object):
    def __init__(self):
        pass
    
    def findOpCodeIndex(self, items):
        for index, item in enumerate(items):
            if item[0].isalpha():
                return index
        return None
    
    def parse(self, scopeName, line):
        items = line.split()
        opCodeIndex = self.findOpCodeIndex(items)
        
        bytecode = Bytecode()
        bytecode.opCode = items[opCodeIndex]
        if opCodeIndex-1 >= 0:
            bytecode.opOffset = items[opCodeIndex-1]
        if opCodeIndex-2 >= 0:
            bytecode.lineNum = items[opCodeIndex-2]
            
        size = len(items)
        if opCodeIndex+1 < size:
            bytecode.opArg = items[opCodeIndex+1]
        if opCodeIndex+2 < size:
            #因为const中可能会有空格，所以切分的结果肯能会有错误
            #比如('hello world')，切分的结果const为('hello
            #所以这里需要重新获得const���»��const
            beg = line.index('(')
            end = line.rindex(')')+1
            bytecode.const = line[beg:end]
        bytecode.scopePos = '%s.%s' % (scopeName, bytecode.opOffset)
        return bytecode
               
class Bytecodes(object):
    def __init__(self):
        self.bytecodeParser = BytecodeParser()
        self.linenum2bytecode = {}
            
    def parseDisResult(self, scopeName, disResult):
        bytecodes = []
        for result in disResult:
            if not result:
                continue
            bytecodes.append(self.bytecodeParser.parse(scopeName, result))        
        self.fillLineNum(bytecodes)
        self.fillLinenum2Bytecode(bytecodes)

    def fillLineNum(self, bytecodes):
        preLineNum = 0
        for bytecode in bytecodes:
            if bytecode.lineNum:
                preLineNum = bytecode.lineNum
            else:
                bytecode.lineNum = preLineNum
                
    def fillLinenum2Bytecode(self, bytecodes):
        for bytecode in bytecodes:
            lineNum = int(bytecode.lineNum)
            if lineNum in self.linenum2bytecode:
                self.linenum2bytecode[lineNum].append(bytecode)
            else:
                self.linenum2bytecode[lineNum] = [bytecode,]
                
    #外部接口�ⲿ�ӿ�         
    def getBytecodes4Line(self, lineNum):
        return self.linenum2bytecode[lineNum]
    
    #for debug
    def printLinenum2Bytecode(self):
        for lineNum, bytecodes4line in self.linenum2bytecode.items():
            print lineNum, ' : '
            for bytecode in bytecodes4line:
                print bytecode
        