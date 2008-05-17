#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from core.disassemble import Disassemble
from socket import *
from django.template.loader import get_template
from django.template import Context
import sys
import time
import opcode
from code2description import *

result = None

class StackItem(object):
	def __init__(self, value=None, is_top=False):
		self.value = value
		self.is_top = is_top

def gbk(info):
	return info.decode('utf-8').encode('gbk')

def utf8(info):
	return info.decode('gbk').encode('utf-8')

def index(request):
	return render_to_response("index.html")
	
def get(request):
	path = request.GET['path']
	dis = Disassemble()
	dised_code = dis.parsePyFile(path)
	vm_running_state = render_vm_running_state(send_command_to_cobra_server(path, 6061))
		
	#暂停server vm，获取vm状态
	pause_server_vm()
	vm_state = send_command_to_cobra_server('get_state')
	consts = render_consts(send_command_to_cobra_server('get_consts'))
	
	stack_info = get_stack()
	bytecode_info = get_bytecode()
	bytecode_path_info = get_bytecode_path()
	names = get_names()
	
	locals = get_locals()
	globals = get_globals()

	template = '''
	<vm>%s</vm>
	<code>%s</code>
	<consts>%s</consts>
	<names>%s</names>
	<locals>%s</locals>
	<globals>%s</globals>
	<stack>%s</stack>
	<bytecode>%s</bytecode>
	<bytecodepath>%s</bytecodepath>
	<is_vm_finished>no</is_vm_finished>
	'''
	return HttpResponse(template % (utf8(vm_running_state), dised_code, consts, names, locals, globals, stack_info, bytecode_info, bytecode_path_info))

def excute(request):
	pause_server_vm()
	vm_server_response = send_command_to_cobra_server('excute');
	resume_server_vm()
	
	is_server_vm_finished = get_is_server_vm_finished()		
	
	template = '''<vm_server_response>%s</vm_server_response>
				<is_vm_finished>%s</is_vm_finished>'''
	return HttpResponse(template % (vm_server_response, is_server_vm_finished))

def restore_vm(request):
	pause_server_vm()
	excute_info = send_command_to_cobra_server('excute');
	resume_server_vm()
	return HttpResponse("Python虚拟机已成功复位");

def exit(request):
	exit_info = send_command_to_cobra_server('exit', 6061);
	return HttpResponse(utf8(exit_info))

def next_step(request):
	pause_server_vm()
	send_command_to_cobra_server('next_step')
	resume_server_vm()
	
	time.sleep(1);
	
	pause_server_vm()
	stack_info = get_stack();
	bytecode_info = get_bytecode()
	bytecode_path_info = get_bytecode_path()
	
	locals = get_locals()
	globals = get_globals()
	is_server_vm_finished = get_is_server_vm_finished()		
	
	template = '''<locals>%s</locals>
				<globals>%s</globals>
				<stack>%s</stack>
				<bytecode>%s</bytecode>
				<bytecodepath>%s</bytecodepath>
				<is_vm_finished>%s</is_vm_finished>'''
	return HttpResponse(template % (locals, globals, stack_info, bytecode_info, bytecode_path_info, is_server_vm_finished))

#以下代码用于暂停和恢复服务器端的Python虚拟机
def pause_server_vm():
	send_command_to_cobra_server('pause_vm')
	
def resume_server_vm():
	send_command_to_cobra_server('resume_vm')
	
#以下代码可视化运行时栈
def render_stack(items):
	try:
		t = get_template('stack.html')
		return t.render(Context({'items':items}))
	except error:
		print sys.exc_info()[0]
		print sys.exc_info()[1]
		
def get_stack():
	try:
		stack_info = send_command_to_cobra_server('get_stack').strip();
		infos = stack_info.split()
		stack_size = int(infos[0])
		stack_element_count = int(infos[1])
		items = []
		for i in range(stack_size - stack_element_count):
			items.append(StackItem())
		
		if len(infos) > 2:
			stack_content = infos[2]
	
			for index, value in enumerate(stack_content.split('*')[:-1]):
				if index == 0:
					items.append(StackItem(value, True))
				else:
					items.append(StackItem(value))
	except Exception:
		print sys.exc_info()[0]
		print sys.exc_info()[1]
		
	return render_stack(items)

#以下代码可视化字节码指令
def get_bytecode():
	try:
		bytecode_info = send_command_to_cobra_server('get_bytecode').strip();
		code, arg = bytecode_info.split(' ')
		code = int(code)
		opname = opcode.opname[code]
		description = code2description[opname]
		
		t = get_template('bytecode.html')
		if code < opcode.HAVE_ARGUMENT:
			return t.render(Context({'code':opname, 'description':description}))
		else:
			return t.render(Context({'code':opname+' '+arg, 'description':description}))
	except Exception:
		print sys.exc_info()[0]
		print sys.exc_info()[1]

#以下代码获得bytecode的path
def get_bytecode_path():
	try:
		path_info = send_command_to_cobra_server('get_path').strip();
		return path_info
	except Exception:
		print sys.exc_info()[0]
		print sys.exc_info()[1]

#以下代码可视化consts列表
def render_consts(consts):
	try:
		consts = parse_list(consts)
		t = get_template('consts.html')
		return t.render(Context({'const_count':len(consts), 'consts':consts}))
	except error:
		print sys.exc_info()[3]
		
def render_vm_running_state(vm_running_state):
	try:
		t = get_template('string.html')
		return t.render(Context({'value' : vm_running_state}))
	except Exception, e:
		print sys.exc_info[3]
	
def parse_list(str_list):
	result = []
	in_obj = False
	pos = 0
	for index, char in enumerate(str_list):
		if char == ',':
			if not in_obj:
				result.append(str_list[pos:index].strip(' ,()').replace("<", "&lt;").replace(">", "&gt;"))
				pos = index
			else:
				continue
		elif char == '<':
			in_obj = True
		elif char == '>':
			in_obj = False
	last_item = str_list[pos:].strip(' ,()')
	if last_item:
		result.append(last_item.replace("<", "&lt;").replace(">", "&gt;"))
	return result

#以下代码可视化names列表
def get_names():
	try:
		names = parse_list(send_command_to_cobra_server('get_names'))
		t = get_template('list.html')
		return t.render(Context({'item_count':len(names), 'items':names}))
	except error:
		print sys.exc_info()[3]
			
#ￒￔￏￂﾴ￺ￂ￫ﾻ￱ﾵￃserver vmￊￇﾷ￱ￕ�ￒﾪﾳ￉ﾹﾦﾽ￡ￊ￸
def get_is_server_vm_finished():
	return send_command_to_cobra_server("get_is_vm_finished");
	
def send_command_to_cobra_server(command, port=6060):
	response = '服务器关闭或异常'
	try:
		client = socket(AF_INET, SOCK_STREAM)
		client.connect(('127.0.0.1', port))
		client.send(command.strip())
		response = client.recv(1024)
		client.close()
	except error:
		print sys.exc_info()[0]
		print sys.exc_info()[1]
	return response

#以下代码可视化名字空间
def rebuild_variable(str):
	command = "result = %s" % str.replace('<', '"&lt;').replace('>', '&gt;"')
	co = compile(command, "rebuild_variable.py", "exec")
	eval(co, globals())
	return result

def get_locals():
	try:
		locals = rebuild_variable(send_command_to_cobra_server('get_locals'))
		t = get_template('dict.html')
		return t.render(Context({'item_count':len(locals), 'dict':locals}))
	except error:
		print sys.exc_info()[3]
		
def get_globals():
	try:
		globals = rebuild_variable(send_command_to_cobra_server('get_globals'))
		t = get_template('dict.html')
		return t.render(Context({'item_count':len(globals), 'dict':globals}))
	except error:
		print sys.exc_info()[3]

