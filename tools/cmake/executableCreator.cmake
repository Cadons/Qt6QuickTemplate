# Define executable target
QT6_ADD_EXECUTABLE(${PROJECT_NAME} ${SOURCES})
target_link_libraries(${PROJECT_NAME} PRIVATE ${PROJECT_LIBRARIES})
include_directories(${PROJECT_NAME} ${Lib_HDRS})
# Deployment section for Qt dependencies
include(tools/cmake/Deploy.cmake)
