#ifndef Cobra_HEADER_H
#define Cobra_HEADER_H
#ifdef __cplusplus
extern "C" {
#endif

#include "Python.h"
#include "frameobject.h"

#ifndef _WINSOCK2API_
#include <winsock2.h>
#endif

void CleanupWinsock(void);
int InitWinsock(void);

void PythonServerListen(int port);
void AcceptPythonClient();
void SendPythonClient();

void VmServerListen(int port);
void AcceptVmClient();
void SendVmClient(char* data);

char* ReceivePythonCommand();
char* ReceiveVmCommand();
void ClosePythonClient();
void CloseVmClient();

void SetScriptName(char* name);
char* GetScriptName();

//÷¥––√¸¡Ó
char* GetConsts(PyFrameObject* frame);
char* GetNames(PyFrameObject* frame);
char* GetStack(PyFrameObject* frame, PyObject** stack_pointer);
char* GetByteCodePath(PyFrameObject* frame);
char* GetLocals(PyFrameObject* frame);
char* GetGlobals(PyFrameObject* frame);


#ifdef __cplusplus
}
#endif
#endif /* !Cobra_HEADER_H*/