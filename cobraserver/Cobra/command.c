#include "Python.h"
#include "frameobject.h"
#include "code.h"
#include "cobra.h"

char buf[10240];



void ClearBuffer() {
	memset(buf, 0, 10240);
}

char* GetConsts(PyFrameObject* frame) {
	PyCodeObject* code = frame->f_code;
	PyObject* consts = code->co_consts;
	char* tmp = NULL;

	ClearBuffer();
	tmp = PyString_AsString(PyObject_Str(consts));
	memcpy(buf, tmp, 10240);
	return buf;
}

char* GetNames(PyFrameObject* frame) {
	PyCodeObject* code = frame->f_code;
	PyObject* names = code->co_names;
	char* tmp = NULL;

	ClearBuffer();
	tmp = PyString_AsString(PyObject_Str(names));
	memcpy(buf, tmp, 10240);
	return buf;
}

char* GetLocals(PyFrameObject* frame) {
	char* tmp = NULL;

	ClearBuffer();
	tmp = PyString_AsString(PyObject_Str(frame->f_locals));
	memcpy(buf, tmp, 10240);
	return buf;
}

char* GetGlobals(PyFrameObject* frame) {
	char* tmp = NULL;

	ClearBuffer();
	tmp = PyString_AsString(PyObject_Str(frame->f_globals));
	memcpy(buf, tmp, 10240);
	return buf;
}

char* GetStack(PyFrameObject* frame, PyObject** stack_pointer) {
	PyCodeObject* co = frame->f_code;
	char stackValue[1024];
	int i = 0;
	int count = 0;
	char* value;

#define STACK_LEVEL()	((int)(stack_pointer - frame->f_valuestack))

	memset(stackValue, 0, 1024);
	count = STACK_LEVEL();
	for( ; i < count; ++i) {
		PyObject* obj = stack_pointer[-(i+1)];
		value = PyString_AsString(PyObject_Str(obj));
		strcat(stackValue, value);
		strcat(stackValue, "*");
	}

	ClearBuffer();
	sprintf(buf, "%d\n%d\n%s", co->co_stacksize, STACK_LEVEL(), stackValue);
	return buf;
}

char* GetByteCodePath(PyFrameObject* frame) {
	//构造并初始化名字集合
	char tmp[100];
	char* names[100];
	int index = 0;
	int i = 0;
	int instruction_offset = frame->f_lasti;
	memset(tmp, 0, 100*sizeof(char));
	memset(names, 0, 100*sizeof(char*));

	while(frame != NULL) {
		PyCodeObject* co = frame->f_code;
		char* name = PyString_AsString(co->co_name);
		if(strcmp(name, "<module>") == 0) {
			name = "$";
		}
		names[index++] = name;
		frame = frame->f_back;
	}

	ClearBuffer();
	for( ; i < index; ++i) {
		strcat(buf, names[i]);
		strcat(buf, ".");
	}
	sprintf(tmp, "%d", instruction_offset);
	strcat(buf, tmp);
	return buf;
}