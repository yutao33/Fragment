
if (CMAKE_SYSTEM_NAME MATCHES "Windows")
# the name of the target operating system
# SET(CMAKE_SYSTEM_NAME Windows)

# which compilers to use for C and C++
SET(CMAKE_C_COMPILER x86_64-w64-mingw32-gcc-posix)
SET(CMAKE_CXX_COMPILER x86_64-w64-mingw32-g++-posix)
# SET(CMAKE_RC_COMPILER i586-mingw32msvc-windres)

# here is the target environment located
SET(CMAKE_FIND_ROOT_PATH  /usr/x86_64-w64-mingw32)

# adjust the default behaviour of the FIND_XXX() commands:
# search headers and libraries in the target environment, search
# programs in the host environment
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

endif (CMAKE_SYSTEM_NAME MATCHES "Windows")

# cmake -G "Unix Makefiles" -DCMAKE_SYSTEM_NAME=Windows -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=../ToolChain.cmake -DCMAKE_INSTALL_PREFIX=/Program/llvm ../..
# cmake -G "Unix Makefiles"  -DCMAKE_BUILD_TYPE=Release -DCMAKE_SYSTEM_NAME=Windows  -DCMAKE_CXX_COMPILER=`which x86_64-w64-mingw32-g++-posix` -DCMAKE_C_COMPILER=`which x86_64-w64-mingw32-gcc-posix` ..