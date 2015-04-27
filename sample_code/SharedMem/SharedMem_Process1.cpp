

#include "Poco/SharedMemory.h"
#include "Poco/Exception.h"
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

using Poco::SharedMemory;
using namespace std;

typedef struct {

	int val1;
	float val2;
	char val3;
} MY_MEM; 


int main(int argc, char** argv)
{

	//SharedMemory mem("MySharedMemory", 1024,
	SharedMemory mem("MySharedMemory", sizeof(MY_MEM),
	SharedMemory::AM_READ | SharedMemory::AM_WRITE);
	
	// access shared mem with casted pointer
	MY_MEM *shared_memory = (MY_MEM *) mem.begin();
	
	shared_memory->val1 = 2;
	shared_memory->val2 = 3.0;
	shared_memory->val3 = 'a';

	// Sleep for a few seconds to give process 2 a chance to read the memory
	sleep(5);

	return 0;

}



