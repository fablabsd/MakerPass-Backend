
#include "Poco/SharedMemory.h"
#include "Poco/NamedMutex.h"
#include "Poco/Exception.h"
#include <iostream>
#include <stdio.h>
#include <string.h>
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

        shared_memory->val1 = 3;
        shared_memory->val2 = 4.0;
        shared_memory->val3 = 'b';


}


int main(int argc, char** argv)
{

	SharedMemory mem("MySharedMemory", sizeof(MY_MEM),
	SharedMemory::AM_READ | SharedMemory::AM_WRITE);
	
	// access shared mem with casted pointer
	shared_memory = (MY_MEM *) mem.begin();

	cout << "Process2 printing shared mem before entering blocking/waiting critical section" << endl; 
	cout << "val1 = " << shared_memory->val1 << endl;
	cout << "val2 = " << shared_memory->val2 << endl;
	cout << "val3 = " << shared_memory->val3 << endl;

	cout << endl;
	cout << "Process2 Blocking..." << endl;
	cout << endl;


	criticalSection();
	
	cout << "Process2 printing shared mem after blocking/waiting critical section" << endl; 
	cout << "val1 = " << shared_memory->val1 << endl;
	cout << "val2 = " << shared_memory->val2 << endl;
	cout << "val3 = " << shared_memory->val3 << endl;

	return 0;

}



