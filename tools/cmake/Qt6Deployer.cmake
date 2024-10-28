function(deploy_qt6_dependencies target)
    if(WIN32)
        if(CMAKE_BUILD_TYPE STREQUAL "Debug" OR "$<CONFIG>" STREQUAL "Debug")
            set(DEPLOYMENT_TOOL ".debug.bat")
            set(QML_DIR "debug/Qt6/qml")
        else()
            set(DEPLOYMENT_TOOL ".exe")
            set(QML_DIR "Qt6/qml")
        endif()

        set(WINDEPLOYQT6_PATH "${PROJECT_VCPKG_INSTALLED_ROOT}/x64-windows/tools/Qt6/bin/windeployqt${DEPLOYMENT_TOOL}")
        
        if(EXISTS ${WINDEPLOYQT6_PATH})
            add_custom_command(TARGET ${target} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E echo "Deploying Qt dependencies for ${target}..."
                COMMAND ${WINDEPLOYQT6_PATH}
                --qmldir "${Qt6_DIR}/../../${QML_DIR}"
                $<TARGET_FILE:${target}>
                WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
            )
        else()
            message(FATAL_ERROR "windeployqt tool not found! [${WINDEPLOYQT6_PATH}]")
        endif()
    elseif(APPLE)
        add_custom_command(TARGET ${target} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E echo "Deploying dependencies for macOS..."
            COMMAND ${CMAKE_COMMAND} -E copy_directory
                "${Qt6_DIR}/../../../lib/Qt/lib"
                "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/"
        )
    elseif(UNIX)
        add_custom_command(TARGET ${target} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E echo "Deploying dependencies for Linux..."
            COMMAND ${CMAKE_COMMAND} -E copy_directory
                "${Qt6_DIR}/../../../lib/Qt/lib"
                "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/"
        )
    endif()
endfunction()
