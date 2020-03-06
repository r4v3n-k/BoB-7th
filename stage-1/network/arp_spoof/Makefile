all : arp_spoof
arp_spoof: main.o
	g++ -g -o arp_spoof main.o -lpthread -lpcap
main.o:
	g++ -g -Wall -c -o main.o main.cpp -lpthread -lpcap
clean:
	rm -f arp_spoof
	rm -f *.o
