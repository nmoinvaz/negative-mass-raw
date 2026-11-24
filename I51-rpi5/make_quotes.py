#!/usr/bin/env python3
"""Writes quotes.md for #51 from the stored sources. Every quote is searched verbatim (whitespace collapsed) in its
source file; a quote that is not found makes the script exit 1. TeX line numbers are those of the stored file.

    python3 -I make_quotes.py [--mutate=textual]

--mutate=textual alters one quote (a changed letter) and must make the script exit 1 (the quotes.md it then writes is
the mutated one: rerun without the flag last).
Sources: DG08 e-print TeX of v1, v2, v3 (../I149-rpi5, fetched by #149); Crossref JSON (Cao abstract); INSPIRE JSON
(Cao references; Paranjape abstract); the Springer chapter page HTML (Paranjape abstract and references).
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "--mutate=textual" in sys.argv
I149 = os.path.join(HERE, "..", "I149-rpi5")
SRC = {
    "v1": os.path.join(I149, "dg08_v1", "nm8.tex"),
    "v2": os.path.join(I149, "dg08_v2", "ivps02.tex"),
    "v3": os.path.join(I149, "dg08_v3", "ivps03.tex"),
    "sh1": os.path.join(HERE, "shirokov_v1", "bondi_dipole.tex"),
    "sh2": os.path.join(HERE, "shirokov_v2", "bondi_dipole.tex"),
    "iv2": os.path.join(HERE, "ivanov_eprint_v2", "ufn1.tex"),
    "sg1": os.path.join(HERE, "new_2611_14482_eprint", "main_final.tex"),
}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def strip_tags(s):
    return norm(html.unescape(re.sub(r"<[^>]+>", " ", s)))


def tex_nocomment(raw):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in raw.split("\n"))


# text sources other than TeX: key -> function returning the text
def cao_abstract():
    j = json.load(open(os.path.join(HERE, "cao_crossref", "out.json")))
    for it in j["message"]["items"]:
        if it["DOI"].lower() == "10.1142/s0218271812500617":
            return strip_tags(it["abstract"])
    raise SystemExit("Cao abstract not found in Crossref JSON")


def cao_refs():
    j = json.load(open(os.path.join(HERE, "cao_inspire_full", "out.json")))
    out = []
    for r in j["metadata"]["references"]:
        r = r["reference"]
        out.append("%s %s %s %s" % ((r.get("authors") or [{}])[0].get("full_name", ""), (r.get("publication_info") or {}).get("journal_title", ""),
                                    (r.get("publication_info") or {}).get("journal_volume", ""), (r.get("publication_info") or {}).get("year", "") or r.get("arxiv_eprint", "")))
    return " | ".join(norm(x) for x in out)


def html_text(d):
    return strip_tags(open(os.path.join(HERE, d, "abs.html"), encoding="utf-8").read())


def par_page():
    return open(os.path.join(HERE, "par_springer_page", "out.html"), encoding="utf-8").read()


def par_abstract_page():
    t = par_page()
    m = re.search(r'<section[^>]*data-title="Abstract"[^>]*>(.*?)</section>', t, re.S)
    return strip_tags(m.group(1))


def par_refs_page():
    t = par_page()
    m = re.search(r'data-title="References"(.*?)</section>', t, re.S)
    return strip_tags(m.group(1))


def par_abstract_inspire():
    j = json.load(open(os.path.join(HERE, "par_inspire", "out.json")))
    return norm(j["hits"]["hits"][0]["metadata"]["abstracts"][0]["value"])


# quotes: (id, item, source key, locator (section), text, verdicts it bears on)
Q = [
    # ---- DG08 section V (Summary)
    ("S1", "DG08", "v3", "V Summary (v2: identical to v3)",
     "We have introduced an alternative diagonalization of the linearized even mode Einstein's equation around a Schwarzschild spacetime, using a field $\\hat \\Psi$ which is smooth for regular metric perturbations, regardless the sign of the mass $M$.", "A1"),
    ("S2", "DG08", "v3", "V Summary",
     "Moreover, the spatial piece of the modified wave equation has a unique self adjoint extension, that naturally selects the boundary condition that is physically relevant.", "A2"),
    ("S3", "DG08", "v3", "V Summary",
     "The connection between the two fields is provided by an intertwining operator, $\\hat \\Psi = \\Psi_z - \\psi_0'/\\psi_0 \\Psi_z =: {\\cal I} \\Psi_z$, similar to the operators linking supersymmetric pairs of quantum hamiltonians.", "A1"),
    ("S4", "DG08", "v3", "V Summary",
     "A straightforward application of this formalism allows us to show that the unstable mode found in \\cite{dg} can actually be excited by initial data compactly supported away from the singularity. This closes a gap in our proof in \\cite{dg} of the linear instability of the negative mass Schwarzschild spacetime.", "A2, A4"),
    ("S5", "DG08", "v1", "V Summary",
     "It is shown that the function $\\hat \\Psi = \\Psi_z - \\psi_0'/\\psi_0 \\Psi_z =: {\\cal I} \\Psi_z$ obeys a wave equation with a smooth potential if $\\psi_0$ is a particular zero mode of Zerilli's Hamiltonian.", "A1"),
    ("S6", "DG08", "v1", "V Summary",
     "This closes a gap in our proof in \\cite{dg} of instability of the negative mass Schwarzschild spacetime.", "A4"),
    # ---- DG08 intertwiner sections: v1 III, v2/v3 IV A
    ("I1", "DG08", "v1", "III Intertwining operators (unnumbered Lemma 1 precedes; v1 has no SUSY remark)",
     "That this is actually the case can be checked by a direct calculation using our previous results, from where we obtain $\\hat {\\cal H} (1/ \\pe) = \\w_o{}^ 2 /\\pe$. We will set $\\hat \\psi {}_{\\w_o}^{(j=2)} := 1/\\pe$", "A1"),
    ("I2", "DG08", "v3", "IV A Intertwining operators (v2: same text in IV A)",
     "That this is actually the case can be checked by a direct calculation using our previous results, from where we obtain $\\hat {\\cal H} (1/ \\pe) = \\w_o{}^ 2 /\\pe$. We will set $\\hat \\psi {}_{\\w_o}^{(j=2)} := 1/\\pe$", "A1"),
    ("I3", "DG08", "v3", "IV A, after Lemma 3 (v2 identical; absent in v1)",
     "In the supersymmetric quantum mechanics context, $\\w_o=0$ and $\\psi _{\\w_o}^{(j=1)}$ satisfies appropriate boundary conditions to make it an eigenfunction of ${\\cal H}$. Moreover, it corresponds to the lowest eigenvalue of ${\\cal H}$. In this case ${\\cal H}$ and $\\hat {\\cal H}$ are isospectral, except for $\\w_o{}^2=0$, which is missing in the spectrum of $\\hat {\\cal H}$.", "A1"),
    ("I4", "DG08", "v3", "IV A, after Lemma 3",
     "In the above construction, however, we do not require any specific boundary condition on the function $\\pe$ used to construct the intertwining operator.", "A1, A2"),
    ("I5", "DG08", "v3", "IV B (eq. l2zm), the l = 2 zero mode of Zerilli's Hamiltonian",
     "\\psi_0 = \\frac{r(r^3+3Mr^2-6M^3)}{8M^4(3M+2r)}", "A1"),
    ("I6", "DG08", "v1", "IV, the zero mode used",
     "The ${\\cal H}_z$ eigenfunction that we will use in Lemma 1 is the generalization to arbitrary harmonic number $\\ell$ of the zero mode ($\\w_0=0$) in \\cite{ghi}.", "A1"),
    # ---- DG08 growth rate and numerics
    ("K1", "DG08", "v3", "II A, case M < 0, eq. (k)",
     "k =\\frac{ (\\ell-1) \\ell (\\ell+1) (\\ell+2)} {6} ,", "A3"),
    ("K2", "DG08", "v3", "II A, case M < 0, the mode (RW24a)",
     "\\exp \\left[\\frac{k(t- r)}{2|M|}\\right]", "A3"),
    ("N1", "DG08", "v3", "III Numerical integration (v2 identical; v1 has no numerics)",
     "The boundary condition at $r=0$ was enforced by imposing Robin type boundary conditions in the form $3 \\hat \\Psi - \\p \\hat \\Psi / \\p r =0$ at $r = 10^{-4}$.", "A2"),
    ("N2", "DG08", "v3", "I Introduction (v2 identical)",
     "As is shown in Section \\ref{num}, this is {\\em not} related to the $x=0$ boundary conditions; if a perturbation is initially supported away from the singularity, {\\em the unstable modes are excited before the excitation reaches the singularity.}", "A2, A4"),
    # ---- Cao 2012
    ("C1", "Cao 2012", "cao_abs", "Crossref abstract (publisher-deposited)",
     "we demonstrate the first numerical evolutions of the interaction between positive and negative mass objects.", "E"),
    ("C2", "Cao 2012", "cao_abs", "Crossref abstract",
     "we set our computational domain around the positive mass black hole while excluding the region around the naked singularity introduced by the negative mass object.", "E"),
    ("C3", "Cao 2012", "cao_abs", "Crossref abstract",
     "Besides the usual Sommerfeld numerical boundary condition, an approximate boundary condition is proposed for this nonasymptotically-flat computational domain.", "E"),
    ("C4", "Cao 2012", "cao_abs", "Crossref abstract",
     "Our result implies that this spacetime does have a Newtonian limit which corresponds to a negative mass particle chasing a positive mass particle.", "C1, E"),
    ("C5", "Cao 2012", "cao_refs", "INSPIRE reference list (30 entries): the negative-mass Schwarzschild perturbation papers",
     "Gibbons, G. Commun.Math.Phys. 35 1974 | Bonnor, W. Z.Phys. 177 1964 |", "A, C"),
    ("C6", "Cao 2012", "cao_refs", "INSPIRE reference list",
     "Gleiser, R. Class.Quant.Grav. 23 2006 | Miyamoto, U. J.Phys.Conf.Ser. 31 2006 | Cardoso, V. Phys.Rev.D 74 2006 |", "A"),
    # ---- Paranjape 2025
    ("P1", "Paranjape 2025", "par_abs", "Springer chapter page, Abstract (INSPIRE has the same text, see P2)",
     "It was shown [ 1 , 2 , 3 ] how to fill in a “negative mass star” so that the singularity is smoothed out, and the energy-momentum satisfies the dominant energy condition and can even gives rise to a dynamically stable configuration.", "A4"),
    ("P2", "Paranjape 2025", "par_abs_inspire", "INSPIRE record 3116840, abstract",
     "and can even gives rise to a dynamically stable configuration. However, some puzzles persist.", "A4"),
    ("P3", "Paranjape 2025", "par_abs", "Springer chapter page, Abstract",
     "Firstly, the exchange of a spin two graviton normally provides an attractive force between sources, while a simple calculation of the geodesic motion in the presence of a negative mass star shows repulsion.", "A4"),
    ("P4", "Paranjape 2025", "par_refs", "Springer chapter page, References 1-3",
     "J. Belletête, M.B. Paranjape, On negative mass. Int. J. Mod. Phys. D 22 , 1341017 (2013).", "A4"),
    ("P5", "Paranjape 2025", "par_refs", "Springer chapter page, References 2-3",
     "S. Mbarek, M.B. Paranjape, Negative mass bubbles in de Sitter spacetime. Phys. Rev. D 90 (10), 101502 (2014).", "A4"),
    ("P6", "Paranjape 2025", "par_refs", "Springer chapter page, References 3",
     "M.C. Johnson, M.B. Paranjape, A. Savard, N. Tapia-Arellano, Stable, thin wall, negative mass bubbles in de Sitter space-time. Gen. Rel. Grav. 52 (8), 80 (2020).", "A4"),
    ("P7", "Paranjape 2025", "par_page", "Springer chapter page, access banner",
     "This is a preview of subscription content, log in via an institution", "—"),
    # ---- post-window items that bear on verdicts (found by the rerun)
    ("H1", "Shirokov 2608.24577", "sh_abs", "arXiv abs page, submission history",
     "[v2] Mon, 26 Oct 2026 10:34:45 UTC (7,082 KB)", "B, C2, E"),
    ("H2", "Shirokov 2608.24577", "sh_abs", "arXiv abs page, comments field",
     "v2: fourth-order time integration and corrected initial data, all simulations rerun, resolution study added, second author added; the qualitative results are unchanged", "B, C2, E"),
    ("H3", "Shirokov 2608.24577", "sh1", "v1 abstract",
     "The phantom star is, to our knowledge, the first asymptotically flat body of negative ADM mass evolved in numerical relativity; alone it survives to $t=1000$, slowly relaxing outward.", "B, E"),
    ("H4", "Shirokov 2608.24577", "sh2", "v2 abstract",
     "To our knowledge, they are the first asymptotically flat bodies of negative ADM mass evolved in numerical relativity.", "B, E"),
    ("H5", "Shirokov 2608.24577", "sh1", "v1 results, lone star to t = 1000",
     "the field peak decays \\emph{linearly} at $0.632\\%$ per $100$ time units from $t\\approx200$", "B"),
    ("H6", "Shirokov 2608.24577", "sh1", "v1 discussion",
     "a measured decay rate over the window evolved, not asymptotic stability.", "B"),
    ("H7", "Shirokov 2608.24577", "sh2", "v2 results, M-t1000",
     "neither collapses nor disperses: its peak field amplitude changes by $0.11\\%$, its matter by $2.3\\%$, and its core moves $0.12$ toward the centre of the domain, almost all of it after $t=400$. A star of negative ADM mass thus shows no sign of instability over the evolved time.", "B"),
    ("H8", "Shirokov 2608.24577", "sh1", "v1 mass ladder (cited in RESULTS C and search_log)",
     "puts it at mass ratio $0.995\\pm0.03$, against $1.000$ predicted", "C2"),
    ("H9", "Shirokov 2608.24577", "sh1", "v1 \"What is not established\" (iii)",
     "(iii)~Stability against sideways perturbations: every release here is head-on.", "A4, B"),
    ("H10", "Shirokov 2608.24577", "sh2", "v2 discussion",
     "Releases with a transverse offset would test whether the pair is stable against sideways perturbations.", "A4, B"),
    ("V1", "Ivanov 2012", "iv_abs", "arXiv abs page (v2), abstract",
     "It is stressed that when only leading terms in the ratio of a characteristic gravitational radius to the distance between the particles are retained our elementary analysis leads to equations of motion equivalent to those derived from relativistic weak-field equations of motion of Havas and Goldberg 1962.", "C1, C2"),
    ("V2", "Ivanov 2012", "iv2", "v2 TeX, discussion before Acknowledgments",
     "Therefore, a self-consistent relativistic treatment of the problem in the next to the weak field approximation must be based on the second-order formalism of Havas and Goldberg 1962. Such an approach is left for a possible future work.", "C2"),
    ("V3", "Ivanov 2012", "iv2", "v2 TeX, after eq. (en6)",
     "In fact, as is described in standard handbooks, e.g. [6], the post-Newtonian corrections are either proportional to $\\Delta \\mu $ or $\\dot y_{1,2}$.", "C2"),
    ("V4", "Ivanov 2012", "iv2", "v2 TeX, after eq. (en6): the typo RESULTS records",
     "when the mass difference is negative and $D_{FW}=2|\\Delta \\mu |$ the particles are at rest with respect to each other.", "C1"),
    ("G1", "Singustars 2611.14482", "sg_abs", "arXiv abs page, abstract",
     "The Tolman--Oppenheimer--Volkoff equations admit singular solutions in which a negative point mass is surrounded by a self-gravitating fluid.", "A4"),
    ("G2", "Singustars 2611.14482", "sg_abs", "arXiv abs page, abstract",
     "From exact equilibria and their radial modes, we find that singustars with $\\Gamma = 2$ are stable only for $M\\lesssim0.63$ and $C\\lesssim0.25$", "A4"),
    ("G3", "Singustars 2611.14482", "sg1", "Discussion (limitations)",
     "We analyze geodesics and nonradial perturbations of \\singu{s} in a forthcoming paper.", "A4"),
    ("G4", "Singustars 2611.14482", "sg1", "Sec. on nonradial perturbations",
     "Axial gravitational perturbations ($s=2$) are then in the limit-point case and evolve uniquely, with no boundary condition.", "A2"),
]


NEG_TERMS = [("star(s)", r"\bstars?\b"), ("matter", r"\bmatter\b"), ("fluid", r"\bfluid\b"), ("Sturm", r"Sturm"), ("node(s)", r"\bnodes?\b"),
             ("truncat", r"truncat"), ("Robin", r"Robin"), ("finite radius/size", r"finite (radius|size)"), ("cap, upper bound", r"\bcap\b|upper bound"),
             ("negative mass star", r"negative mass star"), ("zero mode", r"zero mode"), ("critical", r"critical"), ("threshold", r"threshold")]


def load():
    d = {}
    for k, p in SRC.items():
        d[k] = open(p, encoding="utf-8", errors="replace").read()
    d["cao_abs"] = cao_abstract()
    d["cao_refs"] = cao_refs()
    d["par_abs"] = par_abstract_page()
    d["par_refs"] = par_refs_page()
    d["par_page"] = strip_tags(par_page())
    d["par_abs_inspire"] = par_abstract_inspire()
    d["sh_abs"] = html_text("shirokov_abs")
    d["iv_abs"] = html_text("ivanov_abs")
    d["sg_abs"] = html_text("new_2611_14482_abs")
    return d


def locate(raw, quote, is_tex):
    pat = r"\s+".join(re.escape(t) for t in quote.split())
    m = re.search(pat, raw)
    if not m:
        return None
    return raw.count("\n", 0, m.start()) + 1 if is_tex else 0


def main():
    D = load()
    L, bad = [], []
    w = L.append
    w("# I51 quotes: DG08 §V (and §IV, §III), Cao 2012, Paranjape 2025, Price 1993")
    w("")
    w("Written by `make_quotes.py` from the stored files; each quote below was found verbatim (whitespace collapsed) in its source. "
      "TeX line numbers are those of the stored `.tex` (`../I149-rpi5/dg08_v*/`). DG08 is typeset in revtex4, so sections are I to V and "
      "subsections A to D: `\\section{Summary}` is **§V** in v1, v2 and v3; `\\subsection{Intertwining operators}` is §IV A in v2 and v3 "
      "(§III in v1, which has no numerical section and no subsections). RESULTS.md's \"Sec. IV.1\" is §IV A.")
    w("")
    items = ["DG08", "Cao 2012", "Paranjape 2025", "Shirokov 2608.24577", "Ivanov 2012", "Singustars 2611.14482"]
    for it in items:
        w("## %s" % {"DG08": "Dotti–Gleiser 2008, arXiv:0809.3615 (v1 2008-09, v2 2009-06, v3 2009-09)", "Cao 2012": "Cao 2012, IJMPD 21, 1250061 (abstract and reference list only)",
                     "Paranjape 2025": "Paranjape 2025, \"Puzzles with Negative Mass\" (abstract and reference list only)",
                     "Shirokov 2608.24577": "Shirokov 2608.24577, v1 (2026-08-25) against v2 (2026-10-26): found by the rerun",
                     "Ivanov 2012": "Ivanov 2012, arXiv:1204.1269v2: the Havas–Goldberg statement (RESULTS C1, C2)",
                     "Singustars 2611.14482": "Laguna 2026-11-10, arXiv:2611.14482 (Singustars): found by the rerun"}[it])
        w("")
        for qid, item, key, loc, text, bears in Q:
            if item != it:
                continue
            raw = D[key]
            if MUT and qid == "S2":
                text = text.replace("unique", "unigue")
            line = locate(raw, text, key in SRC)
            if line is None:
                bad.append(qid)
                w("- **%s NOT FOUND** (%s, %s)" % (qid, key, loc))
                continue
            where = (" %s line %d," % (os.path.basename(SRC[key]), line)) if key in SRC else ""
            w("- **%s** [%s;%s bears on: %s] %s" % (qid, (key if key not in SRC else key) , where, bears, ("`" + text + "`")))
            w("  Section: %s." % loc)
        w("")

    # negative evidence for DG08
    w("## DG08: what was searched for and not found")
    w("")
    w("Counts are on the TeX with `%`-comments removed. A term with 0 hits in all three versions is not in the paper; contexts are "
      "printed for every hit of the other terms.")
    w("")
    w("| term | v1 | v2 | v3 | v3 §V only |")
    w("|---|---|---|---|---|")
    ctxs = []
    for name, rx in NEG_TERMS:
        row = []
        for k in ("v1", "v2", "v3"):
            t = norm(tex_nocomment(D[k]))
            hits = list(re.finditer(rx, t, re.I))
            row.append(len(hits))
            if hits and k == "v3":
                for m in hits[:6]:
                    ctxs.append("- v3 `%s`: ...%s..." % (name, t[max(0, m.start() - 110):m.end() + 110]))
        t3 = norm(tex_nocomment(D["v3"]))
        sec5 = t3[t3.index("\\section{Summary}"):t3.index("\\section*{Acknowledgments}")]
        w("| %s | %d | %d | %d | %d |" % (name, row[0], row[1], row[2], len(re.findall(rx, sec5, re.I))))
    w("")
    w("Contexts of the v3 hits:")
    w("")
    L.extend(ctxs)
    w("")

    # where each source was sought: from fetch.log
    w("## Places sought and their status (from `fetch.log`)")
    w("")
    w("| item | URL | HTTP | what it returned |")
    w("|---|---|---|---|")
    for ln in open(os.path.join(HERE, "fetch.log")):
        p = [x.strip() for x in ln.split("|")]
        if len(p) < 5:
            continue
        d = p[3].split("/")[0]
        if not d.startswith(("price_", "cao_", "par_", "s2_", "fatcat_", "sec_")):
            continue
        item = {"price": "Price 1993", "cao": "Cao 2012", "par": "Paranjape 2025", "s2": "Semantic Scholar", "fatcat": "fatcat", "sec": "secondary"}[d.split("_")[0]]
        meta = p[1].split(" ")
        w("| %s | `%s` | %s | %s |" % (item, p[2][:150], meta[0], " ".join(meta[1:])))
    w("")
    open(os.path.join(HERE, "quotes.md"), "w").write("\n".join(L) + "\n")
    if bad:
        print("NOT FOUND:", ", ".join(bad))
        sys.exit(1)
    print("all %d quotes found" % len(Q))


main()
