all: buf divzero fmt sleep stderr getopt getenv ld_preload-get-vars

buf:
	gcc -o buf buf.c

divzero:
	gcc -o divzero divzero.c

fmt:
	gcc -o fmt fmt.c

sleep:
	gcc -o sleep sleep.c

stderr:
	gcc -o stderr stderr.c

getopt:
	gcc -o getopt getopt.c

getenv:
	gcc -o getenv getenv.c

ld_preload-get-vars:
	gcc -fPIC -c ld_preload-get-vars.c -o ld_preload-get-vars.o
	gcc -shared -o ld_preload-get-vars.so ld_preload-get-vars.o

clean:
	rm -rf *.o *.so buf divzero fmt sleep stderr getenv getopt *~

