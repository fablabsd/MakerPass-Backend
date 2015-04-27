

#include "Poco/SharedMemory.h"
#include "Poco/Exception.h"
#include <iostream>
#include <stdio.h>
#include <string.h>


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
	MY_MEM *test_memory = (MY_MEM *) mem.begin();

	cout << "val1 = " << test_memory->val1 << endl;
	cout << "val2 = " << test_memory->val2 << endl;
	cout << "val3 = " << test_memory->val3 << endl;

	return 0;

}



