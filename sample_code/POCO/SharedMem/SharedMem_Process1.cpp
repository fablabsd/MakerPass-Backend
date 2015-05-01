

#include "Poco/SharedMemory.h"
#include "Poco/NamedMutex.h"
#include "Poco/Exception.h"
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "MySharedMemoryStruct.h"

using Poco::SharedMemory;
using Poco::NamedMutex;
using namespace std;

// Declare a named mutex (to be distinguished from a regular mutex
// in that a regular mutex works only on threads, hence no need for
// an identifier) - this is for the purpose of INTERPROCESS memory 
// synchronization
Poco::NamedMutex _mutex("MyInterprocessMutex");

// declare a shared mem variable
MY_MEM *shared_memory = 0;


// declare an example function for concurrency
void criticalSection()
{
	NamedMutex::ScopedLock lock(_mutex);

	shared_memory->val1 = 2;
	shared_memory->val2 = 3.0;
	shared_memory->val3 = 'a';

	cout << "Sleeping inside critical section" << endl;
	sleep(5);


}



int main(int argc, char** argv)
{

	//SharedMemory mem("MySharedMemory", 1024,
	SharedMemory mem("MySharedMemory", sizeof(MY_MEM),
	SharedMemory::AM_READ | SharedMemory::AM_WRITE);
	
	// access shared mem with casted pointer
	shared_memory = (MY_MEM *) mem.begin();

	cout << "Process1 entering critical section" << endl;
	criticalSection();	
	cout << "Process1 exited critical section" << endl;
	


	return 0;

}



