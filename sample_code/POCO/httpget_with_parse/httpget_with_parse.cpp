//
// httpget_with_parse.cpp
//
// $Id: //poco/1.4/Net/samples/httpget/src/httpget.cpp#3 $
//
// This is a combo of httpget.cpp and DOMParse.cpp
//
// Copyright (c) 2005-2012, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "Poco/Net/HTTPClientSession.h"
#include "Poco/Net/HTTPRequest.h"
#include "Poco/Net/HTTPResponse.h"
#include <Poco/Net/HTTPCredentials.h>
#include "Poco/StreamCopier.h"
#include "Poco/NullStream.h"
#include "Poco/Path.h"
#include "Poco/URI.h"
#include "Poco/Exception.h"
#include <iostream>
#include <sstream>
#include "Poco/DOM/DOMParser.h"
#include "Poco/DOM/Document.h"
#include "Poco/DOM/NodeIterator.h"
#include "Poco/DOM/NodeFilter.h"
#include "Poco/DOM/AutoPtr.h"
#include "Poco/SAX/InputSource.h"


using Poco::XML::DOMParser;
using Poco::XML::InputSource;
using Poco::XML::Document;
using Poco::XML::NodeIterator;
using Poco::XML::NodeFilter;
using Poco::XML::Node;
using Poco::XML::AutoPtr;
using Poco::Net::HTTPClientSession;
using Poco::Net::HTTPRequest;
using Poco::Net::HTTPResponse;
using Poco::Net::HTTPMessage;
using Poco::StreamCopier;
using Poco::Path;
using Poco::URI;
using Poco::Exception;



bool doRequest(Poco::Net::HTTPClientSession& session, Poco::Net::HTTPRequest& request, Poco::Net::HTTPResponse& response, std::string& response_string)
{
	session.sendRequest(request);
	std::istream& out = session.receiveResponse(response);
	//std::cout << response.getStatus() << " " << response.getReason() << std::endl;
	if (response.getStatus() != Poco::Net::HTTPResponse::HTTP_UNAUTHORIZED)
	{
		//StreamCopier::copyStream(out, std::cout);
		//StreamCopier::copyStream(out, response_ostream);

    		std::stringstream ss;
    		ss << out.rdbuf();
    		response_string = ss.str();
		return true;
	}
	else
	{
		Poco::NullOutputStream null;
		StreamCopier::copyStream(out, null);
		return false;
	}
}


int main(int argc, char** argv)
{
	if (argc != 2)
	{
		Path p(argv[0]);
		std::cout << "usage: " << p.getBaseName() << " <uri>" << std::endl;
		std::cout << "       fetches the resource identified by <uri> and print it to the standard output" << std::endl;
		return 1;
	}

	try
	{
		URI uri(argv[1]);
		std::string path(uri.getPathAndQuery());
		if (path.empty()) path = "/";

        std::string username;
        std::string password;
        Poco::Net::HTTPCredentials::extractCredentials(uri, username, password);
        Poco::Net::HTTPCredentials credentials(username, password);

		HTTPClientSession session(uri.getHost(), uri.getPort());
		HTTPRequest request(HTTPRequest::HTTP_GET, path, HTTPMessage::HTTP_1_1);
		HTTPResponse response;
		std::string response_string;
		if (!doRequest(session, request, response, response_string))
		{
            		credentials.authenticate(request, response);
			if (!doRequest(session, request, response, response_string))
			{
				std::cerr << "Invalid username or password" << std::endl;
				return 1;
			}
		}


// Chris_A Inserting DOMParser code here  ------------------------


        	//InputSource src(std::cin);
                DOMParser parser;
                //AutoPtr<Document> pDoc = parser.parse(&src);
                AutoPtr<Document> pDoc = parser.parseString(response_string);

                NodeIterator it(pDoc, NodeFilter::SHOW_ALL);
                Node* pNode = it.nextNode();
                while (pNode)
                {
                        //std::cout << "--N " << pNode->nodeName() << " N-- : --V " << pNode->nodeValue() << " V--" << std::endl;


 			if(pNode->nodeName() == "INVOICEList")
 			{
   				pNode = it.nextNode();
   				if(pNode->nodeName() != "#text")
   				{
     					continue; //No text node present
   				}
   				std::cout << "Tag Text: " << pNode->nodeValue() << std::endl;
  			}


                        pNode = it.nextNode();
                }


// End Chris_A modification ---------------------------


	}
	catch (Exception& exc)
	{
		std::cerr << exc.displayText() << std::endl;
		return 1;
	}
	return 0;
}
