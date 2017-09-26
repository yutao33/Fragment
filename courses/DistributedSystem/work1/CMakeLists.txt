project( work1 )
cmake_minimum_required( VERSION 2.8 )


add_executable( DictServer DictServer.cpp )
add_executable( DictClient DictClient.cpp )

if(WIN32)
    target_link_libraries(DictServer ws2_32)
    target_link_libraries(DictClient ws2_32)
else(WIN32)

endif(WIN32)

