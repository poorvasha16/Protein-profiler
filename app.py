import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

import analysis as an

st.set_page_config(page_title="Protein Profiler", page_icon="🧬", layout="wide")
st.title("🧬 Interactive Protein Sequence Profiling & Region Mapping")

SAMPLE = """>sp|P69905|HBA_HUMAN Hemoglobin subunit alpha
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG
KKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTP
AVHASLDKFLASVSTVLTSKYR
>sp|P04637|P53_HUMAN (fragment) Cellular tumor antigen p53
MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGP
DEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYQGSYGFRLGFLHSGTAK
SVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHE
RCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNS
SCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEENLRKKGEPHHELP
PGSTKRALPNNTSSSPQPKKKPLDGEYFTLQIRGRERFEMFRELNEALELKDAQAGKEPG
GSRAHSSHLKSKKGQSTSRHKKLMFKTEGPDSD
"""

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Input")
    up = st.file_uploader("Upload FASTA", type=["fasta", "fa", "faa", "txt"])
    pasted = st.text_area("…or paste FASTA", height=120)
    if st.button("Load sample proteins"):
        st.session_state["sample"] = True
    st.header("Parameters")
    kd_window = st.slider("Hydropathy window", 5, 25, 9, 2)
    tm_cut = st.slider("Hydrophobic region cutoff (KD)", 1.0, 2.5, 1.6, 0.1)
    lc_cut = st.slider("Low-complexity entropy cutoff (bits)", 1.5, 3.5, 2.2, 0.1)

text = up.getvalue().decode() if up else pasted or (SAMPLE if st.session_state.get("sample") else "")
if not text.strip():
    st.info("Upload or paste a protein FASTA file (or click **Load sample proteins**) to begin.")
    st.stop()


@st.cache_data(show_spinner="Parsing FASTA…")
def load(t):
    return an.parse_fasta(t)


df, engine = load(text)
df = df[df.clean_length > 0].reset_index(drop=True)
if df.empty:
    st.error("No valid protein sequences found.")
    st.stop()
st.caption(f"Parsed with: **{engine}**")

choice = st.selectbox("Select sequence", df.id)
row = df[df.id == choice].iloc[0]
seq = row.cleaned_seq
if len(seq) < 10:
    st.warning("Sequence is very short; results may be limited.")

comp = an.composition(seq)
props = an.properties(seq)
regions = an.detect_regions(seq, tm_cutoff=tm_cut, lc_cutoff=lc_cut)
motifs = an.detect_motifs(seq)
hydro = an.hydrophobicity_profile(seq, kd_window)

t1, t2, t3, t4, t5 = st.tabs(["📋 Overview", "🔬 Fingerprint", "🗺️ Protein map", "📑 Regions & motifs", "📈 Graphs"])

# ---------------- Overview ----------------
with t1:
    st.subheader(row.id)
    st.write(row.description)
    c = st.columns(4)
    c[0].metric("Cleaned length", row.clean_length)
    c[1].metric("Removed characters", row.removed_chars)
    c[2].metric("MW (kDa)", round(props["Molecular weight (Da)"] / 1000, 2))
    c[3].metric("pI", props["Isoelectric point (pI)"])
    st.dataframe(pd.DataFrame(props.items(), columns=["Property", "Value"]).astype(str),
                 hide_index=True, use_container_width=True)
    st.markdown("**All sequences in file (Perl-cleaned stats)**")
    st.dataframe(df.drop(columns="cleaned_seq"), hide_index=True, use_container_width=True)

# ---------------- Fingerprint ----------------
with t2:
    a, b = st.columns(2)
    radar = go.Figure(go.Scatterpolar(r=list(comp.percent) + [comp.percent[0]],
                                      theta=list(comp.aa) + [comp.aa[0]], fill="toself"))
    radar.update_layout(title="Amino-acid fingerprint (% composition)", height=420,
                        polar=dict(radialaxis=dict(visible=True)))
    a.plotly_chart(radar, use_container_width=True)
    g = an.group_composition(seq)
    b.plotly_chart(px.pie(g, names="group", values="percent", hole=0.45,
                          title="Physicochemical groups"), use_container_width=True)

    # positional fingerprint: residue type x sequence bin
    nb = min(60, len(seq))
    edges = np.linspace(0, len(seq), nb + 1, dtype=int)
    mat = np.array([[seq[edges[i]:edges[i + 1]].count(x) / max(1, edges[i + 1] - edges[i])
                     for i in range(nb)] for x in an.AA])
    hm = px.imshow(mat, x=[f"{edges[i]+1}-{edges[i+1]}" for i in range(nb)], y=list(an.AA),
                   aspect="auto", color_continuous_scale="Viridis",
                   title="Positional fingerprint (residue frequency along the sequence)")
    st.plotly_chart(hm, use_container_width=True)

# ---------------- Protein map ----------------
with t3:
    COL = {"Hydrophobic / TM-like": "#e67e22", "Low complexity": "#8e44ad", "Charged-rich": "#2980b9"}
    lanes = list(COL) + ["Motifs"]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.55, 0.45],
                        vertical_spacing=0.04)
    fig.add_shape(type="rect", x0=1, x1=len(seq), y0=-0.05, y1=0.05, fillcolor="#bbb",
                  line_width=0, row=1, col=1)
    for r in regions.itertuples():
        y = lanes.index(r.region) + 1
        fig.add_trace(go.Scatter(x=[r.start, r.end, r.end, r.start, r.start],
                                 y=[y - .35, y - .35, y + .35, y + .35, y - .35], fill="toself",
                                 mode="lines", line=dict(color=COL[r.region]), name=r.region,
                                 legendgroup=r.region, showlegend=False,
                                 hovertext=f"{r.region}<br>{r.start}-{r.end} (GRAVY {r.gravy})",
                                 hoverinfo="text"), row=1, col=1)
    if not motifs.empty:
        fig.add_trace(go.Scatter(x=(motifs.start + motifs.end) / 2, y=[len(lanes)] * len(motifs),
                                 mode="markers", marker=dict(size=10, symbol="diamond", color="#c0392b"),
                                 text=motifs.motif + " " + motifs.match + " @" + motifs.start.astype(str),
                                 hoverinfo="text", name="Motifs"), row=1, col=1)
    fig.update_yaxes(tickvals=list(range(1, len(lanes) + 1)), ticktext=lanes, range=[-0.6, len(lanes) + .6],
                     row=1, col=1)
    fig.add_trace(go.Scatter(x=hydro.position, y=hydro.kd, line=dict(color="#16a085"),
                             name="Kyte-Doolittle"), row=2, col=1)
    fig.add_hline(y=0, line_dash="dot", row=2, col=1)
    fig.update_xaxes(title_text="Residue position", row=2, col=1)
    fig.update_yaxes(title_text="Hydropathy", row=2, col=1)
    fig.update_layout(height=620, showlegend=False, title=f"Interactive map — {row.id}")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Hover for details · drag to zoom · double-click to reset.")

# ---------------- Regions & motifs ----------------
with t4:
    st.subheader("Detected regions")
    st.dataframe(regions, hide_index=True, use_container_width=True) if not regions.empty \
        else st.write("No regions detected with the current thresholds.")
    st.subheader("Detected motifs")
    st.dataframe(motifs, hide_index=True, use_container_width=True) if not motifs.empty \
        else st.write("No motifs found.")
    d1, d2 = st.columns(2)
    d1.download_button("Download regions CSV", regions.to_csv(index=False), f"{choice}_regions.csv")
    d2.download_button("Download motifs CSV", motifs.to_csv(index=False), f"{choice}_motifs.csv")

# ---------------- Graphs ----------------
with t5:
    st.plotly_chart(px.bar(comp, x="aa", y="percent", title="Amino-acid composition (%)",
                           color="percent", color_continuous_scale="Tealgrn"), use_container_width=True)
    st.plotly_chart(px.line(hydro, x="position", y="kd",
                            title=f"Hydropathy profile (window {kd_window})"), use_container_width=True)
    if len(df) > 1:
        rows = []
        for r in df.itertuples():
            p = an.properties(r.cleaned_seq)
            rows.append(dict(id=r.id, length=p["Length (aa)"], pI=p["Isoelectric point (pI)"],
                             gravy=p["GRAVY (hydropathy)"], mw=p["Molecular weight (Da)"]))
        st.plotly_chart(px.scatter(pd.DataFrame(rows), x="pI", y="gravy", size="mw", hover_name="id",
                                   title="Multi-sequence comparison (size = MW)"), use_container_width=True)
