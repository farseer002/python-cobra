import dis as pydis
import types

code = None
def read(filename):
	f = open(filename)
	content = f.read()
	global code
	code = compile(content, filename, 'exec')
	f.close()

def find_code(code, name):
	for item in code.co_consts:
		if isinstance(item, types.CodeType):
			if item.co_name == name:
				return item
	return None
	
def dis(code_name=None):
	if code_name is None:
		co = code
		pydis.dis(co)
		return
	names = code_name.split(".")
	co = code
	for name in names:
		co = find_code(co, name)
		if not co:
			print '%s is not a valid name' % code_name
	if co:
		print ("  byte code for %s  " % code_name).center(60, '*')
		pydis.dis(co)