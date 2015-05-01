

#include <iostream>
#include <Poco/Net/MailMessage.h>
#include <Poco/Net/MailRecipient.h>
#include <Poco/Net/SMTPClientSession.h>
#include <Poco/Net/NetException.h>
using namespace std;
using namespace Poco::Net;
using namespace Poco;
int main(int argc, char *argv[])
{
    string host = "mail.google.com";
    UInt16 port = 25;
    string user = "thechrisanderson";
    string password = "Puzeopu4";
    string to = "thechrisanderson@gmail.com";
    string from = "thechrisanderson@gmail.com";
    string subject = "Your first e-mail message sent using Poco Libraries";
    subject = MailMessage::encodeWord(subject, "UTF-8");
    string content = "Well done! You've successfully sent your first message using Poco SMTPClientSession";
    MailMessage message;
    message.setSender(from);
    message.addRecipient(MailRecipient(MailRecipient::PRIMARY_RECIPIENT, to));
    message.setSubject(subject);
    message.setContentType("text/plain; charset=UTF-8");
    message.setContent(content, MailMessage::ENCODING_8BIT);
    try {
        SMTPClientSession session(host, port);
        session.open();
        try {
            session.login(SMTPClientSession::AUTH_LOGIN, user, password);
            session.sendMessage(message);
            cout << "Message successfully sent" << endl;
            session.close();
        } catch (SMTPException &e) {
            cerr << e.displayText() << endl;
            session.close();
            return 0;
        }
    } catch (NetException &e) {
        cerr << e.displayText() << endl;
        return 0;
    }
    return 0;
}
