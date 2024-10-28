
# Deployment section for Qt dependencies
include(tools/cmake/Qt6Deployer.cmake)

# Call deployment function
deploy_qt6_dependencies(${PROJECT_NAME})

# Install settings
include(InstallRequiredSystemLibraries)
install(TARGETS ${CMAKE_PROJECT_NAME}
    BUNDLE  DESTINATION .
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# Install all files in the build directory
install(DIRECTORY ${CMAKE_BINARY_DIR}/
    DESTINATION bin
    FILES_MATCHING PATTERN "*"
)

# Set the output directory for the package
set(CPACK_OUTPUT_DIRECTORY "${ARTIFACT_FOLDER}")
include(CPack)
