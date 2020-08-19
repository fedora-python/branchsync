branchsync 🪄
=============

Synces (and creates) backport branches of your src.fp.o Python Pull Requests.

Given the src.fp.o's fork username and branch,
this tool creates new branches when needed and gives you links to open new
src.fp.o pull requests.

Can be used repeatedly when the branch was updated.

Needs recent [ferrypick](https://github.com/fedora-python/ferrypick).

Example (only the first command is actually run by the user):

```
$ ./branchsync.py python3.6 update-to-3-6-12 thrnciar
$ whoami
churchyard
$ git clone ssh://pkgs.fedoraproject.org/rpms/python3.6.git python3.6
Cloning into 'python3.6'...
remote: Enumerating objects: 1922, done.
remote: Counting objects: 100% (1922/1922), done.
remote: Compressing objects: 100% (791/791), done.
remote: Total 1922 (delta 1188), reused 1855 (delta 1123)
Receiving objects: 100% (1922/1922), 1.18 MiB | 1.87 MiB/s, done.
Resolving deltas: 100% (1188/1188), done.
$ git remote add new ssh://pkgs.fedoraproject.org/forks/thrnciar/rpms/python3.6.git --fetch
From ssh://pkgs.fedoraproject.org/forks/thrnciar/rpms/python3.6
 * [new branch]      f33              -> new/f33
 * [new branch]      master           -> new/master
 * [new branch]      update-to-3-6-12 -> new/update-to-3-6-12
Updating new
$ git remote add backport ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python3.6.git
$ git remote -v
backport	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python3.6.git (fetch)
backport	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python3.6.git (push)
new	ssh://pkgs.fedoraproject.org/forks/thrnciar/rpms/python3.6.git (fetch)
new	ssh://pkgs.fedoraproject.org/forks/thrnciar/rpms/python3.6.git (push)
origin	ssh://pkgs.fedoraproject.org/rpms/python3.6.git (fetch)
origin	ssh://pkgs.fedoraproject.org/rpms/python3.6.git (push)
$ git switch --track new/update-to-3-6-12
Switched to a new branch 'update-to-3-6-12'
Branch 'update-to-3-6-12' set up to track remote branch 'update-to-3-6-12' from 'new'.
$ git merge-base --is-ancestor origin/f33 update-to-3-6-12
https://src.fedoraproject.org/fork/thrnciar/rpms/python3.6/diff/f33..update-to-3-6-12
$ git remote add origin-f32 ssh://pkgs.fedoraproject.org/rpms/python36.git --fetch
remote: Enumerating objects: 420, done.
remote: Counting objects: 100% (381/381), done.
remote: Compressing objects: 100% (195/195), done.
remote: Total 339 (delta 208), reused 257 (delta 139)
Receiving objects: 100% (339/339), 125.11 KiB | 585.00 KiB/s, done.
Resolving deltas: 100% (208/208), completed with 23 local objects.
From ssh://pkgs.fedoraproject.org/rpms/python36
 * [new branch]      el6        -> origin-f32/el6
 * [new branch]      epel7      -> origin-f32/epel7
 * [new branch]      f24        -> origin-f32/f24
 * [new branch]      f25        -> origin-f32/f25
 * [new branch]      f27        -> origin-f32/f27
 * [new branch]      f29        -> origin-f32/f29
 * [new branch]      f30        -> origin-f32/f30
 * [new branch]      f31        -> origin-f32/f31
 * [new branch]      f32        -> origin-f32/f32
 * [new branch]      master     -> origin-f32/master
Updating origin-f32
$ git remote add backport-f32 ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python36.git
$ git remote -v
backport	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python3.6.git (fetch)
backport	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python3.6.git (push)
backport-f32	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python36.git (fetch)
backport-f32	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python36.git (push)
new	ssh://pkgs.fedoraproject.org/forks/thrnciar/rpms/python3.6.git (fetch)
new	ssh://pkgs.fedoraproject.org/forks/thrnciar/rpms/python3.6.git (push)
origin	ssh://pkgs.fedoraproject.org/rpms/python3.6.git (fetch)
origin	ssh://pkgs.fedoraproject.org/rpms/python3.6.git (push)
origin-f32	ssh://pkgs.fedoraproject.org/rpms/python36.git (fetch)
origin-f32	ssh://pkgs.fedoraproject.org/rpms/python36.git (push)
$ git merge-base --is-ancestor origin-f32/f32 update-to-3-6-12
$ git format-patch origin/master
$ fedpkg --name python3.6 sources
Downloading Python-3.6.12.tar.xz

Downloading Python-3.6.12.tar.xz.asc
$ fedpkg --name python36 new-sources Python-3.6.12.tar.xz Python-3.6.12.tar.xz.asc
File already uploaded: Python-3.6.12.tar.xz
File already uploaded: Python-3.6.12.tar.xz.asc
Source upload succeeded. Don't forget to commit the sources file
$ git switch --track origin-f32/f32
Switched to a new branch 'f32'
Branch 'f32' set up to track remote branch 'f32' from 'origin-f32'.
$ git switch -c f32-auto-thrnciar-update-to-3-6-12
Switched to a new branch 'f32-auto-thrnciar-update-to-3-6-12'
$ git push --force -u backport-f32 f32-auto-thrnciar-update-to-3-6-12
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (5/5), 824 bytes | 824.00 KiB/s, done.
Total 5 (delta 3), reused 4 (delta 2), pack-reused 0
remote: Sending to redis to log activity and send commit notification emails
remote: * Publishing information for 1 commits
remote:   - to fedora-message
remote: 
remote: Create a pull-request for f32-auto-thrnciar-update-to-3-6-12
remote:    https://src.fedoraproject.org/fork/churchyard/rpms/python36/diff/master..f32-auto-thrnciar-update-to-3-6-12
remote: 
To ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python36.git
 + 519ea4d...79109b1 f32-auto-thrnciar-update-to-3-6-12 -> f32-auto-thrnciar-update-to-3-6-12 (forced update)
Branch 'f32-auto-thrnciar-update-to-3-6-12' set up to track remote branch 'f32-auto-thrnciar-update-to-3-6-12' from 'backport-f32'.
$ git switch update-to-3-6-12
Switched to branch 'update-to-3-6-12'
Your branch is up to date with 'new/update-to-3-6-12'.
https://src.fedoraproject.org/fork/churchyard/rpms/python36/diff/f32..f32-auto-thrnciar-update-to-3-6-12
$ git remote add origin-f31 ssh://pkgs.fedoraproject.org/rpms/python36.git --fetch
From ssh://pkgs.fedoraproject.org/rpms/python36
 * [new branch]      el6        -> origin-f31/el6
 * [new branch]      epel7      -> origin-f31/epel7
 * [new branch]      f24        -> origin-f31/f24
 * [new branch]      f25        -> origin-f31/f25
 * [new branch]      f27        -> origin-f31/f27
 * [new branch]      f29        -> origin-f31/f29
 * [new branch]      f30        -> origin-f31/f30
 * [new branch]      f31        -> origin-f31/f31
 * [new branch]      f32        -> origin-f31/f32
 * [new branch]      master     -> origin-f31/master
Updating origin-f31
$ git remote add backport-f31 ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python36.git
$ git remote -v
backport	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python3.6.git (fetch)
backport	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python3.6.git (push)
backport-f31	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python36.git (fetch)
backport-f31	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python36.git (push)
backport-f32	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python36.git (fetch)
backport-f32	ssh://pkgs.fedoraproject.org/forks/churchyard/rpms/python36.git (push)
new	ssh://pkgs.fedoraproject.org/forks/thrnciar/rpms/python3.6.git (fetch)
new	ssh://pkgs.fedoraproject.org/forks/thrnciar/rpms/python3.6.git (push)
origin	ssh://pkgs.fedoraproject.org/rpms/python3.6.git (fetch)
origin	ssh://pkgs.fedoraproject.org/rpms/python3.6.git (push)
origin-f31	ssh://pkgs.fedoraproject.org/rpms/python36.git (fetch)
origin-f31	ssh://pkgs.fedoraproject.org/rpms/python36.git (push)
origin-f32	ssh://pkgs.fedoraproject.org/rpms/python36.git (fetch)
origin-f32	ssh://pkgs.fedoraproject.org/rpms/python36.git (push)
$ git merge-base --is-ancestor origin-f31/f31 f32-auto-thrnciar-update-to-3-6-12
https://src.fedoraproject.org/fork/thrnciar/rpms/python36/diff/f31..f32-auto-thrnciar-update-to-3-6-12
```

The output looks very verbose, but there are colors to guide you.

TODO
----

- fork the repo if needed
- read the initial branch info from src.fp.o
- create the new PRs on src.fp.o

Caution
-------

This force pushes to `<fedora_branch>-auto-<original_username>-<original_branch>`
(e.g. `f32-auto-thrnciar-update-to-3-6-12`) into your fork without looking.
This can erase data, you have been warned.
