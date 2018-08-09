1. About the project:
	Using CMake build system, can be compiled on Windows or Unix-like platform

2. Files:
	src/   source files
	bin/   binary files that are linked statically on Windows


3. Usage:
	DictServer(1) 127.0.0.1 4500
	DictClient 127.0.0.1 4500 word

4. Build procedure:

mkdir build
cd build

on Windows using Visual Studio:

    cmake ..
	or static link c++ library
	cmake .. -DCMAKE_USER_MAKE_RULES_OVERRIDE=compiler_flags_overrides.cmake
	

on Unix using gcc:
    
    cmake -DCMAKE_BUILD_TYPE=Debug
    cmake -DCMAKE_BUILD_TYPE=Release