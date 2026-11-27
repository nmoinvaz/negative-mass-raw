import sys
d = "/tmp/claude-1000/-home-nathan-Source-negative-mass-i218/97b7dfd3-03ba-46d3-a327-cbb66951365d/scratchpad/dev/"
head = open(d + "polar_head.py").read(); b1 = open(d + "polar_body.py").read(); b2 = open(d + "polar_body2.py").read()
b3 = open(d + "polar_body3.py").read(); tail = open(d + "polar_tail.py").read()
code = open(d + "emit_out.py").read()
table = "\n# ------------------------------------------------------------------------------------------------ coefficient table (polar_derive.py emit)\nimport math\nfrom math import sqrt\n\n" + code + "\n"
open(sys.argv[1], "w").write(head + table + b1 + b2 + b3 + tail)
