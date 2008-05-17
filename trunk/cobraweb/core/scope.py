#coding=utf-8

class Scope(object):
    def __init__(self, name=None, indentLevel=-1):
        self.name = name
        self.indentLevel = indentLevel
        
    def __str__(self):
        return '(scope <%s, %s>)' % (self.name, self.indentLevel)