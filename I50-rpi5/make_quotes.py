"""Write quotes.md for #50 from the stored source files, checking every quote against its file.

usage: python -I make_quotes.py [--mutate=textual]
Each quote is a snippet that must occur in its source file. Matching ignores whitespace, hyphens/minus signs, soft hyphens,
ligatures and curly-quote variants (pdftotext loses hyphens at line ends and splits ligatures). HTML sources are tag-stripped and
unescaped first. A quote that is not found makes the run exit 1; `--mutate=textual` alters one snippet to show that.
The line number is that of the first matched character in the source file (n/a for html and json).
"""
import hashlib
import html
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = None
for a in sys.argv[1:]:
    if a == '--mutate=textual':
        MUT = 'textual'
    else:
        sys.exit('unknown argument ' + a)

S = {  # source id -> path under the raw folder
    'sn2_pdf': 'pdf_sn_v2/paper_flow.txt', 'sn2_abs': 'abs_2610_13206/abs.html', 'sn1_tex': 'src_sn_v1/x/research.tex',
    'sn2_tex': 'src_sn_v2/x/research.tex',
    'cdk_tex': 'src_cdk_v2/x/main.tex', 'nrm_pdf': 'pdf_nrm_v1/paper_flow.txt', 'nrm_tex': 'src_nrm_v1/x/pphstargatePDF.tex',
    'kain_pdf': 'pdf_kain_v1/paper_flow.txt', 'kain_tex': 'src_kain_v1/x/manuscript.tex',
    'fro_tex': 'src_fro_v1/x/paper.tex', 'mae_tex': 'src_mae_v2/x/Wormholeformation.tex',
    'hay03': 'cit_gr-qc_0306051/paper_flow.txt', 'st15': 'doi_jpcs_pdf/paper_flow.txt',
    'xcy': 'cit_2503_07610/paper_flow.txt', 'cfk': 'cit_2210_04905/paper_flow.txt', 'kain25': 'cit_2507_00109/paper_flow.txt',
    'nnr': 'cit_2012_13788/paper_flow.txt', 'sn_rot': 'cit_2610_29941/paper_flow.txt', 'shi26': 'cit_2604_00071/paper_flow.txt',
    'nak15': 'cit_1508_02657/paper_flow.txt', 'nn19': 'doi_org_10_1134_S1063776119100248/page.html',
    'inspire': 'inspire_sh02/page1.json', 'brady': 'src_brady/x/9402023.tex',
}

# (id, item, source id, section / equation, snippet)
Q = [
    # ---- item 1: Shirokov & Nachevsky ----
    ('S1', 1, 'sn2_abs', 'abstract (v2)', 'An isolated throat is unstable: depending on the sign of a small perturbation, it collapses to a black hole or inflates, at the rate that linear perturbation theory predicts to within 1.9%.'),
    ('S2', 1, 'sn2_abs', 'abstract (v2)', 'The results hold for one phantom-scalar model, equal masses, a single throat compactness and no spin.'),
    ('S3', 1, 'sn2_pdf', 'Sec. IV B', 'The measured e-folding time agrees with it to 0.2% at level 3 and 1.9% at level 4; larger departures grow more slowly. The initial perturbation is truncation error, and its sign flips with resolution: level 3 collapses and level 4 inflates.'),
    ('S4', 1, 'sn2_pdf', 'Sec. IV B', 'for which their linear analysis gives T = 0.758 [18]. We solved the linearised field equations of this solution ourselves, with their regularised master equation and, independently, in the gauge δϕ = 0; both give T = 0.7584, i.e. τlin = 5.13 M .'),
    ('S5', 1, 'sn2_pdf', 'Sec. IV C', 'At ε = ±10−2 and ±10−3 an outward perturbation (ε > 0) always collapses and an inward one always inflates. The radii of each ±ε pair cross at the ε-independent t× ≃ 13.0.'),
    ('S6', 1, 'sn2_pdf', 'Sec. IV C', 'The amplitude also sets the collapse time: horizons form at t = 11 (ε = +10−2 ) and t = 25 (+10−3 ), against t ≤ 61 for the unperturbed throat'),
    ('S7', 1, 'sn2_pdf', 'Sec. IV F', 'Until t ≈ 40 the neck grows exponentially in its own proper time at a rate H, with HR0 = 1.22 (locally 1.0–1.3), where R0 = 3.81 is the perturbed neck’s initial radius. This is 6% below our linear mode’s 1.30, which the local rate reaches. Spherical evolutions find the same proper-time exponential: Ha ≈ 1.1 for the massless throat [13]'),
    ('S8', 1, 'sn2_pdf', 'Sec. IV G', 'A static throat survives for about τ ln(1/ε), so its lifetime grows only logarithmically as the perturbation ε shrinks.'),
    ('S9', 1, 'sn2_pdf', 'Sec. IV G', 'The delay at equal horizon radius (Sec. IV C) puts the cost of each decade in ε at 11–12 M ≃ τ ln 10.'),
    ('S10', 1, 'sn2_pdf', 'Sec. IV H', 'In the language of critical collapse the static throat is consistent with a type-I critical solution [80]: a static solution with a single unstable mode (Sec. IV B) on the threshold between two end states. Here these are collapse and inflation, where the standard problem has collapse and dispersal. Two perturbation amplitudes show both type-I signatures but do not establish the scaling.'),
    ('S11', 1, 'sn2_pdf', 'Sec. IV H', 'The ε = +10−2 and +10−3 horizons form at R = 3.88 and 3.81, both close to the throat’s own R⋆ : a tenfold smaller perturbation leaves the black hole’s mass at formation almost unchanged, where type-II scaling would shrink it as a power of ε. Shinkai and Hayward found evidence for critical solutions with a definite black-hole mass in spherical evolutions of the massless throat [13]; here the critical solution is the static throat itself.'),
    ('S12', 1, 'sn1_tex', 'Sec. IV H (v1)', 'The measurements above are consistent with both type-I signatures, though two amplitudes do not establish the scaling.'),
    ('S13', 1, 'sn2_pdf', 'Sec. IV E', 'Ref. [44] evolved the massless throat with the phantom’s stress-energy halved; its bounce and horizon shedding are artifacts of the halving and do not occur here.'),
    ('S14', 1, 'sn2_tex', 'bibliography', '\\newblock ``Wormhole dynamics: nonlinear collapse and gravitational-wave emission,\'\'\n\\newblock arXiv:2604.00071 [gr-qc] (2026).'),
    # ---- item 2: Clough-Dietrich-Khan ----
    ('C1', 2, 'cdk_tex', 'Sec. III A (Results, Gravitational waves)', 'However, since the remnant is not a black hole, there is no characteristic black hole ringdown in the signal, and there is evidence of a longer lower frequency tail, particularly for higher velocities.'),
    ('C2', 2, 'cdk_tex', 'Sec. III B (Results, Matter fluxes)', 'We see that whilst the gravitational-wave flux is strictly positive as expected, the matter flux alternates in sign, with waves of positive and negative energy leaving the volume.'),
    ('C3', 2, 'cdk_tex', 'Sec. III B', 'The evolution does appear to settle down into a stable remnant, that could be described as a ``star\'\' of the warp fluid - it is a configuration of the fluid that appears to balance the gravitational forces and fluid pressures.'),
    ('C4', 2, 'cdk_tex', 'Sec. III B', 'It would be interesting to study whether this is a generic effect, such that spacetimes with NEC-violating matter cannot dynamically settle into a state with a mass below zero.'),
    ('C5', 2, 'cdk_tex', 'Sec. II E (Numerical setup)', 'The velocity of the warp ship is varied between 0.1 and 0.2.'),
    ('C6', 2, 'cdk_tex', 'Sec. I', 'it will quickly evolve away from that state and, in most cases, the warp fluid and spacetime deformations will disperse or collapse into a central point.'),
    ('C7', 2, 'cdk_tex', 'Sec. IV (Discussion)', 'We caution that the waveforms obtained are likely to be highly specific to the model employed'),
    # ---- item 3: Nakonieczna-Rogatko-Moderski ----
    ('N1', 3, 'nrm_pdf', 'Sec. IV (Results)', 'The results of the numerical computations are depicted on Penrose diagrams, i.e., we plot lines of constant r (u, v) in the (v, u)-plane.'),
    ('N2', 3, 'nrm_pdf', 'Sec. IV B (Einstein-phantom dilaton)', 'for every considered dilaton field amplitude the emerging spacetime is non-singular, that is black holes do not form.'),
    ('N3', 3, 'nrm_pdf', 'Sec. IV D (Einstein-Maxwell-phantom dilaton)', 'For values of amplitudes not exceeding 0.15 there are two branches of r,v = 0 horizon.'),
    ('N4', 3, 'nrm_pdf', 'Sec. IV D', 'may be interpreted as a dynamical wormhole [24]. On the other hand, for greater values of the parameter p̃k (larger than 0.2) the two branches of the horizon r,v = 0 form a loop with two ends coinciding with ending points of singular part of line r = 0.'),
    ('N5', 3, 'nrm_pdf', 'Sec. IV D', 'For even bigger values of amplitudes of dilaton field, from approximately p̃k = 0.25, the spacetime is non-singular with no visible horizons.'),
    ('N6', 3, 'nrm_pdf', 'Sec. IV D', 'The structure of an area beyond the horizon r,u = 0 is impossible to interpret fully and clearly, because calculations cannot be carried out until r = 0 and they end at some positive value of r.'),
    ('N7', 3, 'nrm_pdf', 'Sec. V (Conclusions)', 'In fact one has a formation of the black hole which gains phantom dilaton field which violates null energy condition. This phenomenon provides a formation of the wormhole structure.'),
    ('N8', 3, 'nrm_tex', 'Table III, row EM\\bar D, alpha = -1', '$ns\\rightarrow ns^\\ast$ & $WH\\rightarrow NS\\rightarrow ns$ & $ns\\rightarrow WH$'),
    ('N9', 3, 'nrm_tex', 'Figs. 2-18 captions', 'Lines of constant $r$ in $(vu)$-plane for $EM\\overline{D}$ evolution with a varying dilaton field amplitude.'),
    # ---- item 4: Kain 2026 ----
    ('K1', 4, 'kain_pdf', 'Sec. I', 'The study of dynamically evolved wormholes was initiated by Shinkai and Hayward when they dynamically evolved the Ellis-Bronnikov wormhole [21], which has since been dynamically evolved by a number of groups using various numerical methods [22–29].'),
    ('K2', 4, 'kain_tex', 'Sec. IV E (quantum corrected Schwarzschild, dynamical evolution)', 'We have studied dynamical evolutions with different initial data which also lead to collapse. This includes using different static solutions and different parameters for the pulse. We found the results to be qualitatively similar.'),
    ('K14', 4, 'kain_tex', 'Sec. III D (Ellis-Bronnikov, dynamical evolution)', 'We find that as the strength of the perturbation is reduced, the system maintains the static configuration longer before eventually evolving away.'),
    ('K15', 4, 'kain_tex', 'Sec. V (Comparison and conclusion)', 'As far as we are aware, the Ellis-Bronnikov wormhole and the quantum corrected Schwarzschild black hole are the only two charge free wormhole systems that have been dynamically evolved and which exhibit expansion or collapse.'),
    ('K3', 4, 'kain_pdf', 'refs. 22-23', '[22] J. A. González, F. S. Guzmán, and O. Sarbach, Instability of wormholes supported by a ghost scalar field. II. Nonlinear evolution, Class. Quant. Grav. 26, 015011 (2009), arXiv:0806.1370 [gr-qc]. [23] A. Doroshkevich, J. Hansen, I. Novikov, and A. Shatskiy, Passage of radiation through wormholes, Int. J. Mod. Phys. D 18, 1665 (2009), arXiv:0812.0702 [gr-qc].'),
    ('K4', 4, 'kain_pdf', 'refs. 24-25', '[24] H.-a. Shinkai and T. Torii, Wormhole Dynamics, J. Phys. Conf. Ser. 574, 012056 (2015). [25] H.-A. Shinkai and T. Torii, Nonlinear Dynamics in the Einstein-Gauss-Bonnet gravity, Phys. Rev. D 96, 044009 (2017), arXiv:1706.02070 [gr-qc].'),
    ('K5', 4, 'kain_pdf', 'refs. 26-27', '[26] I. D. Novikov and D. I. Novikov, Collapse of a Wormhole and its Transformation into Black Holes, J. Exp. Theor. Phys. 129, 495 (2019). [27] I. D. Novikov, D. I. Novikov, and S. V. Repin, Disintegration and expansion of wormholes, Phys. Rev. D 102, 124073 (2020), arXiv:2012.13788 [gr-qc].'),
    ('K6', 4, 'kain_pdf', 'refs. 28-29', '[28] K. Calhoun, B. Fay, and B. Kain, Matter traveling through a wormhole, Phys. Rev. D 106, 104054 (2022), arXiv:2210.04905 [gr-qc]. [29] A. Xu, X. Y. Chew, and D.-h. Yeom, Dynamics of Bronnikov-Ellis wormhole with double-null simulation, JCAP 08, 012, arXiv:2503.07610 [gr-qc].'),
    ('K7', 4, 'st15', 'Sec. 4 (Conclusions and Discussions)', 'In [7], for small perturbations, an existence of critical solution is suggested. The similar behaviors are also observed in our investigations, which will be reported elsewhere.'),
    ('K8', 4, 'nn19', 'abstract (publisher landing page)', 'Based on Khalatnikov’s ideas, we consider the physical processes that arise in the collapse of wormholes of different types.'),
    ('K9', 4, 'nnr', 'abstract', 'We consider the process of catastrophic expansion of a spacelike wormhole after a violation of its equilibrium state.'),
    ('K10', 4, 'cfk', 'abstract', 'We confirm that, for the massless symmetric wormhole, a pulse of regular scalar field causes the wormhole throat to collapse and form an apparent horizon, while a pulse of ghost scalar field can cause the wormhole throat to expand.'),
    ('K11', 4, 'xcy', 'abstract', 'The process of two scenarios can be accelerated by increasing the amplitude of pulses but can be delayed by increasing the wormhole’s mass.'),
    ('K12', 4, 'xcy', 'body text, pulse collisions (before Fig. 7)', 'Specifically, can fine-tuned collisions stabilize the throat, delaying or preventing horizon formation and maintaining traversability?'),
    ('K13', 4, 'xcy', 'body text, after Fig. 8', 'hybrid pulse interactions can reduce but do not cure the instability, offering only limited extensions to the wormhole’s lifetime.'),
    # ---- item 5: citers of Shinkai-Hayward ----
    ('H1', 5, 'hay03', 'body text, summary of SH02', 'Unexpected critical behaviour was also discovered: the initial energy determines the collapse time x − x0 = −0.60 ln E0 and there appears to be a minimal black-hole mass M = 0.30a or Hubble constant H = 1.1/a as perturbations tend to zero, for both exotic and normal field perturbations. All this is unexplained.'),
    ('H2', 5, 'hay03', 'conclusions (bullet list)', 'Numerically discovered critical behaviour suggests critical black-hole and inflationary-universe solutions.'),
    ('H3', 5, 'kain25', 'abstract', 'In vacuum, the wormhole expands, but in the presence of even a small amount of classical matter, the wormhole collapses, forming a horizon and evolving to an evaporating black hole.'),
    ('H4', 5, 'shi26', 'abstract', 'To force a clean collapse while breaking spherical symmetry, we reduce the phantom stress-energy support to Ssupport = 0.5 and add a quadrupolar scalar-field perturbation'),
    ('H5', 5, 'shi26', 'Sec. II (initial data and perturbation)', 'This halves the repulsive support, forcing the wormhole into the compressive branch.'),
    ('H6', 5, 'sn_rot', 'abstract', 'At intermediate spins some throats expand, with the direction of departure depending on the effective perturbation.'),
    ('H7', 5, 'nak15', 'abstract', 'The square of mass parameter of the dark matter scalar field potential controlled the formation of a Cauchy horizon or wormhole throats in the spacetime.'),
    ('H8', 5, 'inspire', 'INSPIRE abstract of 2610.38659', 'the apparent loss of the radial instability found in the original real-eigenvalue treatment is therefore not stabilization, but a transition to an oscillatory instability.'),
    ('H9', 5, 'inspire', 'INSPIRE abstract of 2611.00541', 'Numerical evolutions are consistent with saturation on the nodeless branch.'),
    # ---- item 6: the Frolov map ----
    ('F1', 6, 'fro_tex', '[Fro97] eq. (metric)', 'dS^2 = - 2e^{2\\Sigma}\\, du dv + R^2\\, d\\Omega^2,'),
    ('F2', 6, 'fro_tex', '[Fro97] eq. (ss_soln)', 'R &=& \\sqrt{u^2 - uv - pv^2},'),
    ('F3', 6, 'fro_tex', '[Fro97] eq. (ss_soln)', '\\Phi &=& \\frac{1}{2} \\ln\n    \\left[-\\frac{2pv + u(1 - \\sqrt{1+4p})}{2pv + u(1 + \\sqrt{1+4p})}\\right] +\n    \\varphi(p).'),
    ('F4', 6, 'fro_tex', '[Fro97] eq. (const_phi)', '- \\frac{1}{2} \\ln \\left[\\frac{\\sqrt{1+4p}-1}{\\sqrt{1+4p}+1}\\right] ='),
    ('F5', 6, 'fro_tex', '[Fro97] Sec. II', 'For values $p>0$ of control parameter, a black hole is formed; for\n$p<0$ the field disperses, and the spacetime is flat again in region\n$u>0$. (Our choice of sign of $p$ is opposite to the one in\n\\cite{Brady:94}.'),
    ('F6', 6, 'fro_tex', '[Fro97] eq. (crit)', 'R_0 &=& \\sqrt{u^2 - uv},'),
    ('F7', 6, 'fro_tex', '[Fro97] eq. (es:3)-(es:7)', '(R^2)_{,uv} + e^{2\\Sigma} = 0,'),
    ('F8', 6, 'fro_tex', '[Fro97] eq. (es:5), (es:6)', 'R_{,vv} - 2\\Sigma_{,v}R_{,v} + R (\\Phi_{,v})^2 = 0,'),
    ('F9', 6, 'fro_tex', '[Fro97] eq. (mass)', '1 - \\frac{2M}{R} = 2 g^{uv} R_{,u}R_{,v}.'),
    ('F10', 6, 'fro_tex', '[Fro97] eq. (ah)', 'A(u,v) = u^{;\\mu}_{\\ \\ ;\\mu} = R_{,v}.'),
    ('F11', 6, 'fro_tex', '[Fro97] Sec. III', 'The signs are chosen to make the arguments of the logarithm positive in\nthe region of interest ($v>0$, $u<0$), where the field evolution occurs.'),
    ('F12', 6, 'fro_tex', '[Fro97] Sec. IV', 'Clearly, the self-similar mode has eigenvalue $k=0$'),
    ('F13', 6, 'fro_tex', '[Fro97] Sec. V', 'The eigenvalues $k$ approach $\\sup \\Re k = 1$, which corresponds to the\nmass-scaling exponent $\\beta=1$. This is different from the exponent\n$\\beta=1/2$ found in'),
    ('F14', 6, 'fro_tex', '[Fro97] Sec. V', '\\frac{1}{2} < \\Re k < 1,'),
    ('B1', 6, 'brady', '[Bra94] eq. (8)', 'r^2 &=& \\alpha v^2 + \\beta u^2 - uv \\; , \\label{eqn:8}'),
    ('B2', 6, 'brady', '[Bra94] Sec. 2', 'In order to discuss the problem of collapse we can set $\\beta = 1$ without loss\nof generality.'),
    ('B3', 6, 'brady', '[Bra94] Sec. 2', 'these are subcritical ($0<\\alpha < 1/4$), critical ($\\alpha = 0$) and\nsupercritical ($\\alpha <0$).'),
    ('B4', 6, 'brady', '[Bra94] Sec. 2', 'Moreover notice when $\\alpha = 1/4$ the solution is simply flat\nspace.'),
    ('B5', 6, 'brady', '[Bra94] eq. (mass1)', 'm(u,v) =  -uv(1-4\\alpha\\beta)/4r'),
    ('B6', 6, 'brady', '[Bra94] abstract', 'for near critical evolution\n$M \\simeq |\\alpha-\\alpha_{\\rm crit}|^{1/2}$.'),
    ('M1', 6, 'mae_tex', '[Mae09] eq. (roberts1)', 'ds^2=-2dudv+(-uv+C_1v^2+C_2u^2)d\\Omega^2, \\label{roberts1}'),
    ('M2', 6, 'mae_tex', '[Mae09] eq. (roberts2)', '\\phi=\\phi_0\\pm \\frac{1}{2\\sqrt{\\pi}}{\\rm arctanh}\\biggl(\\frac{1-2C_1(v/u)}{\\sqrt{1-4C_1C_2}}\\biggl) \\label{roberts2}'),
    ('M3', 6, 'mae_tex', '[Mae09] eq. (roberts-mass)', 'm_{\\rm MS}=-\\frac{(1-4C_1C_2)uv}{4\\sqrt{-uv+C_1v^2+C_2u^2}}. \\label{roberts-mass}'),
    ('M4', 6, 'mae_tex', '[Mae09] eq. (beq)', '{\\ma R}^{\\mu}_{~~\\nu}=8\\pi \\epsilon \\phi^{,\\mu}\\phi_{,\\nu}, \\label{beq}'),
    ('M5', 6, 'mae_tex', '[Mae09] Sec. II', 'For $C_1C_2=1/4$, it is the Minkowski spacetime.'),
    ('M6', 6, 'mae_tex', '[Mae09] Sec. II', 'Therefore, the scalar field is purely imaginary corresponding to a ghost scalar field for $C_1C_2>1/4$.'),
    ('M7', 6, 'mae_tex', '[Mae09] Sec. II', 'On the other hand, the solution with $C_1=0$ was obtained by Brady in 1994'),
    ('M8', 6, 'mae_tex', '[Mae09] Sec. III', 'two Roberts spacetimes with the same nonzero $C_2$ but different $C_1$ can be attached in a regular manner at $v=0$.'),
    ('M9', 6, 'mae_tex', '[Mae09] Sec. II', 'we can set $|C_1|=1$ without loss of generality by the coordinate transformations ${\\bar v}:=\\sqrt{|C_1|}v$ and ${\\bar u}:=u/\\sqrt{|C_1|}$'),
]

TERMS = ['critical', 'threshold', 'fine-tun', 'bisect', 'scaling', 'exponent', 'lifetime', 'unstable mode', 'throat', 'wormhole', 'Choptuik', 'black hole']
COUNT_SRC = [  # what the "does not contain" counts are taken from
    ('Shirokov & Nachevsky v2 (PDF text)', 'sn2_pdf'), ('Clough et al. v2 (TeX)', 'cdk_tex'), ('Nakonieczna et al. v1 (PDF text)', 'nrm_pdf'),
    ('Kain 2026 v1 (PDF text)', 'kain_pdf'),
]

STRIP = re.compile(r'[\s\-\u2010\u2011\u2212\u00ad\u200b]+')
LIG = {'\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl', '\ufb03': 'ffi', '\ufb04': 'ffl', '\u2019': "'", '\u2018': "'", '\u201c': '"', '\u201d': '"'}


def load(sid):
    path = os.path.join(HERE, S[sid])
    raw = open(path, encoding='utf-8', errors='replace').read()
    sha = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    lineno = True
    if path.endswith('.html'):
        raw = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw, flags=re.S)))
        raw = html.unescape(raw)
        lineno = False
    if path.endswith('.json'):
        d = json.load(open(path, encoding='utf-8'))
        raw = '\n'.join(' '.join(a['value'] for a in h['metadata'].get('abstracts', [])) for h in d['hits']['hits'])
        lineno = False
    raw = unicodedata.normalize('NFC', raw)
    # normalized text with a map to source line numbers
    out, lines = [], []
    ln = 1
    for ch in raw:
        if ch == '\n':
            ln += 1
        for c2 in LIG.get(ch, ch):
            if STRIP.fullmatch(c2):
                continue
            out.append(c2)
            lines.append(ln)
    return ''.join(out), lines, sha, lineno, raw


def norm(s):
    s = ''.join(LIG.get(c, c) for c in unicodedata.normalize('NFC', s))
    return STRIP.sub('', s)


CACHE = {}
fails = []
ok = 0
recs = []
for i, (qid, item, sid, where, snip) in enumerate(Q):
    if MUT == 'textual' and qid == 'S10':
        snip = snip.replace('type-I critical solution', 'type-II critical solution')
    if sid not in CACHE:
        CACHE[sid] = load(sid)
    text, lines, sha, has_lines, raw = CACHE[sid]
    ns = norm(snip)
    pos = text.find(ns)
    if pos < 0:
        fails.append(qid)
        print('FAIL', qid, 'not found in', S[sid], ':', snip[:70].replace('\n', ' '))
        recs.append((qid, item, sid, where, snip, None, sha))
        continue
    ok += 1
    recs.append((qid, item, sid, where, snip, lines[pos] if has_lines else None, sha))
    print('PASS', qid, S[sid], 'line', lines[pos] if has_lines else 'n/a')

# term counts for the "does not contain" lists
counts = {}
for label, sid in COUNT_SRC:
    if sid not in CACHE:
        CACHE[sid] = load(sid)
    raw = CACHE[sid][4]
    counts[label] = [len(re.findall(re.escape(t).replace(r'\-', '[- ]?'), raw, re.I)) for t in TERMS]

print('quotes:', ok, 'found,', len(fails), 'not found')
if fails:
    sys.exit(1)
if MUT:
    sys.exit(0)

# ---------------------------------------------------------------------------------------------------------------
PROSE = open(os.path.join(HERE, 'quotes_prose.md'), encoding='utf-8').read()
by_item = {}
for r in recs:
    by_item.setdefault(r[1], []).append(r)
parts = ['# I50-rpi5: records for the reading gaps of notes/critical_ghost.md (#50)\n',
         'Written by `make_quotes.py` from the stored source files (`fetch.log` has URL, status and sha256 of each download). Every quote ',
         'below was found in its file by the script (matching ignores whitespace, hyphens and ligatures). Papers are data: nothing in them ',
         'was run, and no text addressed to an AI agent was found in any page or file read.\n']
for item in sorted(by_item):
    parts.append('\n## ' + PROSE.split('@@ITEM%d@@' % item)[1].split('@@END@@')[0].strip('\n') + '\n')
    parts.append('\n**Quotes** (id, source file, line in that file, section or equation):\n')
    for qid, it, sid, where, snip, line, sha in by_item[item]:
        parts.append('\n- **%s** `%s` line %s, %s. sha256 `%s`\n\n  > %s\n' % (
            qid, S[sid], line if line else 'n/a', where, sha[:16], snip.replace('\n', '\n  > ')))
parts.append('\n## Term counts used in the "does not contain" lists\n')
parts.append('\nCase-insensitive counts in the whole text of the source (hyphen optional where written with one); `black hole` and `wormhole` ')
parts.append('counts include the bibliography.\n\n| source | ' + ' | '.join(TERMS) + ' |\n|---|' + '---|' * len(TERMS) + '\n')
for label, _ in COUNT_SRC:
    parts.append('| %s | %s |\n' % (label, ' | '.join(str(n) for n in counts[label])))
open(os.path.join(HERE, 'quotes.md'), 'w', encoding='utf-8').write(''.join(parts))
print('wrote quotes.md')
