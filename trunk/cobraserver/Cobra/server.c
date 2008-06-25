#include "Python.h"
#include "cobra.h"

SOCKET pythonServer;
SOCKET pythonClient;
SOCKET vmServer;
SOCKET vmClient;
char recvBuf[1024];
int vmListened = 0;
int pythonListened = 0;
//int should_pause = 1;

static char scriptFile[1024];


void CleanupWinsock(void)
{
	closesocket(pythonServer);
	closesocket(vmServer);
	printf("close server listened in port 6061\n");
	printf("close server listened in port 6060\n");
	if (WSACleanup() == SOCKET_ERROR)
	{
		printf("WSACleanup failed with error %d\n", WSAGetLastError());
	}
}

int InitWinsock(void)
{
	WSADATA WSAData;
	int ret;
	ret = WSAStartup(MAKEWORD(2,2), &WSAData);
	switch (ret) {
	case 0:	/* No error */
		return 1; /* Success */
	case WSASYSNOTREADY:
		printf("WSAStartup failed: network not ready\n");
		break;
	case WSAVERNOTSUPPORTED:
	case WSAEINVAL:
		printf("WSAStartup failed: requested version not supported\n");
		break;
	default:
		printf("WSAStartup failed: error code %d\n", ret);
		break;
	}

	return 0; /* Failure */
}


void TrimEnd(char* recvBuf, int end)
{
	while(recvBuf[end] == '\r' || recvBuf[end] == '\n')
	{
		recvBuf[end] = '\0';
		--end;
	}
}

char* ReceiveCommand(SOCKET* client)
{
	int ret;

	ret = recv(*client, recvBuf, 1024, 0);
	if (ret > 0)
	{
		recvBuf[ret] = '\0';
		TrimEnd(recvBuf, ret-1);
		printf("receive command content : <%s>\n", recvBuf);
		return recvBuf;
	}
	else if (ret == 0)
	{
		printf("command connection closed\n");
	}
	else
	{
		printf("recv failed: %d\n", WSAGetLastError());
	}
	return NULL;
}

char* ReceivePythonCommand()
{
	return ReceiveCommand(&pythonClient);
}


char* ReceiveVmCommand()
{
	return ReceiveCommand(&vmClient);
}


void Listen(SOCKET* server, int port)
{
	SOCKADDR_IN serverAddr;
	//	SOCKADDR_IN clientAddr;
	//	int clientAddrLength = sizeof(clientAddr);
	int ret;

	*server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(port);    
	serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);

	ret = bind(*server, (SOCKADDR *)&serverAddr, sizeof(serverAddr));
	if(ret == SOCKET_ERROR)
	{
		printf("bind fail : %d\n", WSAGetLastError());
	}
	ret = listen(*server, 10);
	if(ret == SOCKET_ERROR)
	{
		printf("listen fail : %d\n", WSAGetLastError());
	}
	printf("listen in port : %d...\n", port);
}

void Accept(SOCKET* server, SOCKET* client)
{
	SOCKADDR_IN clientAddr;
	int clientAddrLength = sizeof(clientAddr);
	printf("\nbegin accepting...\n");
	*client = accept(*server, (SOCKADDR*)&clientAddr, &clientAddrLength);
	getsockname(*client, (SOCKADDR*)&clientAddr, &clientAddrLength);
	printf("accept %s:%d\n", inet_ntoa(clientAddr.sin_addr), clientAddr.sin_port);
	if(*client == INVALID_SOCKET)
	{
		printf("accept fail : %d\n", WSAGetLastError());
	}
}

void Send(SOCKET* client, char* data)
{
	int leftLength = strlen(data);
	int index = 0;
	int ret;
	while(leftLength > 0)
	{
		ret = send(*client, &data[index], leftLength, 0);
		if(ret == SOCKET_ERROR)
		{
			printf("send fail : %d\n", WSAGetLastError());
		}
		leftLength -= ret;
		index += ret;
	}
}


void PythonServerListen(int port)
{
	if(pythonListened == 0) {
		Listen(&pythonServer, port);
		pythonListened = 1;
	}
}

void AcceptPythonClient()
{
	printf("waiting python client...");
	Accept(&pythonServer, &pythonClient);
}

void SendPythonClient(char* data)
{
	Send(&pythonClient, data);
}

void VmServerListen(int port)
{
	if(vmListened == 0) {
		Listen(&vmServer, port);
		vmListened = 1;
	}
}

void AcceptVmClient()
{
	printf("waiting vm client...");
	Accept(&vmServer, &vmClient);
}

void SendVmClient(char* data)
{
	Send(&vmClient, data);
}

void ClosePythonClient()
{
	SOCKADDR_IN clientAddr;
	int clientAddrLength = sizeof(clientAddr);
	int ret;
	ret = getsockname(pythonClient, (SOCKADDR*)&clientAddr, &clientAddrLength);
	printf("close %s:%d\n\n", inet_ntoa(clientAddr.sin_addr), clientAddr.sin_port);
	closesocket(pythonClient);
}

void CloseVmClient()
{
	SOCKADDR_IN clientAddr;
	int clientAddrLength = sizeof(clientAddr);
	int ret;
	ret = getsockname(vmClient, (SOCKADDR*)&clientAddr, &clientAddrLength);
	printf("close %s:%d\n\n", inet_ntoa(clientAddr.sin_addr), clientAddr.sin_port);
	closesocket(vmClient);
}


/************************************************************************/
/* 内部数据维护，与网络无关                                             */
/************************************************************************/
void SetScriptName(char* fileName)
{
	memset(scriptFile, 0, sizeof(scriptFile));
	if(strlen(fileName) >= 1024)
	{
		printf("file name is too long!\n");
		return;
	}
	strcpy(scriptFile, fileName);
}

char* GetScriptName()
{
	return scriptFile;
}