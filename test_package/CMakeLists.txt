project(helloworld)
cmake_minimum_required(VERSION 3.15)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(gdal REQUIRED)

add_executable(helloworld main.cpp)

target_link_libraries(helloworld
    PUBLIC
    gdal::gdal
)

set_target_properties(helloworld
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    )