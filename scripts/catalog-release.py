#!/usr/bin/env python3
"""Build a version-only release from trusted main; never push or merge main."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

LISTS = tuple(f"community-app-catalog/{name}.json" for name in
              ("Nintendo", "PlayStation", "Xbox", "OtherPlatforms"))
STATE = ".github/catalog-release-state.json"
BRANCH = "codex/catalog-release"
REPO = "tgeorgiadis/quiver-community-app-catalog"


def run(*args, input=None):
    return subprocess.run(args, input=input, text=True, capture_output=True, check=True).stdout.strip()


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError("Expected a numeric major.minor.patch version")
    return tuple(map(int, value.split(".")))


def fingerprint(doc):
    content = {key: value for key, value in doc.items() if key != "version"}
    return hashlib.sha256(json.dumps(content, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True).encode()).hexdigest()


def snapshot(docs):
    return {path: {"version": doc["version"], "sha256": fingerprint(doc)}
            for path, doc in docs.items()}


def plan(docs, released):
    if set(docs) != set(LISTS) or set(released) != set(LISTS):
        raise ValueError("Unexpected catalog lists in release state")
    updates = {}
    for path in LISTS:
        doc, previous = docs[path], released[path]
        current, old = version(doc["version"]), version(previous["version"])
        if current < old:
            raise ValueError(f"Version went backwards: {path}")
        if fingerprint(doc) != previous["sha256"]:
            updates[path] = ".".join(map(str, (current[0], current[1], current[2] + 1)))
        elif current > old:
            # Permit an intentional version-only release. The fingerprint excludes
            # version, so the release state records the requested version.
            updates[path] = doc["version"]
    result = {path: {**doc, "version": updates.get(path, doc["version"])}
              for path, doc in docs.items()}
    return updates, snapshot(result)


def read_docs(root):
    return {path: json.loads((root / path).read_text(encoding="utf-8")) for path in LISTS}


def write_plan(root):
    docs = read_docs(root)
    released = json.loads((root / STATE).read_text(encoding="utf-8"))
    updates, state = plan(docs, released)
    for path, target in updates.items():
        file = root / path
        raw = file.read_text(encoding="utf-8")
        # Change only the top-level version line, preserving all catalog formatting.
        raw, count = re.subn(r'^  "version": "[0-9.]+",$',
                             f'  "version": "{target}",', raw, flags=re.MULTILINE)
        if count != 1:
            raise ValueError(f"Expected exactly one top-level version line: {path}")
        file.write_text(raw, encoding="utf-8", newline="\n")
    (root / STATE).write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return updates, state != released


def validate(base, head):
    docs = read_docs(base)
    released = json.loads((base / STATE).read_text(encoding="utf-8"))
    updates, expected_state = plan(docs, released)
    actual = read_docs(head)
    for path in LISTS:
        if actual[path] != {**docs[path], "version": updates.get(path, docs[path]["version"])}:
            raise ValueError(f"Release must only apply the expected version bump: {path}")
    if json.loads((head / STATE).read_text(encoding="utf-8")) != expected_state:
        raise ValueError("Release state must match the catalog contents being versioned")
    if expected_state == released:
        raise ValueError("No unreleased catalog changes")
    def tracked(root):
        return {p: (root / p).read_bytes() for p in run("git", "-C", str(root), "ls-files").splitlines()}
    before, after = tracked(base), tracked(head)
    changed = {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
    if not changed <= set(LISTS) | {STATE}:
        raise ValueError("Release changed files outside the version lists and release state")


def publish():
    # The workflow checks out trusted main, never a PR checkout with a write token.
    if run("gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner") != REPO:
        raise ValueError("Release publication is restricted to the real catalog repository")
    run("git", "fetch", "origin", "main")
    base = run("git", "rev-parse", "origin/main")
    run("git", "checkout", "-B", BRANCH, base)
    previous = run("git", "ls-remote", "origin", f"refs/heads/{BRANCH}")
    old_head = previous.split()[0] if previous else ""
    updates, changed = write_plan(Path.cwd())
    if not changed:
        print("No unreleased catalog changes.")
        return
    run("python3", "scripts/validate-json.py", *LISTS, STATE)
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run("git", "add", "--", *LISTS, STATE)
    tree = run("git", "write-tree")
    if old_head:
        run("git", "fetch", "origin", BRANCH)
    unchanged = old_head and run("git", "rev-parse", f"{old_head}^{{tree}}") == tree
    if not unchanged:
        run("git", "commit", "-m", "Release catalog list updates")
    # If main advanced while preparing, let the queued next run recompute safely.
    if run("git", "ls-remote", "origin", "refs/heads/main").split()[0] != base:
        raise ValueError("Main advanced during preparation; rerun the release workflow")
    if not unchanged:
        run("git", "push", f"--force-with-lease=refs/heads/{BRANCH}:{old_head}",
            "origin", f"HEAD:refs/heads/{BRANCH}")
    body = ("Batches version bumps for catalog changes already merged into main.\n\n" +
            "\n".join(f"- `{path}`: `{target}`" for path, target in updates.items()) +
            "\n\nMerge this PR manually when the batch is ready. This PR is refreshed as more "
            "catalog changes merge; review the latest diff before merging. "
            "If GitHub requests approval to run validation, approve the workflows first. "
            "No apps or platform metadata are changed by this PR.\n")
    prs = json.loads(run("gh", "pr", "list", "--repo", REPO, "--head", BRANCH,
                         "--base", "main", "--state", "open", "--json", "number"))
    if prs:
        run("gh", "pr", "edit", str(prs[0]["number"]), "--repo", REPO,
            "--title", "Release catalog updates", "--body-file", "-", input=body)
    else:
        print(run("gh", "pr", "create", "--repo", REPO, "--head", BRANCH,
                  "--base", "main", "--title", "Release catalog updates", "--body-file", "-", input=body))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "publish", "validate"))
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    if args.command == "publish":
        publish()
    elif args.command == "validate":
        validate(*(Path(p) for p in args.paths))
    else:
        print(write_plan(Path.cwd()))
