all: sum_test

main.o:	main.cpp sum.h
		g++ -c -o main.o main.cpp

sum.o: sum.cpp
		g++ -c -o sum.o sum.cpp

clean:
	rm -f *.o
	rm -f sum_test
