import os
import subprocess
from decouple import config
import shutil

def create_directory(dir_name):
    source_directory = config('SOURCE_DUMP_PATH')
    directory = source_directory+'/'+dir_name
    if not os.path.exists(directory):
        os.makedirs(directory)

def pull_repository(repo_url, destination_dir,repo_name):
    try:
        destination_dir = os.path.join(destination_dir, repo_name)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        else:
            git_dir = os.path.join(destination_dir, ".git")
            if os.path.exists(git_dir) and os.path.isdir(git_dir):
                print(f"The directory {destination_dir} is already a Git repository.")
                shutil.rmtree(git_dir)

        result = subprocess.run(['git', 'clone', '--separate-git-dir', os.path.join(destination_dir, '.git'), repo_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        if result.returncode == 0:
            print(f"Repository cloned successfully into {destination_dir}")
        else:
            print(f"An error occurred while cloning the repository.")
    except Exception as e:
        print(f"Error: {e}")

class PushCodeError(Exception):
    pass

def push_code_to_repository(source_dir, destination_repo_url, branch_name):
    try:
        # Initialize a Git repository in the source directory
        subprocess.run(["git", "init"], cwd=source_dir)
        
        # Add all files in the source directory to the Git repository
        subprocess.run(["git", "add", "."], cwd=source_dir)
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", "Pushed spring boot code converted from EJB"], cwd=source_dir)

        # Add the remote repository as a remote named "origin"
        subprocess.run(["git", "remote", "add", "origin", destination_repo_url], cwd=source_dir)

        # Push the code to the remote repository
        subprocess.run(["git", "push", "-u", "origin", branch_name], cwd=source_dir)

        print(f"Code pushed successfully to {destination_repo_url}/{branch_name}")
    except Exception as e:
        raise PushCodeError(f"Code is converted but Unable to push the code: {e}")

# if __name__ == "__main__":
#     # Replace 'repo_url_here' with the actual repository URL
#     repo_url = 'https://github.com/tknerr/sample-ejb-app.git'
#     code_dir = 'code_test'

#     # Replace 'destination_dir_here' with the actual directory where you want to clone the repository
#     destination_dir = '/Users/skarnawadi/Documents/codetest/'+code_dir
#     create_directory(code_dir)

#     pull_repository(repo_url, destination_dir)




