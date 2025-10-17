import os
import sys
from typing import Dict
import click
from leetcode_api import LeetCodeClient
from github_api import GitHubClient


@click.group()
def cli() -> None:
    """LeetCode-GitHub Auto Sync CLI."""


def _read_required_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        click.echo(f"Missing required environment variable: {var_name}", err=True)
        sys.exit(1)
    return value


def _language_extension_map() -> Dict[str, str]:
    return {
        "python": "py",
        "python3": "py",
        "cpp": "cpp",
        "java": "java",
        "javascript": "js",
        "typescript": "ts",
        "c": "c",
        "csharp": "cs",
        "go": "go",
        "ruby": "rb",
        "swift": "swift",
        "kotlin": "kt",
        "rust": "rs",
        "scala": "scala",
        "mysql": "sql",
    }


@cli.command()
@click.option("--limit", default=20, show_default=True, help="Fetch last N accepted submissions")
@click.option("--dry-run", is_flag=True, default=False, help="Do not push changes, only print actions")
def sync(limit: int, dry_run: bool) -> None:
    """Run synchronization using environment variables."""
    lc_session = _read_required_env("LC_SESSION")
    lc_csrf = _read_required_env("LC_CSRF")
    github_pat = _read_required_env("GITHUB_PAT")
    gh_owner = _read_required_env("GH_OWNER")
    gh_repo = _read_required_env("GH_REPO")

    lc = LeetCodeClient(lc_session, lc_csrf)
    gh = GitHubClient(github_pat, gh_owner, gh_repo)

    submissions = lc.fetch_accepted_submissions(limit=limit)
    ext_map = _language_extension_map()

    changed = 0
    for sub in submissions:
        sub_id = sub["id"]
        code, lang, title_slug, difficulty = lc.get_submission_details(sub_id)
        ext = ext_map.get(lang, lang or "txt")
        rel_path = f"solutions/{difficulty}/{title_slug}.{ext}"

        existing_sha = gh.get_file_sha(rel_path)
        commit_message = f"sync: {title_slug} ({difficulty}) via LeetCode Auto Sync"

        if dry_run:
            click.echo(f"Would sync {rel_path} (existing_sha={existing_sha})")
            changed += 1
            continue

        gh.create_or_update_file(rel_path, code.encode("utf-8"), commit_message, sha=existing_sha)
        click.echo(f"Synced {rel_path}")
        changed += 1

    click.echo(f"Done. {changed} file(s) processed.")


if __name__ == "__main__":
    cli()


