# Qt Quick Template
## Installation Instructions

### 1. Install vcpkg
Follow the setup instructions for vcpkg on the [official Microsoft documentation](https://learn.microsoft.com/en-us/vcpkg/get_started/overview).

### 2. Clone the Repository
Clone this project to your local environment.

### 3. Configure CMake Presets
1. In the root of the project, create a file named `CMakeUserPresets.json`.
2. Use the following preset template:

    ```json
    {
      "version": 3,
      "configurePresets": [
        {
          "name": "default",
          "hidden": true,
          "generator": "Ninja",
          "binaryDir": "${sourceDir}/build",
          "cacheVariables": {
            "CMAKE_TOOLCHAIN_FILE": "<Path to vcpkg location>/vcpkg/scripts/buildsystems/vcpkg.cmake",
            "CMAKE_PREFIX_PATH": "$env{QTDIR}"
          }
        },
        {
          "name": "Debug-Ninja",
          "inherits": "default",
          "description": "Debug build with Ninja generator",
          "cacheVariables": {
            "CMAKE_BUILD_TYPE": "Debug"
          }
        },
        {
          "name": "Release-Ninja",
          "inherits": "default",
          "description": "Release build with Ninja generator",
          "cacheVariables": {
            "CMAKE_BUILD_TYPE": "Release"
          }
        },
        {
          "name": "Debug-VisualStudio",
          "inherits": "default",
          "generator": "Visual Studio 17 2022",
          "architecture": {
            "value": "x64"
          },
          "description": "Debug build with Visual Studio generator",
          "cacheVariables": {
            "CMAKE_BUILD_TYPE": "Debug"
          }
        },
        {
          "name": "Release-VisualStudio",
          "inherits": "default",
          "generator": "Visual Studio 17 2022",
          "architecture": {
            "value": "x64"
          },
          "description": "Release build with Visual Studio generator",
          "cacheVariables": {
            "CMAKE_BUILD_TYPE": "Release"
          }
        },
        {
          "name": "Debug-UnixMakefiles",
          "inherits": "default",
          "generator": "Unix Makefiles",
          "description": "Debug build with Unix Makefiles generator",
          "cacheVariables": {
            "CMAKE_BUILD_TYPE": "Debug"
          }
        },
        {
          "name": "Release-UnixMakefiles",
          "inherits": "default",
          "generator": "Unix Makefiles",
          "description": "Release build with Unix Makefiles generator",
          "cacheVariables": {
            "CMAKE_BUILD_TYPE": "Release"
          }
        },
        {
          "hidden": true,
          "name": "Qt-Default",
          "inherits": null,
          "vendor": {
            "qt-project.org/Default": {
              "checksum": "VoalogTkyWuFomeO1TLFx0olLJ4="
            }
          }
        }
      ],
      "vendor": {
        "qt-project.org/Presets": {
          "checksum": "r/8mpKzVd/5Hmlwd9l9908VMhsw="
        }
      }
    }
    ```

### 4. Select a Build Preset
Choose a build preset with your preferred generator (e.g., Ninja or Visual Studio).

### 5. Update `vcpkg.json` if Needed
To modify project metadata such as the name or maintainers in your project, follow these steps:

1. **Update `vcpkg.json`**: Open the `vcpkg.json` file and make the necessary changes to the project name, maintainers, or any other metadata.

2. **Run the Setup Script**: Navigate to the `tools` folder in your project directory and execute the `setup.py` script to apply your changes:

   ```bash
   python setup.py
   ```

3. **Install Dependencies**: Before running the setup script, ensure you have all required dependencies installed. Use the following command:

   ```bash
   pip install -r requirements.txt
   ```

Following these steps will ensure your project metadata is updated correctly and that all necessary dependencies are in place.


### 6. Install System Dependencies (macOS and Linux Only)
For macOS and Linux systems, install the following packages to enable required build tools:

- **Debian/Ubuntu:**

      
      sudo apt-get install autoconf automake autoconf-archive
      

- **Red Hat/Fedora:**
  
   
      sudo dnf install autoconf automake autoconf-archive


- **Arch Linux:**

 
      sudo pacman -S autoconf automake autoconf-archive


- **Alpine Linux:**


      apk add autoconf automake autoconf-archive

- **macOS:**


      brew install autoconf automake autoconf-archive


### 7. Configure and Build the Project
Run `cmake` with the selected preset. This will trigger vcpkg to install dependencies in `build/vcpkg_installed` and configure the project. Once configured, you can build the project using your preferred IDE or `cmake --build`.

### 8. Adding New Dependencies
When adding a new dependency, simply reconfigure CMake, and vcpkg will automatically install any newly specified packages.

### Additional Resources
For further information about vcpkg usage, see the [official documentation](https://learn.microsoft.com/en-us/vcpkg/)