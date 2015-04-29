#include "Poco/Thread.h"
#include "Poco/Runnable.h"
#include <iostream>


class Thread1: public Poco::Runnable
{
	virtual void run()
	{
		std::cout << "Hello, world! - thread 1" << std::endl;
	}
};


int main(int argc, char** argv)
{
	
	Thread1 runnable;
	Poco::Thread thread;
	thread.start(runnable);
	thread.join();
	return 0;

}
