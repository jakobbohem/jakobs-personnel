## chatGPT4 -program

import os
import shutil
import git

def git_pull_and_copy(src_dir, target_file, dest_dir):
    # Save the current working directory
    original_wd = os.getcwd()

    try:
        # Move to the source directory
        os.chdir(src_dir)

        # Initialize GitPython repo object
        repo = git.Repo(os.getcwd())

        # Perform git pull
        try:
            origin = repo.remote(name='origin')
            origin.pull('main')
            print("Git pull successful.")
        except git.GitCommandError as e:
            print(f"Git pull failed: {e}")
            return

        # Check if target file exists
        if not os.path.exists(target_file):
            print(f"Error: File {target_file} does not exist in {src_dir}")
            return

        # Copy the specified file to original working directory
        dest_path = os.path.join(dest_dir, os.path.basename(target_file))
        shutil.copy(target_file, dest_path)
        print(f"File {target_file} copied to {dest_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Change back to the original working directory
        os.chdir(original_wd)

# Example usage
src_dir = './some_relative_path'
target_file = 'some_file.txt'
dest_dir = './'
git_pull_and_copy(src_dir, target_file, dest_dir)
