cmake_minimum_required(VERSION 3.20)
set(CMAKE_CXX_STANDARD 20)

set(CMAKE_PREFIX_PATH_PATH "C:\\vcpkg\\installed\\x64-windows\\share")

project(WebMovieCollector)
find_package(CURL REQUIRED)
add_executable(WebMovieCollector main.cpp
        Requester.cpp
        Requester.h)
target_link_libraries(WebMovieCollector PRIVATE CURL::libcurl)
