
all: main.c libmylib.so
	gcc main.c -L . -lmylib -lm -Wl,-rpath . -o main

libmylib.so: lib.c
	gcc $< -shared -fPIC -o $@

clean:
	rm main libmylib.so
