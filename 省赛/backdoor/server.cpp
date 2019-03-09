#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <unistd.h>

#include <iostream>
#include <fstream>
#include <string>
#include <ctime>
#include <string.h>
using namespace std;
//服务器监听的端口
uint16_t server_port = htons(3000);
in_addr  server_bind_addr = { htonl(INADDR_ANY) };
/*===============================================================================
 *接收客户端发送的数据，并保存到当前文件夹下，以发送者IP为文件名的文件中
 * ==============================================================================*/
void data_process(int client_fd, sockaddr_in client_addr)
{
	char *buffer = new char[300];
	char *sender = new char[30];
	recv(client_fd, buffer, 280, 0);

	inet_ntop(AF_INET, &client_addr.sin_addr.s_addr, sender, 25);
	fstream file;
	file.open(sender, fstream::out | fstream::app);
	file << buffer << endl;

	file.close();
}


int main()
{
	
	int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
	
	sockaddr_in dst_addr = {};
	dst_addr.sin_family = AF_INET;
	dst_addr.sin_port = server_port;
	dst_addr.sin_addr = server_bind_addr;

	if(bind(socket_fd, (sockaddr *)&dst_addr, sizeof(dst_addr)))
	{
		cout << "bind error" << endl;
		close(socket_fd);
		return 0;		
	}

	if(listen(socket_fd, 1024) == -1)
	{
		cout << "listen error" << endl;
		close(socket_fd);
		return 0;
	}

	cout << "start server listenning on port 3000" << endl;

	while(true)
	{
		sockaddr_in client_addr = {};
		socklen_t length = sizeof(sockaddr_in);

		int client_fd = accept(socket_fd, (sockaddr *)&client_addr, &length);
		if(client_fd != -1)
		{
			cout << "received request" << endl;
			if(!fork())
			{
				data_process(client_fd, client_addr);
				close(client_fd);
				break;
			}
		}
		else
		{
			cout << "failed to accept" << endl;
		}
		close(client_fd);
	}

	close(socket_fd);
	return 0;
}
