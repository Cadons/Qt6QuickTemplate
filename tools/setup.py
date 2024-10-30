import json
import os
import os.path
from traceback import print_tb
from git import Repo

vcpkg_json_path = os.path.join("..", "vcpkg.json")

def load_vcpkg_json(vcpkg_json_path):
    """Load the vcpkg.json file and return its content as a dictionary."""
    try:
        with open(vcpkg_json_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: {vcpkg_json_path} not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: {vcpkg_json_path} is not a valid JSON file.")

def create_semver(vcpkg_data):
    """Create a SemVer string from version fields."""
    # Check if version key is present and follows SemVer format
    version = vcpkg_data.get("version")
    if version and isinstance(version, str):
        # Simple check to see if it follows a SemVer pattern (major.minor.patch)
        if len(version.split('.')) == 3:
            return version

    # Fallback to version-semver
    major = vcpkg_data.get("version-semver", "0").split(".")
    if len(major) < 3:
        major += ["0"] * (3 - len(major))  # Fill missing parts with zeros
    return f"{major[0]}.{major[1]}.{major[2]}"

def get_git_tag(branch_name, repo:Repo):
    """Check if the given branch has an associated tag and return it."""
    tags = repo.tags
    for tag in tags:
        if tag.commit ==repo.head.commit:
            return str(tag)  # Return the tag name if it matches the current commit
    return None

def update_vcpkg_json(vcpkg_json_path, new_version):
    """Update the version in vcpkg.json if a new version is provided."""
    try:
        with open(vcpkg_json_path, 'r+') as file:
            vcpkg_data = json.load(file)
            vcpkg_data['version'] = new_version  # Update the version field
            file.seek(0)  # Move to the beginning of the file
            json.dump(vcpkg_data, file, indent=4)  # Write the updated data
            file.truncate()  # Remove any remaining part of the old data
        print(f"Updated vcpkg.json with version: {new_version}")
    except Exception as e:
        print(f"Failed to update vcpkg.json: {e}")

def collect_vpkg_data(vcpkg_data):
    """Collect specific environment data to write to config.cmake."""
    vpkg_data = {}

    # Define the keys we want to collect
    needed_keys = [
        "name",
        "version",
        "maintainers",
        "description",
        "documentation",
        "homepage",
        "license",
        "version-semver",
        "version-string",
        "version-date"
    ]

    # Collect data from vcpkg.json
    for key in needed_keys:
        if key in vcpkg_data:
            vpkg_data[f"QT_PROJECT_{key.upper()}"] = str(vcpkg_data[key])

    # Create the SemVer string
    vpkg_data["QT_PROJECT_SEMVER"] = create_semver(vcpkg_data)

    # Get the current branch name and check for a tag
    try:
        local_repo = Repo(path=os.path.join(os.curdir,".."))

        local_branch = local_repo.active_branch.name
        # Check if there's a tag on the current branch's commit
        tag_name = get_git_tag(local_branch,local_repo)
        
        if tag_name:
            vpkg_data["QT_PROJECT_VERSION"] = f"{tag_name}"
            update_vcpkg_json(vcpkg_json_path, tag_name)  # Update the version if there's a tag

        else:
            vpkg_data["QT_PROJECT_VERSION"] = f"{vpkg_data.get('QT_PROJECT_SEMVER', '1.0.0')}-{local_branch}"
    except Exception:
        print("Error during version retriving")
        vpkg_data["QT_PROJECT_VERSION"] = vpkg_data.get("QT_PROJECT_SEMVER", "1.0.0")

    return vpkg_data

def write_config_cmake(vpkg_data):
    """Write the collected environment data to config.cmake."""
    config_file_path = os.path.join("cmake","config.cmake")
    with open(config_file_path, 'w') as f:
        f.write("# config.cmake\n\n")
        
        # Write QT_PROJECT_VERSION
        f.write("set(QT_PROJECT_VERSION \"{}\")\n".format(vpkg_data.get("QT_PROJECT_VERSION", "unknown")))
        f.write("message(STATUS \"QT_PROJECT_VERSION set to: ${QT_PROJECT_VERSION}\")\n\n")
        
        # Write QT_PROJECT_SEMVER
        f.write("set(QT_PROJECT_SEMVER \"{}\")\n".format(vpkg_data.get("QT_PROJECT_SEMVER", "0.0.0")))
        f.write("message(STATUS \"QT_PROJECT_SEMVER set to: ${QT_PROJECT_SEMVER}\")\n\n")

        # Write other variables
        for key, value in vpkg_data.items():
            if key not in ["QT_PROJECT_VERSION", "QT_PROJECT_SEMVER"]:
                f.write(f"set({key} \"{value}\")\n")
                f.write(f"message(STATUS \"{key} set to: ${{{key}}}\")\n\n")

# Main function to load vcpkg.json, collect data, and write to config.cmake
def main():

    try:
        print("Configuring project....")
        vcpkg_data = load_vcpkg_json(vcpkg_json_path)
        vpkg_data = collect_vpkg_data(vcpkg_data)

        write_config_cmake(vpkg_data)
        print("Project Ready")
    except Exception as e:
        print(e)

# Run the main function
main()
