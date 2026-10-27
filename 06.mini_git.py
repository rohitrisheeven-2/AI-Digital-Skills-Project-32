"""
06. Mini-Git: Content-Addressable Version Control Simulator
Demonstrates how Git stores blobs, trees, and commit DAGs using SHA-1 hashing in memory/JSON.
"""

import hashlib
import time
from dataclasses import dataclass, field

@dataclass
class Commit:
    commit_hash: str
    parent_hash: str | None
    message: str
    timestamp: float
    snapshot: dict[str, str]  # filename -> blob_hash

class MiniGitRepository:
    def __init__(self):
        self.blobs: dict[str, str] = {}       # blob_hash -> content
        self.staging: dict[str, str] = {}     # filename -> blob_hash
        self.commits: dict[str, Commit] = {}  # commit_hash -> Commit
        self.head: str | None = None

    def _hash_object(self, data: str) -> str:
        return hashlib.sha1(data.encode("utf-8")).hexdigest()[:10]

    def add(self, filename: str, content: str):
        blob_hash = self._hash_object(content)
        self.blobs[blob_hash] = content
        self.staging[filename] = blob_hash
        print(f"Staged '{filename}' -> blob {blob_hash}")

    def commit(self, message: str) -> str:
        parent = self.head
        snapshot = dict(self.commits[parent].snapshot) if parent else {}
        snapshot.update(self.staging)
        self.staging.clear()

        raw_commit = f"{parent}|{message}|{time.time()}|{sorted(snapshot.items())}"
        c_hash = self._hash_object(raw_commit)
        self.commits[c_hash] = Commit(
            commit_hash=c_hash,
            parent_hash=parent,
            message=message,
            timestamp=time.time(),
            snapshot=snapshot
        )
        self.head = c_hash
        print(f"Created commit [{c_hash}]: {message}")
        return c_hash

    def log(self):
        curr = self.head
        print("\n=== Commit History (HEAD -> Root) ===")
        while curr:
            c = self.commits[curr]
            print(f"commit {c.commit_hash} (parent: {c.parent_hash})")
            print(f"    Message: {c.message}")
            print(f"    Files tracked: {list(c.snapshot.keys())}")
            curr = c.parent_hash

if __name__ == "__main__":
    repo = MiniGitRepository()
    repo.add("main.py", "print('Hello World v1')")
    repo.add("README.md", "# Project Repo")
    repo.commit("Initial commit with main.py and README")

    repo.add("main.py", "print('Hello World v2 - updated feature')")
    repo.add("utils.py", "def add(a, b): return a + b")
    repo.commit("Add utils.py and update main.py")
    repo.log()
