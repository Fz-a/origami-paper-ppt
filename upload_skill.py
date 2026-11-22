"""Upload an already-reviewed Codex skill folder to a GitHub repository.

Usage: python upload_skill.py SKILL_DIRECTORY --package-dir PACKAGE_DIRECTORY --repo OWNER/REPO
Authentication: GITHUB_TOKEN or GH_TOKEN environment variable.
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


FILES = ("SKILL.md", "README.md", "LICENSE", ".gitignore", "assets/origami-template.pptx", "upload_skill.py")


def credential():
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        return token
    raise RuntimeError("No GitHub token found. Set GITHUB_TOKEN or GH_TOKEN.")


def request(method, url, token, payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url, data=body, method=method,
        headers={"Accept": "application/vnd.github+json",
                 "Authorization": f"Bearer {token}",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404 and method == "GET":
            return None
        raise RuntimeError(f"GitHub API returned HTTP {exc.code} for {url}") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--package-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--repo", required=True, help="OWNER/REPO")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.skill_dir.resolve()
    package = args.package_dir.resolve()
    files = {}
    for relative in FILES:
        path = (root if relative in ("SKILL.md", "assets/origami-template.pptx") else package) / relative
        if not path.is_file():
            parser.error(f"Missing file: {path}")
        files[relative] = path.read_bytes()
    print("Files selected:", ", ".join(FILES))
    if args.dry_run:
        return
    token = credential()
    api = f"https://api.github.com/repos/{args.repo}/contents"
    for relative, data in files.items():
        url = f"{api}/{relative}"
        existing = request("GET", f"{url}?ref={args.branch}", token)
        payload = {"message": f"Update {relative}", "branch": args.branch,
                   "content": base64.b64encode(data).decode("ascii")}
        if existing:
            payload["sha"] = existing["sha"]
        request("PUT", url, token, payload)
        print("Uploaded", relative)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Upload failed: {exc}", file=sys.stderr)
        raise SystemExit(1)