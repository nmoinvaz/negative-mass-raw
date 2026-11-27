exec(open('red2.py').read().split("res = {}")[0])
import sys
gauge = sys.argv[1]
zero = sp.Integer(0)
if gauge == 'G1':
    kw = dict(Ff=zero)
else:
    kw = dict(Yy=zero)
E = {}
for k, (e0, e1) in out.items():
    E[k] = bg(sub_modes(e1, **kw))
    print(gauge, k, ':', E[k], '\n', flush=True)
pickle.dump(E, open(f'E_{gauge}.pkl', 'wb'))
