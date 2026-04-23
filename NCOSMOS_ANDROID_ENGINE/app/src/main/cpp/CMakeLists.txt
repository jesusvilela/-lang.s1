cmake_minimum_required(VERSION 3.18.1)
project("ncosmos_engine")

add_library(
    ncosmos_engine
    SHARED
    ncosmos_engine.cpp
)

find_library(
    log-lib
    log
)

target_link_libraries(
    ncosmos_engine
    ${log-lib}
)
