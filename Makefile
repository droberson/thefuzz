all: buf divzero fmt sleep stderr getopt getenv ld_preload-get-vars

buf:
	gcc -o tests/buf tests/buf.c

divzero:
	gcc -o tests/divzero tests/divzero.c

fmt:
	gcc -o tests/fmt tests/fmt.c

sleep:
	gcc -o tests/sleep tests/sleep.c

stderr:
	gcc -o tests/stderr tests/stderr.c

getopt:
	gcc -o tests/getopt tests/getopt.c

getenv:
	gcc -o tests/getenv tests/getenv.c

ld_preload-get-vars:
	gcc -fPIC -c tests/ld_preload-get-vars.c -o tests/ld_preload-get-vars.o
	gcc -shared -o ld_preload-get-vars.so tests/ld_preload-get-vars.o

clean:
	rm -rf tests/*.o *.so tests/buf tests/divzero tests/fmt tests/sleep tests/stderr tests/getenv tests/getopt tests/*~

