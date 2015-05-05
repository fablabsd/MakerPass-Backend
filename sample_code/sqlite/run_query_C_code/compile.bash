

echo g++  -Wall -Wno-sign-compare  -O2  -fPIC  -c ./run_query.cpp  -o ./run_query.o 
g++  -Wall -Wno-sign-compare  -O2  -fPIC  -c ./run_query.cpp  -o ./run_query.o

echo g++ -O2 -Wl,-rpath,/usr/local/lib -o ./httpget ./httpget.o -L/home/pi/temp/sqlite-autoconf-3080900/.libs  -lpthread -ldl -lrt

g++ -O2 -Wl,-rpath,/usr/local/lib -o ./run_query ./run_query.o -L/home/pi/temp/sqlite-autoconf-3080900/.libs  -lpthread -ldl -lrt -lsqlite3


 
