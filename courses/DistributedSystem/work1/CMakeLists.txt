project( work1 )
cmake_minimum_required( VERSION 2.8 )

set(CMAKE_VERBOSE_MAKEFILE ON)

# set(EXECUTABLE_OUTPUT_PATH  ${PROJECT_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)
SET( CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
SET( CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})

file(GLOB_RECURSE CURRENT_HEADERS  *.h *.hpp)
source_group("Include" FILES ${CURRENT_HEADERS})

add_executable( DictServer DictServer.cpp Dict.cpp Dict.h Server.h Common.h)
add_executable( DictServer1 DictServer1.cpp Dict.cpp Dict.h Server.h Common.h)
add_executable( DictClient DictClient.cpp Common.h)

# add_custom_command(TARGET DictServer
#     POST_BUILD
#     WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
#     COMMAND ${CMAKE_COMMAND} -E copy dict.txt ${EXECUTABLE_OUTPUT_PATH}/dict.txt)
add_custom_command(OUTPUT dict.txt
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/dict.txt ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/dict.txt)

add_custom_target(COPYRES ALL DEPENDS dict.txt)

if(CMAKE_BUILD_TYPE)
	message(${CMAKE_BUILD_TYPE})
endif(CMAKE_BUILD_TYPE)

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

