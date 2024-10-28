# ---------------------------------------------------------------------
# Qt project template for QML applications with VCPKG
# ---------------------------------------------------------------------
cmake_minimum_required(VERSION 3.16)
include(tools/cmake/qtProject.cmake)

# Find Qt packages
find_package(Qt6 REQUIRED COMPONENTS Qml Quick Core QuickControls2)

#Enable modules
set(PROJECT_LIBRARIES Qt6::Core Qt6::Quick Qt6::QuickControls2)
#Resources
set(RESOURCES ${CMAKE_CURRENT_LIST_DIR}/resources/resources.qrc)
#Create the executable and configure deployment
include(tools/cmake/executableCreator.cmake)

#Other project sections

# Optional subdirectory for tests
add_subdirectory(test)
#other subdirectories
