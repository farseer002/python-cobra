#coding=utf-8
from scope import Scope

class ScopeStack(object):
	def __init__(self):
		self.list = [str(i) for i in range(10)]
		self.top = 0
		
	def push(self, scope):
		if self.top != 0:
			lastScope = self.list[self.top-1]
			if lastScope.indentLevel >= scope.indentLevel:
				raise ValueError('lastScope.indentLevel >= scope.indentLevel')
		self.list[self.top] = scope
		self.top += 1
		
	
	def popUntil(self, scope=Scope()):
		if self.top == 0:
			return
		
		if scope.indentLevel == -1:
			self.top = 0
			return
		
		while True:
			if self.top == 0:
				break
			lastScope = self.list[self.top-1]
			if lastScope.indentLevel < scope.indentLevel:
				break
			self.top -= 1
		
	def __str__(self):
		if self.top == 0:
			return '$'
		else:
			#字符串首未知的$表示module自身��ʾmodule����
			return '$.' + '.'.join(['%s' % scope.name for scope in self.list[0:self.top]])
		
if __name__ == '__main__':
	s = ScopeStack()
	print s