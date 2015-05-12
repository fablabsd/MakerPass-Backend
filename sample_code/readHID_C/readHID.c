#include <stdio.h>
#include <errno.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define MAX_BUF_SIZE  10
/*

readHID.c -- Read a string from a rawHID device in /dev

*/


int main(int argc, char *argv[])
{
    int fd, ret_val, count, numread,i;
    char buf[MAX_BUF_SIZE];

    if (argc < 2) {
	printf("\nUsage:  readHID <device from /dev>\n\n");
	return 1;
    }
    

    /* Open the device for reading */
    fd = open(argv[1], O_RDWR);

    while(1) {

    	/* Read from device */
    	numread = read(fd, buf, MAX_BUF_SIZE);

    	buf[numread] = '\0';
   
	/*printf("%i \n", numread); */
	/*printf("%i", buf);*/
	for (i = 0; i < numread; ++i) {
		int intval = 0;
		intval = (unsigned int) buf[i];
		if (intval > 0) { 
			printf("%i ", intval);
			if (intval == 88) { printf("\n");  }
		}

	}
	
	fflush(stdout);


    }

    /* we won't get here, but for solidarity..*/
    close(fd);
} // end main()
