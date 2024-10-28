include(tools/cmake/config.cmake)
message("-----------------CMake_Qt Project-------------------------")
message("Mantainer: ${QT_PROJECT_MAINTAINERS}")
message("Project Name:${QT_PROJECT_NAME}")
message("Description:${QT_PROJECT_DESCRIPTION}")
message("Version Semver:${QT_PROJECT_SEMVER}")
message("Version:${QT_PROJECT_VERSION}")
message("------------------------------------------")

message("Configuring Qt project.....")

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

# Set the project name
if(DEFINED QT_PROJECT_NAME)
    set(CMAKE_PROJECT_NAME ${QT_PROJECT_NAME})
    project(${CMAKE_PROJECT_NAME} CXX)
    message(STATUS "Project name set to: ${CMAKE_PROJECT_NAME}")
else()
    message(FATAL_ERROR "Project not configured, use setup.py in the tools folder. Add name to vcpkg.json")
endif()

# Optionally use the collected metadata in the project
set_property(GLOBAL PROPERTY USE_FOLDERS ON)
set_property(GLOBAL PROPERTY PROJECT_LABEL "${CMAKE_PROJECT_NAME} ${CMAKE_PROJECT_VERSION}")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON) 

set(ARTIFACT_FOLDER "${CMAKE_BINARY_DIR}/Packages")
set(PROJECT_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${CMAKE_BUILD_TYPE}")
set(PROJECT_VCPKG_INSTALLED_ROOT "${CMAKE_BINARY_DIR}/vcpkg_installed")

# Set output directories for different types of files
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_OUTPUT_DIRECTORY}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_OUTPUT_DIRECTORY}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${PROJECT_OUTPUT_DIRECTORY}/lib")

message(${PROJECT_NAME})

# Source file handling
file(GLOB_RECURSE Lib_SRCS "${CMAKE_CURRENT_LIST_DIR}/../../src/*.cpp" "${CMAKE_CURRENT_LIST_DIR}/src/*.cxx")
file(GLOB_RECURSE Lib_HDRS "${CMAKE_CURRENT_LIST_DIR}/../../include/*.h" "${CMAKE_CURRENT_LIST_DIR}/include/*.hpp")
set(SOURCES ${Lib_SRCS} ${Lib_HDRS})
set(RESOURCES "")
