/* Minimal main program -- everything is loaded from the library */

#include "Python.h"
#include "cobra.h"

#ifdef __FreeBSD__
#include <floatingpoint.h>
#endif

int
main(int argc, char **argv)
{
	/* 754 requires that FP exceptions run in "no stop" mode by default,
	 * and until C vendors implement C99's ways to control FP exceptions,
	 * Python requires non-stop mode.  Alas, some platforms enable FP
	 * exceptions by default.  Here we disable them.
	 */
#ifdef __FreeBSD__
	fp_except_t m;

	m = fpgetmask();
	fpsetmask(m & ~FP_X_OFL);
#endif
	//return Py_Main(argc, argv);
	char* command;
	char* newArgv[2];
	int ret;
	
	newArgv[0] = argv[0];
	InitWinsock();
//	Py_Main(argc, argv);
	PythonServerListen(6061);
	while(1)
	{
		char fileName[256];
		//接收客户端的连接
		AcceptPythonClient();
		//从客户端接收需要执行的py文件
		command = ReceivePythonCommand();
		
		if(strcmp(command, "exit") == 0)
		{
			SendPythonClient("Python虚拟机已停止");
			ReceivePythonCommand();
			ClosePythonClient();
			break;
		}
		
		SendPythonClient("Python虚拟机开始运行");
		//等待客户端的关闭信号，防止同时关闭TCP连接
		ReceivePythonCommand();
		//关闭和客户端的链接
		ClosePythonClient();
		memset(fileName, 0, 256);
		strcpy(fileName, command);
		newArgv[1] = fileName;
		printf("Python VM excutes file : %s\n", fileName);
		ret = Py_Main(2, newArgv);
	}
	CleanupWinsock();
	return ret;
}
