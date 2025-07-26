import os
from git import Repo, GitCommandError 

def clone_repo(repo_url: str, destination: str) -> None:
    if not os.path.exists(destination):
        try:
            Repo.clone_from(repo_url, destination)
            print(f"Repository cloned to {destination}")
        except GitCommandError as e:
            print(f"Error cloning repository: {e}")
    else:
        print(f"Destination {destination} already exists. Skipping clone.")

def pull_from_repo(repo_path: str) -> tuple[bool, str]:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            origin = repo.remotes.origin
            pull_info = origin.pull()
            return True, "Successfully pulled changes from remote."
        except GitCommandError as e:
            return False, f"Error pulling from repository: {e}"
    else:
        return False, f"Repository path {repo_path} does not exist."

def add_changes(repo_path: str, files: list) -> tuple[bool, str]:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            repo.index.add(files)
            message = f"Added changes for files: {', '.join(files)}"
            return True, message
        except GitCommandError as e:
            return False, f"Error adding changes: {e}"
    else:
        return False, f"Repository path {repo_path} does not exist."

def reset_changes(repo_path: str, files: list) -> tuple[bool, str]:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            for file in files:
                repo.git.reset('HEAD', file)
            message = f"Reset changes for files: {', '.join(files)}"
            return True, message
        except GitCommandError as e:
            return False, f"Error resetting changes: {e}"
    else:
        return False, f"Repository path {repo_path} does not exist."

def commit_changes(repo_path: str, message: str) -> tuple[bool, str]:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            repo.index.commit(message)
            return True, "Changes committed successfully."
        except GitCommandError as e:
            return False, f"Error committing changes: {e}"
    else:
        return False, f"Repository path {repo_path} does not exist."

def push_to_repo(repo_path: str) -> tuple[bool, str]:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            origin = repo.remotes.origin
            push_info = origin.push()
            
            # Check push results
            if push_info[0].flags & push_info[0].ERROR:
                return False, "Push failed with error."
            return True, "Changes pushed to remote repository."
        except GitCommandError as e:
            return False, f"Error pushing to repository: {e}"
    else:
        return False, f"Repository path {repo_path} does not exist."

def get_unstaged_files(repo_path: str) -> list:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            # Get modified files
            modified = [item.a_path for item in repo.index.diff(None)]
            # Get untracked files
            untracked = repo.untracked_files
            return modified + untracked
        except GitCommandError as e:
            print(f"Error getting unstaged files: {e}")
            return []
    else:
        print(f"Repository path {repo_path} does not exist.")
        return []

def get_staged_files(repo_path: str) -> list:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            # Get staged files by comparing index to HEAD
            staged = [item.a_path for item in repo.index.diff("HEAD")]
            return staged
        except GitCommandError as e:
            print(f"Error getting staged files: {e}")
            return []
    else:
        print(f"Repository path {repo_path} does not exist.")
        return []

def get_current_branch(repo_path: str) -> str:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            return repo.active_branch.name
        except GitCommandError as e:
            print(f"Error getting current branch: {e}")
            return ""
    else:
        print(f"Repository path {repo_path} does not exist.")
        return ""

def get_file_diff(repo_path: str, file_path: str, staged: bool = False) -> str:
    """Get the diff for a specific file."""
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            if staged:
                # Get diff for staged changes
                diff = repo.git.diff('--cached', file_path)
            else:
                # Get diff for unstaged changes
                diff = repo.git.diff(file_path)
            return diff
        except GitCommandError as e:
            print(f"Error getting diff: {e}")
            return ""
    return ""

def get_config(key: str) -> str:
    """Get Git configuration value."""
    try:
        repo = Repo(".")
        return repo.git.config("--get", key)
    except:
        return ""

def set_config(key: str, value: str) -> None:
    """Set Git configuration value."""
    try:
        repo = Repo(".")
        repo.git.config(key, value)
    except GitCommandError as e:
        print(f"Error setting config {key}: {e}")