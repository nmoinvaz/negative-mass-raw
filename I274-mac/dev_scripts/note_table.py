"""the per-box table of the note in taylor_polar.md, from results/record/*.json (the same numbers as i274_recount_output.txt)"""
import glob, json, os, sys
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
order = [ln.strip() for ln in open(os.path.join(RAW, "box_names.txt"))] + ["s1_l5"]
print("| box | source | l | eps, omega | region | R_s | winding stored, crate | planted found (of) | max step | min abs D | margin, with plant (rad) | E (rad) | margin / 10 E | asked = stored | wall (s) |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for n in order:
    r = json.load(open(os.path.join(RAW, "results", "record", n + ".json")))
    c, lg = r["crate"], r["log"]
    reg = f"Re [{r['x0']}, {r['x1']}], " + (f"abs(Im) ≤ {r['y1']}" if r["sym"] else f"Im [{r['y0']}, {r['y1']}]")
    same = r["points"]["asked_not_stored"] == 0 and r["points"]["stored_not_asked"] == 0
    print(f"| {n}{' (extra)' if n == 's1_l5' else ''} | #{r['issue']} | {r['l']} | {r['eps']:+d}, {r['w']} | {reg} | {r['rs']:.1f} | {lg['wind']:+.4f}, {c['winding']:+.4f} | "
          f"{c['plant_diff']:+.4f} of {lg['expected']} | {c['maxstep']:.2f} | {c['nmin']:.2e} | {c['margin']:.2e}, {c['plant_margin']:.2e} | {r['E']:.2e} | "
          f"{r['margin_used'] / (10 * r['E']):.1f} | {'yes, ' + str(r['points']['asked']) if same else 'NO'} | {c['wall_sum']:.1f} |")
