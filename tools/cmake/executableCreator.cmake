# Define executable target
QT6_ADD_EXECUTABLE(${PROJECT_NAME} ${SOURCES})
target_link_libraries(${PROJECT_NAME} PRIVATE ${PROJECT_LIBRARIES})

# Deployment section for Qt dependencies
include(tools/cmake/Deploy.cmake)