set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON) 
# Define executable target
QT6_ADD_LIBRARY(${PROJECT_NAME} ${SOURCES})
target_link_libraries(${PROJECT_NAME} PRIVATE ${PROJECT_LIBRARIES})

# Deployment section for Qt dependencies
include(tools/cmake/Deploy.cmake)