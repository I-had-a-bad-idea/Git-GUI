import os
from git import Repo, GitCommandError 

def init_repo(path: str) -> tuple[bool, str]:
    try:
        Repo.init(path)
        return True, "Repository created successfully"
    except Exception as e:
        return False, str(e)

def clone_repo(repo_url: str, destination: str) -> tuple[bool, str]:

    if not os.path.exists(destination):
        try:
            Repo.clone_from(repo_url, destination)
            return True, f"Repository cloned successfully to {destination}"
        except GitCommandError as e:
            return False, str(e)
    else:
        return False, f"Destination {destination} already exists"


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
            repo.git.add(files)

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

def get_log(repo_path: str) -> tuple[bool, str, list]:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            log_entries = []
            for commit in repo.iter_commits():
                log_entries.append({
                    "commit": commit.hexsha,
                    "author": commit.author.name,
                    "date": commit.committed_datetime,
                    "message": commit.message.strip()
                })
            return True, "", log_entries
        except GitCommandError as e:
            print(f"Error getting log: {e}")
            return False, f"Error getting log: {e}", []
    else:
        return False, f"Repository path {repo_path} does not exist.", []

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
    try:
        repo = Repo(".")
        return repo.git.config("--get", key)
    except:
        return ""

def set_config(key: str, value: str) -> None:
    try:
        repo = Repo(".")
        repo.git.config(key, value)
    except GitCommandError as e:
        print(f"Error setting config {key}: {e}")

def get_remote_url(repo_path: str) -> str:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            return repo.remotes.origin.url
        except:
            return ""
    return ""

def get_branches(repo_path: str) -> tuple[bool, str, dict]:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            branches = [branch.name for branch in repo.heads]
            current = repo.active_branch.name
            return True, "", {"branches": branches, "current": current}
        except GitCommandError as e:
            return False, f"Error getting branches: {e}", {}
    return False, "Repository path does not exist", {}

def create_branch(repo_path: str, branch_name: str) -> tuple[bool, str]:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            current = repo.active_branch
            new_branch = repo.create_head(branch_name)
            return True, f"Created branch {branch_name}"
        except GitCommandError as e:
            return False, f"Error creating branch: {e}"
    return False, "Repository path does not exist"

def delete_branch(repo_path: str, branch_name: str) -> tuple[bool, str]:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            if branch_name == repo.active_branch.name:
                return False, "Cannot delete the currently active branch"
            repo.delete_head(branch_name)
            return True, f"Deleted branch {branch_name}"
        except GitCommandError as e:
            return False, f"Error deleting branch: {e}"
    return False, "Repository path does not exist"

def switch_branch(repo_path: str, branch_name: str) -> tuple[bool, str]:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            repo.git.checkout(branch_name)
            return True, f"Switched to branch {branch_name}"
        except GitCommandError as e:
            return False, f"Error switching branch: {e}"
    return False, "Repository path does not exist"