import os
import subprocess
import shutil
import json
import stat
import gc
from time import sleep
from git import Repo, exc

# Constants
VCPKG_REPO_URL = "git@srv-git.medacta.locale:mysw_dev/vcpkg.git"  # Replace with actual VCPKG repo URL
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(PROJECT_DIR, "tmp")
VCPKG_CLONE_PATH = os.path.join(TMP_DIR, "vcpkg_temp")

# Paths
vcpkg_json_path = os.path.join(PROJECT_DIR, "..", "vcpkg.json")
portfile_template_path = os.path.join(PROJECT_DIR, "cmake", "portfile_template.cmake")
portfile_output_path = os.path.join(TMP_DIR, "ports")

# Create tmp directory
os.makedirs(TMP_DIR, exist_ok=True)

# Utilities
def find_git_root(path):
    """Find the root Git directory by traversing upwards."""
    while not os.path.isdir(os.path.join(path, ".git")):
        parent = os.path.dirname(path)
        if parent == path:
            raise exc.InvalidGitRepositoryError(f"No .git directory found in {PROJECT_DIR} or its parents.")
        path = parent
    return path

def get_project_name():
    """Read the project name from vcpkg.json."""
    with open(vcpkg_json_path, "r") as f:
        data = json.load(f)
    return data["name"]

def handle_remove_readonly(func, path, exc_info):
    """Error handler for removing read-only files."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_with_retries(path, retries=5, delay=2):
    """Retry deletion with exponential backoff on failure."""
    os.chdir(PROJECT_DIR)
    for attempt in range(retries):
        try:
            shutil.rmtree(path, onerror=handle_remove_readonly)
            print(f"Deleted {path} successfully.")
            return
        except Exception as e:
            if attempt < retries - 1:
                print(f"Retry {attempt + 1}/{retries} to delete {path} failed due to: {e}. Retrying...")
                sleep(delay * (2 ** attempt))  # Exponential backoff
            else:
                print(f"Failed to delete {path} after {retries} attempts: {e}")

# Git operations
def clone_vcpkg_repo():
    """Clone the vcpkg repository."""
    if os.path.exists(VCPKG_CLONE_PATH):
        delete_with_retries(VCPKG_CLONE_PATH)
    Repo.clone_from(VCPKG_REPO_URL, VCPKG_CLONE_PATH).close()

def add_and_commit(repo, message):
    """Add all changes and commit to the provided repository."""
    repo.git.add(A=True)
    repo.index.commit(message)

# Portfile creation
def create_portfile(repo_url, last_tag, project_name):
    """Generate portfile.cmake from the template."""
    os.makedirs(portfile_output_path, exist_ok=True)
    with open(portfile_template_path, "r") as template_file:
        template_content = template_file.read()
    portfile_content = template_content.replace("<REPO>", repo_url).replace("<REF>", last_tag)
    
    portfile_path = os.path.join(portfile_output_path, project_name, "portfile.cmake")
    os.makedirs(os.path.dirname(portfile_path), exist_ok=True)  # Create the project directory
    with open(portfile_path, "w") as portfile_file:
        portfile_file.write(portfile_content)
    shutil.copyfile(vcpkg_json_path, os.path.join(portfile_output_path, project_name, "vcpkg.json"))

# Vcpkg operations
def run_vcpkg_commands(project_name):
    """Run vcpkg format-manifest and x-add-version commands."""
    vcpkg_json_path_local = os.path.join("ports", project_name, "vcpkg.json")
    try:
        subprocess.run(["vcpkg", "format-manifest", vcpkg_json_path_local], check=True)
        subprocess.run([
            "vcpkg",
            "--x-builtin-ports-root=./ports",
            "--x-builtin-registry-versions-dir=./versions",
            "x-add-version", "--all", "--verbose", "--overwrite-version"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running vcpkg commands: {e}")
        raise

# Main workflow
try:
    # Get project and repo details
    project_name = get_project_name()
    git_root = find_git_root(PROJECT_DIR)
    
    # Retrieve repository info
    repo = Repo(git_root)
    repo_url = next(repo.remote().urls)
    last_tag = repo.git.describe("--tags", "--abbrev=0")
    del repo  # Free resources
    
    # Generate portfile.cmake and clone vcpkg repository
    create_portfile(repo_url, last_tag, project_name)
    clone_vcpkg_repo()
    
    # Commit the new portfile to vcpkg repository
    repo = Repo(VCPKG_CLONE_PATH)
    add_and_commit(repo, f"{project_name} files added to the registry")
    
    # Run vcpkg commands
    os.chdir(VCPKG_CLONE_PATH)
    run_vcpkg_commands(project_name)
    
    # Finalize by committing the registry addition and pushing
    add_and_commit(repo, f"{project_name} added to the registry")
    repo.git.push()
    
    # Show the last commit hash
    last_commit = repo.head.commit.hexsha
    print(f"Last commit hash in vcpkg repository (update vcpkg-configuration.json with this baseline):")
    print(f"{last_commit}")
    
    # Clean up
    del repo
    gc.collect()  # Force garbage collection
    
finally:
    # Ensure temporary vcpkg clone and ports are deleted
    delete_with_retries(TMP_DIR)


print(f"Process completed: {project_name} added to the vcpkg registry.")
