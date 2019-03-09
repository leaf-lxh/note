#include <iostream>
#include <fstream>


#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main()
{
	FILE *flag_file = popen("cat /flag*", "r");
	
	char *flag = new char[100];
	memset(flag, 0, 100);
	fgets(flag, 99, flag_file);

	std::cout << flag << std::endl;
	pclose(flag_file);

	return 0;
}

