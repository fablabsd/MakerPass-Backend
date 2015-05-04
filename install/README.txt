

Dependencies:

** POCO -- untar, and follow instructions for install in linux in the README

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
   
** SQLite -- Read instruction in "INSTALL" file.  This probably just consists
of a ./configure; make; make install

