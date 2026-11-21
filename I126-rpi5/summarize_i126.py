"""
Walls, evaluations and new cache points of #126's runs, from this folder's queue.log, logs and caches. Usage, from this
folder:  python summarize_i126.py > summary.txt
A job's wall is the time between its start and end lines in queue.log. Its evaluations are the last count printed in its log
(winding2.py: "(N evals"; zerilli_zeros.py: "N evaluations"). A cache's points before the run are those of its source copy
named in cache_sources.sha256, checked against the sha256 there; after, those in cache/.
"""
import os, re, sys, pickle, hashlib, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
iso = dt.datetime.fromisoformat
st, en, rc = {}, {}, {}
for ln in open('queue.log'):
    m = re.match(r'(\S+) (?:15-min load [\d.]+ < 4: )?start (\S+?): (?:winding2|zerilli)', ln)
    if m:
        st[m.group(2)] = iso(m.group(1))
    m = re.match(r'(\S+) end (\S+) rc=(\d+)', ln)
    if m:
        en[m.group(2)], rc[m.group(2)] = iso(m.group(1)), int(m.group(3))
jobs = [l.split('|')[0] for l in open('jobs.txt')]
ctrl = [j for j in jobs if '_mut_' in j or j == 'z_flat']
groups = [('W boxes (winding2.py --guard=all)', [j for j in jobs if j.startswith('w_') and j not in ctrl]),
          ('Z boxes (zerilli_zeros.py --guard=all)', [j for j in jobs if j.startswith('z_') and j not in ctrl]),
          ('Controls', ctrl)]
print("# Walls and evaluations of #126's jobs (from queue.log and the logs)")
tot = {}
for title, js in groups:
    print(f"\n## {title}\n\n| job | exit | wall (min) | evaluations |\n|---|---|---|---|")
    w = 0.0
    for j in js:
        txt = open(f'{j}.log').read()
        ev = (re.findall(r'\((\d+) evals', txt) or re.findall(r'(\d+) evaluations', txt) or [''])[-1]
        wall = (en[j] - st[j]).total_seconds() / 60
        w += wall
        print(f"| {j} | {rc[j]} | {wall:.1f} | {ev} |")
    tot[title] = w
    print(f"\n{len(js)} jobs, {w:.1f} min = {w / 60:.2f} h of process time")
allw = sum(tot.values())
first, last = min(st.values()), max(en.values())
print(f"\nAll {len(jobs)} jobs: {allw / 60:.2f} h of process time; first start {first:%Y-%m-%d %H:%M}, last end {last:%Y-%m-%d %H:%M}, "
      f"{(last - first).total_seconds() / 3600:.2f} h of wall time")

src = {}
for ln in open('cache_sources.sha256'):
    sha, path = ln.rstrip('\n').split('  ', 1)
    if 'not copied' not in path:
        src[os.path.basename(path)] = (sha, path)
print("\n# Cache points before and after the run\n\n| cache | before | after | new |\n|---|---|---|---|")
tb = ta = 0
for f in sorted(os.listdir('cache')):
    sha, path = src[f]
    raw = open(os.path.join('..', path), 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == sha, path
    b, a = len(pickle.loads(raw)), len(pickle.load(open(os.path.join('cache', f), 'rb')))
    tb += b; ta += a
    print(f"| {f[:-4]} | {b} | {a} | {a - b} |")
print(f"\n{len(os.listdir('cache'))} caches: {tb} points before, {ta} after, {ta - tb} new")
