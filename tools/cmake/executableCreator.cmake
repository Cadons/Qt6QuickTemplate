# Define executable target
QT6_ADD_EXECUTABLE(${PROJECT_NAME} ${SOURCES} ${RESOURCES})
target_link_libraries(${PROJECT_NAME} PRIVATE ${PROJECT_LIBRARIES})
include_directories(${PROJECT_NAME} "${CMAKE_CURRENT_LIST_DIR}/../../include")
# Deployment section for Qt dependencies
include(tools/cmake/Deploy.cmake)
