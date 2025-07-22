import os
from git import Repo, GitCommandError # type: ignore

#TODO make the print statements go to the ui interface

def clone_repo(repo_url: str, destination: str) -> None:
    if not os.path.exists(destination):
        try:
            Repo.clone_from(repo_url, destination)
            print(f"Repository cloned to {destination}")
        except GitCommandError as e:
            print(f"Error cloning repository: {e}")
    else:
        print(f"Destination {destination} already exists. Skipping clone.")

def pull_from_repo(repo_path: str) -> None:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            origin = repo.remotes.origin
            origin.pull()
            print("Sucessfulle pulled.")
        except GitCommandError as e:
            print(f"Error pulling from repository: {e}")
    else:
        print(f"Repository path {repo_path} does not exist.")

def add_changes(repo_path: str, files: list) -> None:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            repo.index.add(files)
            print(f"Added changes for files: {files}")
        except GitCommandError as e:
            print(f"Error adding changes: {e}")
    else:
        print(f"Repository path {repo_path} does not exist.")

def commit_changes(repo_path: str, message: str) -> None:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            repo.index.commit(message)
            print("Changes committed.")
        except GitCommandError as e:
            print(f"Error committing changes: {e}")
    else:
        print(f"Repository path {repo_path} does not exist.")

def push_to_repo(repo_path: str) -> None:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            origin = repo.remotes.origin
            origin.push()
            print("Changes pushed to remote repository.")
        except GitCommandError as e:
            print(f"Error pushing to repository: {e}")
    else:
        print(f"Repository path {repo_path} does not exist.")

def get_repo_status(repo_path: str) -> None:
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            status = repo.git.status()
            print("Repository status:")
            print(status)
        except GitCommandError as e:
            print(f"Error getting repository status: {e}")
    else:
        print(f"Repository path {repo_path} does not exist.")