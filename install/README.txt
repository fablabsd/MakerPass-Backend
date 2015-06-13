

Dependencies:


** WeMo API ("ouimeaux") -- follow instructions in the docs dirctory for easy_install 
(note this is not how we did it initially for this install, but running easy_install 
does confirm we are fully installed)
For further easy-to-read docs go here:
http://ouimeaux.readthedocs.org/en/latest/wemo.html

** SSH for git -- this facilitates auto-push/pull with no need for password entry.  You need to:
	(a) create a public key "ssh-keygen -t rsa", then copy the id_rsa.pub contents into 
	the "add key" dialog in bitbucket, under "manage account" then "ssh keys."  
	(b)  Then in your .git/config file replace the https url link with the new link that is 
	generated under the "clone" dialog in bitbucket (it should show "SSH" as the selected link).
   
** SQLite -- sudo apt-get install sqlite3 
If you get a weird error about it not existing in /usr/local/bin just do a which sqlite3 and 
you will see it's installed in /usr/bin...no idea why it's looking for it in usr/local/bin -- might
have something to do with the fact that my first attempt on this involved compiling from source
A lot of good sqlite info can be found here (about the CLI):
https://www.sqlite.org/cli.html

