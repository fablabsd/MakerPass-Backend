
#include "Poco/Util/XMLConfiguration.h"
#include "Poco/Exception.h"
#include <iostream>


using Poco::AutoPtr;
using Poco::Util::XMLConfiguration;
using namespace std;



int main(int argc, char** argv)
{



	AutoPtr<XMLConfiguration> pConf(new XMLConfiguration("configuration.xml"));
	std::string prop1 = pConf->getString("prop1");
	cout << "prop1 = " << prop1 << endl;
	int prop2 = pConf->getInt("prop2");
	cout << "prop2 = " << prop2 << endl;
	std::string prop3 = pConf->getString("prop3"); // ""
	cout << "prop3 = " << prop3 << endl;
	std::string prop4 = pConf->getString("prop3.prop4"); // ""
	cout << "prop4 = " << prop4 << endl;
	prop4 = pConf->getString("prop3.prop4[@attr]"); // "value3"
	cout << "prop4 = " << prop4 << endl;
	prop4 = pConf->getString("prop3.prop4[1][@attr]"); // "value4"
	cout << "prop4 = " << prop4 << endl;


	return 0;

}



