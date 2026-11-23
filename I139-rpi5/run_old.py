"""Runs threshold_isolation.py as it was before #139 (git show 850785b) in place of the worktree's copy, with the same argv.
usage: run_old.py [threshold_isolation.py args]   (from phase2/dg_proof of the i139 worktree)"""
import os
import subprocess
import sys

WT = os.path.expanduser('~/Source/negative-mass-i139')
path = os.path.join(WT, 'phase2/dg_proof/threshold_isolation.py')
src = subprocess.run(['git', '-C', WT, 'show', '850785b:phase2/dg_proof/threshold_isolation.py'],
                     capture_output=True, text=True, check=True).stdout
sys.argv = [path] + sys.argv[1:]
exec(compile(src, path, 'exec'), {'__file__': path, '__name__': '__main__'})
