"""Protein analysis with BioPython: composition, properties, hydrophobicity,
region detection, motif detection."""
import io, math, os, re, subprocess, tempfile
from collections import Counter

import pandas as pd
from Bio import SeqIO
from Bio.SeqUtils import ProtParamData
from Bio.SeqUtils.ProtParam import ProteinAnalysis

AA = "ACDEFGHIKLMNPQRSTVWY"
GROUPS = {
    "Hydrophobic": "AVILMFWC",
    "Polar": "STNQGPHY",
    "Positive": "KR",
    "Negative": "DE",
}

# ---------- 1. Parsing (Perl first, Python fallback) ----------
def parse_fasta(text: str):
    """Returns (DataFrame, engine_used). Uses the Perl/BioPerl script if available."""
    here = os.path.dirname(os.path.abspath(__file__))
    with tempfile.NamedTemporaryFile("w", suffix=".fasta", delete=False) as f:
        f.write(text)
        path = f.name
    try:
        out = subprocess.run(
            ["perl", os.path.join(here, "perl", "parse_fasta.pl"), path],
            capture_output=True, text=True, timeout=60, check=True,
        ).stdout
        df = pd.read_csv(io.StringIO(out), sep="\t", keep_default_na=False)
        return df, "Perl / BioPerl"
    except Exception:
        rows = []
        for r in SeqIO.parse(path, "fasta"):
            raw = str(r.seq).upper()
            clean = re.sub(f"[^{AA}]", "", raw)
            rows.append(dict(id=r.id, description=r.description, raw_length=len(raw),
                             clean_length=len(clean), removed_chars=len(raw) - len(clean),
                             cleaned_seq=clean))
        return pd.DataFrame(rows), "Python fallback (BioPython)"
    finally:
        os.unlink(path)

# ---------- 2. Composition & properties ----------
def composition(seq):
    c, n = Counter(seq), len(seq)
    return pd.DataFrame({"aa": list(AA), "count": [c[a] for a in AA],
                         "percent": [100 * c[a] / n for a in AA]})

def group_composition(seq):
    n = len(seq)
    return pd.DataFrame({"group": list(GROUPS),
                         "percent": [100 * sum(seq.count(a) for a in g) / n for g in GROUPS.values()]})

def properties(seq):
    pa = ProteinAnalysis(seq)
    ss = pa.secondary_structure_fraction()
    return {
        "Length (aa)": len(seq),
        "Molecular weight (Da)": round(pa.molecular_weight(), 1),
        "Isoelectric point (pI)": round(pa.isoelectric_point(), 2),
        "Charge at pH 7": round(pa.charge_at_pH(7.0), 2),
        "GRAVY (hydropathy)": round(pa.gravy(), 3),
        "Aromaticity": round(pa.aromaticity(), 3),
        "Instability index": round(pa.instability_index(), 1),
        "Stability": "stable" if pa.instability_index() < 40 else "unstable",
        "Helix fraction": round(ss[0], 3),
        "Turn fraction": round(ss[1], 3),
        "Sheet fraction": round(ss[2], 3),
    }

# ---------- 3. Profiles ----------
def hydrophobicity_profile(seq, window=9):
    window = min(window, len(seq))
    vals = ProteinAnalysis(seq).protein_scale(ProtParamData.kd, window, 1.0)
    pos = [i + window // 2 + 1 for i in range(len(vals))]
    return pd.DataFrame({"position": pos, "kd": vals})

def _entropy(w):
    n = len(w)
    return -sum((c / n) * math.log2(c / n) for c in Counter(w).values())

# ---------- 4. Region detection ----------
def _segments(mask, min_len):
    segs, start = [], None
    for i, m in enumerate(list(mask) + [False]):
        if m and start is None:
            start = i
        elif not m and start is not None:
            if i - start >= min_len:
                segs.append((start + 1, i))          # 1-based inclusive
            start = None
    return segs

def _window_mask(seq, w, test):
    mask = [False] * len(seq)
    for i in range(len(seq) - w + 1):
        if test(seq[i:i + w]):
            for j in range(i, i + w):
                mask[j] = True
    return mask

def detect_regions(seq, tm_window=19, tm_cutoff=1.6, lc_window=12, lc_cutoff=2.2, charge_cutoff=0.4):
    regions = []
    if len(seq) >= tm_window:
        prof = ProteinAnalysis(seq).protein_scale(ProtParamData.kd, tm_window, 1.0)
        mask = [False] * len(seq)
        for i, v in enumerate(prof):
            if v >= tm_cutoff:
                for j in range(i, i + tm_window):
                    mask[j] = True
        regions += [("Hydrophobic / TM-like", s, e) for s, e in _segments(mask, 15)]
    if len(seq) >= lc_window:
        m = _window_mask(seq, lc_window, lambda w: _entropy(w) < lc_cutoff)
        regions += [("Low complexity", s, e) for s, e in _segments(m, 10)]
    if len(seq) >= 15:
        m = _window_mask(seq, 15, lambda w: sum(w.count(a) for a in "DEKR") / 15 >= charge_cutoff)
        regions += [("Charged-rich", s, e) for s, e in _segments(m, 15)]
    rows = []
    for name, s, e in regions:
        sub = seq[s - 1:e]
        rows.append(dict(region=name, start=s, end=e, length=e - s + 1,
                         gravy=round(ProteinAnalysis(sub).gravy(), 2), sequence=sub))
    return pd.DataFrame(rows, columns=["region", "start", "end", "length", "gravy", "sequence"])

# ---------- 5. Motif detection ----------
MOTIFS = {
    "N-glycosylation (N-x-S/T)": r"N[^P][ST][^P]",
    "PKC phosphorylation": r"[ST].[RK]",
    "CK2 phosphorylation": r"[ST]..[DE]",
    "RGD cell attachment": r"RGD",
    "Nuclear localization (K-K/R-x-K/R)": r"K[KR].[KR]",
    "Walker A (P-loop)": r"[AG]....GK[ST]",
    "C2H2 zinc finger": r"C.{2,4}C.{12}H.{3,5}H",
    "KDEL ER retention (C-term)": r"[KH]DEL$",
}

def detect_motifs(seq):
    rows = []
    for name, pat in MOTIFS.items():
        for m in re.finditer(f"(?=({pat}))", seq):    # lookahead => overlapping hits
            hit = m.group(1)
            rows.append(dict(motif=name, start=m.start() + 1, end=m.start() + len(hit), match=hit))
    return pd.DataFrame(rows, columns=["motif", "start", "end", "match"])
