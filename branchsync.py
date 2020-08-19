#!/usr/bin/env python3

import contextlib
import os
import shlex
import sys
import subprocess
import tempfile


# Branhes to backport to, in order from master, without master
FBRANCHES = ['f33', 'f32', 'f31']

# Colors
BLUE = '\033[94m'
GREEN = '\033[92m'
END = '\033[0m'

# Component swaps
COMPONENTS = {
    'python3.9': {
        'f32': 'python39',
        'f31': 'python39',
    },
    'python3.8': {
        'f32': 'python3',
        'f31': 'python38',
    },
    'python3.7': {
        'f32': 'python37',
        'f31': 'python3',
    },
    'python3.6': {
        'f32': 'python36',
        'f31': 'python36',
    },
    'python3.5': {
        'f32': 'python35',
        'f31': 'python35',
    },
}


def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def run(cmd):
    debug(f'{BLUE}$ {cmd}{END}')
    cmd = shlex.split(cmd)
    out = subprocess.check_output(cmd, text=True).rstrip()
    if out:
        debug(out)
    return out


@contextlib.contextmanager
def in_tmp():
    original_location = os. getcwd()
    try:
        with tempfile.TemporaryDirectory() as d:
            os.chdir(d)
            yield
    finally:
        os.chdir(original_location)


def parse_args():
    # TODO?: Add more sophisticated argument parsing
    # TODO: Get this info from (a link to) Pagure PR
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} COMPONENT BRANCH [ORIGINAL_USERNAME [MY_USERNAME]]')
        sys.exit(1)

    component = sys.argv[1]
    branch = sys.argv[2]
    try:
        original_username = sys.argv[3]
    except IndexError:
        original_username = run('whoami')
    try:
        my_username = sys.argv[4]
    except IndexError:
        my_username = run('whoami')

    return component, branch, original_username, my_username


def git_stuff(component, branch, original_username, my_username):
    origin = f'ssh://pkgs.fedoraproject.org/rpms/{component}.git'
    new = f'ssh://pkgs.fedoraproject.org/forks/{original_username}/rpms/{component}.git'
    backport = f'ssh://pkgs.fedoraproject.org/forks/{my_username}/rpms/{component}.git'
    
    run(f'git clone {origin} {component}')
    os.chdir(component)
    run(f'git remote add new {new} --fetch')
    run(f'git remote add backport {backport}')
    run(f'git remote -v')
    run(f'git switch --track new/{branch}')
    branch_ = branch
    for fbranch in FBRANCHES:
        try:
            new_component = COMPONENTS[component][fbranch]
        except KeyError:
            remote = 'origin'
            component_ = component
        else:
            origin_ = f'ssh://pkgs.fedoraproject.org/rpms/{new_component}.git'
            run(f'git remote add origin-{fbranch} {origin_} --fetch')
            backport_ = f'ssh://pkgs.fedoraproject.org/forks/{my_username}/rpms/{new_component}.git'
            run(f'git remote add backport-{fbranch} {backport_}')
            run(f'git remote -v')
            remote = f'origin-{fbranch}'
            component_ = new_component
        try:
            run(f'git merge-base --is-ancestor {remote}/{fbranch} {branch_}')
        except subprocess.CalledProcessError:
            patches = run(f'git format-patch origin/master').splitlines()
            run(f'git switch --track {remote}/{fbranch}')
            backport_branch = f'{fbranch}-auto-{original_username}-{branch}'
            run(f'git switch -c {backport_branch}')
            for patch in patches:
                try:
                    run(f'ferrypick {patch} {component_}')
                except subprocess.CalledProcessError:
                    print('Sorry, this branch needs manual backport :(')
                    sys.exit(1)
            run(f'git push --force -u backport-{fbranch} {backport_branch}')
            run(f'git switch {branch}')
            branch_ = backport_branch
            link = (f'https://src.fedoraproject.org/fork/{my_username}/'
                    f'rpms/{component_}/diff/{fbranch}..{branch_}')
        else:
            link = (f'https://src.fedoraproject.org/fork/{original_username}/'
                    f'rpms/{component_}/diff/{fbranch}..{branch_}')
        print(f'{GREEN}{link}{END}')


def main():
    with in_tmp():
        git_stuff(*parse_args())


if __name__ == '__main__':
    main()
