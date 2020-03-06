all: test2

test2: main.o
	g++ -g -o test2 main.o -ltins

main.o: main.cpp
	g++ -g -c -o main.o main.cpp

clear:
	rm -f *.o
	rm -f test2

