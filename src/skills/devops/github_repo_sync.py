"""
GitHub Repository Sync

Handles GitHub repository synchronization operations including:
- Clone repositories from GitHub
- Pull latest changes from remote
- Push local changes to remote
- Sync branches with remote
- Create pull requests
- Sync fork with upstream
"""

import os
import subprocess
import re
import json
import urllib.parse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CloneResult:
    """Result of clone operation."""

    repo_url: str = ""
    local_path: str = ""
    branch: str = "main"
    success: bool = False
    message: str = ""


@dataclass
class PullResult:
    """Result of pull operation."""

    local_path: str = ""
    branch: str = ""
    files_updated: int = 0
    success: bool = False
    message: str = ""


@dataclass
class PushResult:
    """Result of push operation."""

    local_path: str = ""
    branch: str = ""
    commits_pushed: int = 0
    success: bool = False
    message: str = ""


@dataclass
class SyncBranchResult:
    """Result of branch sync operation."""

    local_path: str = ""
    branch: str = ""
    upstream_branch: str = ""
    success: bool = False
    message: str = ""


@dataclass
class CreatePRResult:
    """Result of PR creation."""

    repo_path: str = ""
    title: str = ""
    head_branch: str = ""
    base_branch: str = ""
    pr_url: str = ""
    success: bool = False
    message: str = ""


@dataclass
class SyncForkResult:
    """Result of fork sync operation."""

    local_path: str = ""
    upstream_url: str = ""
    branches_synced: List[str] = field(default_factory=list)
    success: bool = False
    message: str = ""


def run_git_command(
    repo_path: str, args: List[str], capture_output: bool = True
) -> subprocess.CompletedProcess:
    """Execute a git command in the repository."""
    cmd = ["git"] + args
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=capture_output,
        text=True,
        shell=False,
    )
    return result


def parse_github_url(url: str) -> Dict[str, str]:
    """Parse GitHub URL to extract owner and repo."""
    parsed = {
        "owner": "",
        "repo": "",
        "is_github": False,
    }

    url = url.strip().rstrip("/")

    https_pattern = r"https?://github\.com/([^/]+)/([^/.]+)(?:\.git)?/?$"
    ssh_pattern = r"git@github\.com:([^/]+)/([^/.]+)(?:\.git)?/?$"

    match = re.match(https_pattern, url)
    if match:
        parsed["owner"] = match.group(1)
        parsed["repo"] = match.group(2)
        parsed["is_github"] = True
        return parsed

    match = re.match(ssh_pattern, url)
    if match:
        parsed["owner"] = match.group(1)
        parsed["repo"] = match.group(2)
        parsed["is_github"] = True
        return parsed

    return parsed


def clone_repo(repo_path: str, options: dict) -> CloneResult:
    """Clone a repository from GitHub."""
    result = CloneResult()

    repo_url = options.get("url", "")
    if not repo_url:
        repo_url = repo_path

    branch = options.get("branch", "main")
    depth = options.get("depth")
    recursive = options.get("recursive", True)

    if not repo_url:
        result.message = "No repository URL provided"
        return result

    parsed = parse_github_url(repo_url)
    if not parsed["is_github"]:
        result.message = f"Invalid GitHub URL: {repo_url}"
        return result

    target_dir = options.get("target_dir", os.path.basename(parsed["repo"]))
    if not os.path.isabs(target_dir):
        target_dir = os.path.join(os.getcwd(), target_dir)

    clone_args = ["clone"]

    if depth:
        clone_args.extend(["--depth", str(depth)])

    if branch:
        clone_args.extend(["--branch", branch])

    if not recursive:
        clone_args.append("--no-recursive")

    clone_args.append(repo_url)
    clone_args.append(target_dir)

    try:
        cmd_result = subprocess.run(
            clone_args,
            capture_output=True,
            text=True,
            shell=False,
        )

        if cmd_result.returncode == 0:
            result.success = True
            result.repo_url = repo_url
            result.local_path = target_dir
            result.branch = branch
            result.message = f"Successfully cloned {repo_url} to {target_dir}"
        else:
            result.message = cmd_result.stderr.strip() or "Clone failed"

    except Exception as e:
        result.message = f"Clone error: {str(e)}"

    return result


def pull_changes(repo_path: str, options: dict) -> PullResult:
    """Pull latest changes from remote."""
    result = PullResult()

    if not os.path.exists(repo_path):
        result.message = f"Repository path does not exist: {repo_path}"
        return result

    if not os.path.exists(os.path.join(repo_path, ".git")):
        result.message = f"Not a git repository: {repo_path}"
        return result

    branch = options.get("branch")
    rebase = options.get("rebase", False)

    pull_args = ["pull"]
    if rebase:
        pull_args.append("--rebase")

    remote = options.get("remote", "origin")
    pull_args.append(remote)

    if branch:
        pull_args.append(branch)

    cmd_result = run_git_command(repo_path, pull_args)

    result.local_path = repo_path

    if cmd_result.returncode == 0:
        result.success = True
        output = cmd_result.stdout

        files_match = re.search(r"(\d+) file changed", output)
        if files_match:
            result.files_updated = int(files_match.group(1))

        current_branch = run_git_command(repo_path, ["branch", "--show-current"])
        result.branch = (
            current_branch.stdout.strip()
            if current_branch.returncode == 0
            else branch or "unknown"
        )

        result.message = f"Successfully pulled changes from {remote}"
    else:
        result.message = cmd_result.stderr.strip() or "Pull failed"

    return result


def push_changes(repo_path: str, options: dict) -> PushResult:
    """Push local changes to remote."""
    result = PushResult()

    if not os.path.exists(repo_path):
        result.message = f"Repository path does not exist: {repo_path}"
        return result

    if not os.path.exists(os.path.join(repo_path, ".git")):
        result.message = f"Not a git repository: {repo_path}"
        return result

    branch = options.get("branch")
    remote = options.get("remote", "origin")
    force = options.get("force", False)
    tags = options.get("tags", False)

    push_args = ["push"]
    if force:
        push_args.append("--force")
    if tags:
        push_args.append("--tags")

    push_args.append(remote)

    if branch:
        push_args.append(branch)

    cmd_result = run_git_command(repo_path, push_args)

    result.local_path = repo_path

    if branch:
        result.branch = branch
    else:
        current_branch = run_git_command(repo_path, ["branch", "--show-current"])
        result.branch = (
            current_branch.stdout.strip()
            if current_branch.returncode == 0
            else "unknown"
        )

    if cmd_result.returncode == 0:
        result.success = True
        output = cmd_result.stdout

        commits_match = re.search(r"(\d+) commit", output)
        if commits_match:
            result.commits_pushed = int(commits_match.group(1))

        result.message = f"Successfully pushed to {remote}/{result.branch}"
    else:
        result.message = cmd_result.stderr.strip() or "Push failed"

    return result


def sync_branch(repo_path: str, options: dict) -> SyncBranchResult:
    """Sync a branch with its remote counterpart."""
    result = SyncBranchResult()

    if not os.path.exists(repo_path):
        result.message = f"Repository path does not exist: {repo_path}"
        return result

    if not os.path.exists(os.path.join(repo_path, ".git")):
        result.message = f"Not a git repository: {repo_path}"
        return result

    branch = options.get("branch")
    remote = options.get("remote", "origin")
    upstream = options.get("upstream")

    if not branch:
        current_branch = run_git_command(repo_path, ["branch", "--show-current"])
        if current_branch.returncode == 0:
            branch = current_branch.stdout.strip()
        else:
            result.message = "Could not determine current branch"
            return result

    result.local_path = repo_path
    result.branch = branch

    if upstream:
        result.upstream_branch = upstream
    else:
        result.upstream_branch = f"{remote}/{branch}"

    fetch_result = run_git_command(repo_path, ["fetch", remote, branch])
    if fetch_result.returncode != 0:
        result.message = (
            f"Failed to fetch {remote}/{branch}: {fetch_result.stderr.strip()}"
        )
        return result

    if options.get("rebase", False):
        sync_args = ["rebase", f"{remote}/{branch}"]
    else:
        sync_args = ["merge", f"{remote}/{branch}"]

    merge_result = run_git_command(repo_path, sync_args)

    if merge_result.returncode == 0:
        result.success = True
        result.message = f"Successfully synced {branch} with {result.upstream_branch}"
    else:
        if "Already up to date" in merge_result.stdout:
            result.success = True
            result.message = (
                f"{branch} is already up to date with {result.upstream_branch}"
            )
        else:
            result.message = merge_result.stderr.strip() or "Sync failed"

    return result


def create_pull_request(repo_path: str, options: dict) -> CreatePRResult:
    """Create a pull request using gh CLI."""
    result = CreatePRResult()

    if not os.path.exists(repo_path):
        result.message = f"Repository path does not exist: {repo_path}"
        return result

    if not os.path.exists(os.path.join(repo_path, ".git")):
        result.message = f"Not a git repository: {repo_path}"
        return result

    title = options.get("title", "")
    body = options.get("body", "")
    head_branch = options.get("head_branch", "")
    base_branch = options.get("base_branch", "main")
    draft = options.get("draft", False)

    if not head_branch:
        current_branch = run_git_command(repo_path, ["branch", "--show-current"])
        if current_branch.returncode == 0:
            head_branch = current_branch.stdout.strip()
        else:
            result.message = "Could not determine current branch"
            return result

    if not title:
        result.message = "PR title is required"
        return result

    gh_result = subprocess.run(
        ["gh", "pr", "create", "--base", base_branch, "--head", head_branch],
        capture_output=True,
        text=True,
        cwd=repo_path,
        shell=False,
    )

    result.repo_path = repo_path
    result.title = title
    result.head_branch = head_branch
    result.base_branch = base_branch

    if gh_result.returncode == 0:
        pr_url = gh_result.stdout.strip()
        result.success = True
        result.pr_url = pr_url
        result.message = f"Successfully created PR: {pr_url}"
    else:
        error_msg = gh_result.stderr.strip()
        if "gh: command not found" in error_msg or "gh: not found" in error_msg.lower():
            result.message = "GitHub CLI (gh) is not installed"
        else:
            result.message = error_msg or "Failed to create PR"

    return result


@dataclass
class StatusResult:
    """Result of status check."""

    local_path: str = ""
    current_branch: str = ""
    has_remote: bool = False
    remote_url: str = ""
    uncommitted_changes: int = 0
    untracked_files: int = 0
    ahead: int = 0
    behind: int = 0
    success: bool = False
    message: str = ""


def get_repo_status(repo_path: str) -> StatusResult:
    """Get repository status."""
    result = StatusResult()
    result.local_path = repo_path

    if not os.path.exists(repo_path):
        result.message = f"Repository path does not exist: {repo_path}"
        return result

    if not os.path.exists(os.path.join(repo_path, ".git")):
        result.message = f"Not a git repository: {repo_path}"
        return result

    try:
        # Get current branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        if branch_result.returncode == 0:
            result.current_branch = branch_result.stdout.strip()

        # Get remote info
        remote_result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        if remote_result.returncode == 0:
            result.has_remote = True
            result.remote_url = remote_result.stdout.strip()

        # Get uncommitted changes
        diff_result = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        if diff_result.returncode == 0:
            result.uncommitted_changes = len(
                [l for l in diff_result.stdout.strip().split("\n") if l]
            )

        # Get untracked files
        untracked_result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        if untracked_result.returncode == 0:
            result.untracked_files = len(
                [l for l in untracked_result.stdout.strip().split("\n") if l]
            )

        # Get ahead/behind
        if result.has_remote:
            rev_result = subprocess.run(
                [
                    "git",
                    "rev-list",
                    "--left-right",
                    "--count",
                    f"origin/{result.current_branch}...{result.current_branch}",
                ],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            if rev_result.returncode == 0:
                parts = rev_result.stdout.strip().split()
                if len(parts) == 2:
                    result.behind = int(parts[0])
                    result.ahead = int(parts[1])

        result.success = True
        result.message = f"Repository status: {result.current_branch}"
        if result.uncommitted_changes > 0:
            result.message += f", {result.uncommitted_changes} uncommitted"
        if result.untracked_files > 0:
            result.message += f", {result.untracked_files} untracked"

    except Exception as e:
        result.message = f"Error getting status: {str(e)}"

    return result


def sync_fork(repo_path: str, options: dict) -> SyncForkResult:
    """Sync a fork with its upstream repository."""
    result = SyncForkResult()

    if not os.path.exists(repo_path):
        result.message = f"Repository path does not exist: {repo_path}"
        return result

    if not os.path.exists(os.path.join(repo_path, ".git")):
        result.message = f"Not a git repository: {repo_path}"
        return result

    upstream_url = options.get("upstream_url")
    branches = options.get("branches", ["main", "master"])
    sync_method = options.get("sync_method", "merge")

    result.local_path = repo_path

    if upstream_url:
        add_upstream_result = run_git_command(
            repo_path, ["remote", "add", "upstream", upstream_url]
        )
        if (
            add_upstream_result.returncode != 0
            and "already exists" not in add_upstream_result.stderr
        ):
            result.message = (
                f"Failed to add upstream: {add_upstream_result.stderr.strip()}"
            )
            return result
        result.upstream_url = upstream_url
    else:
        result.upstream_url = "origin"

    fetch_result = run_git_command(repo_path, ["fetch", "upstream"])
    if fetch_result.returncode != 0:
        result.message = f"Failed to fetch upstream: {fetch_result.stderr.strip()}"
        return result

    synced_branches = []

    for branch in branches:
        branch_result = run_git_command(repo_path, ["checkout", branch])
        if branch_result.returncode != 0:
            continue

        if sync_method == "rebase":
            sync_result = run_git_command(repo_path, ["rebase", f"upstream/{branch}"])
        else:
            sync_result = run_git_command(repo_path, ["merge", f"upstream/{branch}"])

        if sync_result.returncode == 0:
            synced_branches.append(branch)

    result.branches_synced = synced_branches

    if synced_branches:
        result.success = True
        result.message = f"Successfully synced {len(synced_branches)} branches: {', '.join(synced_branches)}"
    else:
        result.message = "No branches were synced"

    return result


def github_repo_sync(repo_path: str, action: str, options: dict = None) -> dict:
    """
    Main function for GitHub repository synchronization operations.

    Args:
        repo_path: Local repo path or GitHub URL
        action: Action to perform (clone, pull, push, sync_branch, create_pr, sync_fork)
        options: Action-specific options

    Returns:
        dict with status, action, results, and summary
    """
    if options is None:
        options = {}

    supported_actions = [
        "clone",
        "pull",
        "push",
        "sync_branch",
        "create_pr",
        "sync_fork",
        "status",
    ]

    if action not in supported_actions:
        return {
            "status": "error",
            "action": action,
            "results": {},
            "summary": f"Unknown action: {action}. Supported actions: {', '.join(supported_actions)}",
        }

    try:
        if action == "clone":
            clone_result = clone_repo(repo_path, options)
            return {
                "status": "success" if clone_result.success else "error",
                "action": action,
                "results": {
                    "repo_url": clone_result.repo_url,
                    "local_path": clone_result.local_path,
                    "branch": clone_result.branch,
                },
                "summary": clone_result.message,
            }

        elif action == "pull":
            pull_result = pull_changes(repo_path, options)
            return {
                "status": "success" if pull_result.success else "error",
                "action": action,
                "results": {
                    "local_path": pull_result.local_path,
                    "branch": pull_result.branch,
                    "files_updated": pull_result.files_updated,
                },
                "summary": pull_result.message,
            }

        elif action == "push":
            push_result = push_changes(repo_path, options)
            return {
                "status": "success" if push_result.success else "error",
                "action": action,
                "results": {
                    "local_path": push_result.local_path,
                    "branch": push_result.branch,
                    "commits_pushed": push_result.commits_pushed,
                },
                "summary": push_result.message,
            }

        elif action == "sync_branch":
            sync_result = sync_branch(repo_path, options)
            return {
                "status": "success" if sync_result.success else "error",
                "action": action,
                "results": {
                    "local_path": sync_result.local_path,
                    "branch": sync_result.branch,
                    "upstream_branch": sync_result.upstream_branch,
                },
                "summary": sync_result.message,
            }

        elif action == "create_pr":
            pr_result = create_pull_request(repo_path, options)
            return {
                "status": "success" if pr_result.success else "error",
                "action": action,
                "results": {
                    "repo_path": pr_result.repo_path,
                    "title": pr_result.title,
                    "head_branch": pr_result.head_branch,
                    "base_branch": pr_result.base_branch,
                    "pr_url": pr_result.pr_url,
                },
                "summary": pr_result.message,
            }

        elif action == "sync_fork":
            fork_result = sync_fork(repo_path, options)
            return {
                "status": "success" if fork_result.success else "error",
                "action": action,
                "results": {
                    "local_path": fork_result.local_path,
                    "upstream_url": fork_result.upstream_url,
                    "branches_synced": fork_result.branches_synced,
                },
                "summary": fork_result.message,
            }

        elif action == "status":
            status_result = get_repo_status(repo_path)
            return {
                "status": "success" if status_result.success else "error",
                "action": action,
                "results": {
                    "current_branch": status_result.current_branch,
                    "has_remote": status_result.has_remote,
                    "remote_url": status_result.remote_url,
                    "uncommitted_changes": status_result.uncommitted_changes,
                    "untracked_files": status_result.untracked_files,
                    "ahead": status_result.ahead,
                    "behind": status_result.behind,
                },
                "summary": status_result.message,
            }

    except Exception as e:
        return {
            "status": "error",
            "action": action,
            "results": {},
            "summary": f"Error performing {action}: {str(e)}",
        }


def invoke(payload: dict) -> dict:
    """MCP skill invocation."""
    repo_path = payload.get("repo_path", "")
    action = payload.get("action", "")
    options = payload.get("options", {})

    if not repo_path:
        return {
            "status": "error",
            "action": action,
            "results": {},
            "summary": "No repository path or URL provided",
        }

    if not action:
        return {
            "status": "error",
            "action": action,
            "results": {},
            "summary": "No action provided",
        }

    result = github_repo_sync(repo_path, action, options)
    return result


def register_skill():
    """Return skill metadata."""
    return {
        "name": "github-repo-sync",
        "description": "Handles GitHub repository synchronization operations including cloning, pulling, pushing, branch syncing, PR creation, and fork syncing",
        "version": "1.0.0",
        "domain": "DEVOPS",
    }
