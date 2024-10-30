vcpkg_from_git(
    OUT_SOURCE_PATH SOURCE_PATH
    URL <REPO>
    REF <REF>
)

# Configure the CMake build for both Release and Debug
vcpkg_cmake_configure(
    SOURCE_PATH "${SOURCE_PATH}"
    OPTIONS
        -DCMAKE_BUILD_TYPE=Release
        -DBUILD_TEST=OFF
)

# Build for Release
vcpkg_cmake_build()

# Install Release binaries
vcpkg_cmake_install()

# Copy PDB files for debugging information
vcpkg_copy_pdbs()

# Handle Debug configuration if needed
if (VCPKG_BUILD_TYPE STREQUAL "Debug")
    vcpkg_cmake_configure(
        SOURCE_PATH "${SOURCE_PATH}"
        OPTIONS
            -DCMAKE_BUILD_TYPE=Debug
            -DBUILD_TEST=OFF
    )
    
    # Build Debug binaries
    vcpkg_cmake_build()
    
    # Install Debug binaries
    vcpkg_cmake_install()
endif()

# Clean up debug include files
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")

# Install license file
file(
    INSTALL "${SOURCE_PATH}/LICENSE" 
    DESTINATION "${CURRENT_PACKAGES_DIR}/share/${PORT}" 
    RENAME copyright
)

# Copy usage documentation
configure_file("${CMAKE_CURRENT_LIST_DIR}/usage" "${CURRENT_PACKAGES_DIR}/share/${PORT}/usage" COPYONLY)
