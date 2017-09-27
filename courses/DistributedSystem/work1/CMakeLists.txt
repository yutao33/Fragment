project( work1 )
cmake_minimum_required( VERSION 2.8 )

set(CMAKE_VERBOSE_MAKEFILE ON)

add_executable( DictServer DictServer.cpp )
add_executable( DictServer1 DictServer1.cpp )
add_executable( DictClient DictClient.cpp )

message(${CMAKE_BUILD_TYPE})

if(WIN32)
    message("WIN32")
    target_link_libraries(DictServer ws2_32)
    target_link_libraries(DictServer1 ws2_32)
    target_link_libraries(DictClient ws2_32)
else(WIN32)
	message("not WIN32")
    set(CMAKE_CXX_FLAGS "--std=c++11")
    target_link_libraries(DictServer1 pthread)
    if(${CMAKE_BUILD_TYPE} MATCHES "Debug")
    	message("add debug definition")
        add_definitions(-D_DEBUG)
    endif(${CMAKE_BUILD_TYPE} MATCHES "Debug")
endif(WIN32)

