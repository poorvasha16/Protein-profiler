import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

import analysis as an


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Protein Profiler",
    page_icon="🧬",
    layout="wide"
)


# =========================================================
# CUSTOM DESIGN / CSS
# =========================================================

st.markdown("""
<style>

/* ---------- MAIN BACKGROUND ---------- */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #dbeafe 0%, transparent 25%),
        radial-gradient(circle at 90% 10%, #fce7f3 0%, transparent 25%),
        radial-gradient(circle at 50% 100%, #ccfbf1 0%, transparent 30%),
        linear-gradient(135deg, #f8fbff 0%, #f0fdfa 100%);
}


/* ---------- MAIN CONTENT ---------- */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}


/* ---------- MAIN TITLE ---------- */

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 850;
    margin-bottom: 8px;

    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed,
        #db2777,
        #0891b2
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #64748b;
    margin-bottom: 28px;
}


/* ---------- BIOLOGY CARDS ---------- */

.bio-card {
    border-radius: 22px;
    padding: 20px;
    text-align: center;
    min-height: 175px;

    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.10);

    transition: transform 0.2s ease;
}

.bio-card:hover {
    transform: translateY(-4px);
}

.dna-card {
    background: linear-gradient(135deg, #dbeafe, #eff6ff);
    border: 2px solid #93c5fd;
}

.rna-card {
    background: linear-gradient(135deg, #fce7f3, #fff1f2);
    border: 2px solid #f9a8d4;
}

.protein-card {
    background: linear-gradient(135deg, #ccfbf1, #ecfeff);
    border: 2px solid #5eead4;
}

.bio-icon {
    font-size: 58px;
    margin-bottom: 5px;
}

.bio-title {
    font-size: 22px;
    font-weight: 800;
    color: #1e293b;
}

.bio-text {
    font-size: 14px;
    color: #64748b;
}


/* ---------- INPUT CARD ---------- */

.input-card {
    background: rgba(255,255,255,0.90);
    border: 2px solid #bfdbfe;
    border-radius: 22px;
    padding: 24px;
    margin-top: 25px;
    margin-bottom: 25px;

    box-shadow: 0 10px 30px rgba(37,99,235,0.10);
}

.input-title {
    font-size: 25px;
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 5px;
}

.input-description {
    color: #64748b;
    font-size: 15px;
}


/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #dbeafe 0%,
        #e0f2fe 45%,
        #ccfbf1 100%
    );
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #075985;
    font-weight: 800;
}


/* ---------- BUTTONS ---------- */

.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    border: 1px solid #60a5fa;

    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );

    color: white;
}

.stButton > button:hover {
    border-color: #7c3aed;
    color: white;
}


/* ---------- METRICS ---------- */

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.95);
    border-radius: 18px;
    padding: 18px;

    border: 2px solid #bfdbfe;

    box-shadow: 0 6px 18px rgba(15,23,42,0.08);
}

div[data-testid="stMetricLabel"] {
    color: #475569;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #2563eb;
    font-weight: 800;
}


/* ---------- TABS ---------- */

button[data-baseweb="tab"] {
    font-weight: 700;
    font-size: 15px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #2563eb;
    border-bottom: 4px solid #2563eb;
}


/* ---------- DATA TABLE ---------- */

div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #cbd5e1;
}


/* ---------- ALERTS ---------- */

div[data-testid="stAlert"] {
    border-radius: 14px;
}


/* ---------- SELECT BOX ---------- */

div[data-baseweb="select"] > div {
    border-radius: 12px;
}


/* ---------- TEXT AREA ---------- */

textarea {
    border-radius: 12px !important;
}


/* ---------- FILE UPLOADER ---------- */

section[data-testid="stFileUploaderDropzone"] {
    border-radius: 15px;
    border: 2px dashed #60a5fa;
    background: #eff6ff;
}


/* ---------- SECTION HEADINGS ---------- */

h2, h3 {
    color: #0f766e;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🧬 Protein Profiler</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive Protein Sequence Profiling & Region Mapping'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DNA / RNA / PROTEIN VISUAL CARDS
# =========================================================

d1, d2, d3 = st.columns(3)

with d1:
    st.markdown("""
    <div class="bio-card dna-card">
        <div class="bio-icon">🧬</div>
        <div class="bio-title">DNA</div>
        <div class="bio-text">
            Genetic information and nucleotide sequences
        </div>
    </div>
    """, unsafe_allow_html=True)

with d2:
    st.markdown("""
    <div class="bio-card rna-card">
        <div class="bio-icon">🧪</div>
        <div class="bio-title">RNA</div>
        <div class="bio-text">
            Transcription and functional RNA molecules
        </div>
    </div>
    """, unsafe_allow_html=True)

with d3:
    st.markdown("""
    <div class="bio-card protein-card">
        <div class="bio-icon">🧬</div>
        <div class="bio-title">Protein</div>
        <div class="bio-text">
            Sequence, structure, properties and functional regions
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SAMPLE FASTA
# =========================================================

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


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown("""
<div class="input-card">
    <div class="input-title">🔬 Input Protein Sequence</div>
    <div class="input-description">
        Upload a FASTA file or paste your protein sequence below to begin analysis.
    </div>
</div>
""", unsafe_allow_html=True)


input_col1, input_col2 = st.columns(2)

with input_col1:
    up = st.file_uploader(
        "📂 Upload FASTA file",
        type=["fasta", "fa", "faa", "txt"]
    )

with input_col2:
    pasted = st.text_area(
        "📝 Or paste FASTA sequence",
        height=120,
        placeholder="Example:\n>Protein_1\nMVLSPADKTNVKAAWGKV..."
    )


button_col1, button_col2, button_col3 = st.columns([1, 1, 1])

with button_col2:
    load_sample = st.button(
        "🧬 Load Sample Proteins",
        use_container_width=True
    )


# =========================================================
# SIDEBAR PARAMETERS
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Analysis Parameters")

    st.markdown("---")

    st.markdown("### 🌊 Hydropathy")

    kd_window = st.slider(
        "Hydropathy window",
        5,
        25,
        9,
        2
    )

    tm_cut = st.slider(
        "Hydrophobic region cutoff (KD)",
        1.0,
        2.5,
        1.6,
        0.1
    )

    st.markdown("---")

    st.markdown("### 🧩 Complexity")

    lc_cut = st.slider(
        "Low-complexity entropy cutoff (bits)",
        1.5,
        3.5,
        2.2,
        0.1
    )

    st.markdown("---")

    st.info(
        "Adjust these parameters to change the detected protein regions "
        "and hydropathy analysis."
    )


# =========================================================
# INPUT HANDLING
# =========================================================

if up:
    text = up.getvalue().decode()

elif pasted.strip():
    text = pasted

elif load_sample:
    text = SAMPLE

elif st.session_state.get("sample"):
    text = SAMPLE

else:
    text = ""


# =========================================================
# START MESSAGE
# =========================================================

if not text.strip():

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #dbeafe, #ecfeff);
        border: 1px solid #93c5fd;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        margin-top: 20px;
        color: #075985;
        font-weight: 600;
    ">
        🧬 Upload or paste a protein FASTA sequence above to begin analysis.
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# =========================================================
# FASTA PARSING
# =========================================================

@st.cache_data(show_spinner="🔬 Parsing FASTA…")
def load(t):
    return an.parse_fasta(t)


df, engine = load(text)

df = df[df.clean_length > 0].reset_index(drop=True)


if df.empty:

    st.error("❌ No valid protein sequences found.")

    st.stop()


st.success(f"✅ FASTA successfully parsed using **{engine}**")


# =========================================================
# SEQUENCE SELECTION
# =========================================================

st.markdown("### 🧬 Select Protein Sequence")

choice = st.selectbox(
    "Choose a protein for detailed analysis",
    df.id
)

row = df[df.id == choice].iloc[0]

seq = row.cleaned_seq


if len(seq) < 10:

    st.warning(
        "⚠️ Sequence is very short; results may be limited."
    )


# =========================================================
# ANALYSIS
# =========================================================

comp = an.composition(seq)

props = an.properties(seq)

regions = an.detect_regions(
    seq,
    tm_cutoff=tm_cut,
    lc_cutoff=lc_cut
)

motifs = an.detect_motifs(seq)

hydro = an.hydrophobicity_profile(
    seq,
    kd_window
)


# =========================================================
# TABS
# =========================================================

t1, t2, t3, t4, t5 = st.tabs([
    "📋 Overview",
    "🔬 Fingerprint",
    "🗺️ Protein Map",
    "📑 Regions & Motifs",
    "📈 Graphs"
])


# =========================================================
# OVERVIEW
# =========================================================

with t1:

    st.subheader(row.id)

    st.write(row.description)

    c = st.columns(4)

    c[0].metric(
        "🧬 Cleaned Length",
        row.clean_length
    )

    c[1].metric(
        "✂️ Removed Characters",
        row.removed_chars
    )

    c[2].metric(
        "⚖️ MW (kDa)",
        round(
            props["Molecular weight (Da)"] / 1000,
            2
        )
    )

    c[3].metric(
        "⚡ pI",
        props["Isoelectric point (pI)"]
    )

    st.markdown("### 🔎 Protein Properties")

    st.dataframe(
        pd.DataFrame(
            props.items(),
            columns=["Property", "Value"]
        ).astype(str),
        hide_index=True,
        use_container_width=True
    )

    st.markdown("### 📊 All Sequences in File")

    st.dataframe(
        df.drop(columns="cleaned_seq"),
        hide_index=True,
        use_container_width=True
    )


# =========================================================
# FINGERPRINT
# =========================================================

with t2:

    a, b = st.columns(2)

    # Radar chart
    radar = go.Figure(
        go.Scatterpolar(
            r=list(comp.percent) + [comp.percent[0]],
            theta=list(comp.aa) + [comp.aa[0]],
            fill="toself"
        )
    )

    radar.update_layout(
        title="🧬 Amino-acid Fingerprint (%)",
        height=420,
        polar=dict(
            radialaxis=dict(
                visible=True
            )
        )
    )

    a.plotly_chart(
        radar,
        use_container_width=True
    )


    # Pie chart
    g = an.group_composition(seq)

    pie = px.pie(
        g,
        names="group",
        values="percent",
        hole=0.45,
        title="🧪 Physicochemical Groups"
    )

    b.plotly_chart(
        pie,
        use_container_width=True
    )


    # Positional fingerprint
    st.markdown("### 🧩 Positional Fingerprint")

    nb = min(
        60,
        len(seq)
    )

    edges = np.linspace(
        0,
        len(seq),
        nb + 1,
        dtype=int
    )

    mat = np.array([
        [
            seq[
                edges[i]:
                edges[i + 1]
            ].count(x)
            /
            max(
                1,
                edges[i + 1] - edges[i]
            )

            for i in range(nb)
        ]

        for x in an.AA
    ])

    hm = px.imshow(
        mat,

        x=[
            f"{edges[i]+1}-{edges[i+1]}"
            for i in range(nb)
        ],

        y=list(an.AA),

        aspect="auto",

        color_continuous_scale="Viridis",

        title="Residue Frequency Along the Sequence"
    )

    st.plotly_chart(
        hm,
        use_container_width=True
    )


# =========================================================
# PROTEIN MAP
# =========================================================

with t3:

    st.markdown("### 🗺️ Interactive Protein Region Map")

    COL = {
        "Hydrophobic / TM-like": "#f97316",
        "Low complexity": "#8b5cf6",
        "Charged-rich": "#0ea5e9"
    }

    lanes = list(COL) + ["Motifs"]

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.55, 0.45],
        vertical_spacing=0.04
    )


    fig.add_shape(
        type="rect",
        x0=1,
        x1=len(seq),
        y0=-0.05,
        y1=0.05,
        fillcolor="#cbd5e1",
        line_width=0,
        row=1,
        col=1
    )


    for r in regions.itertuples():

        y = lanes.index(r.region) + 1

        fig.add_trace(
            go.Scatter(
                x=[
                    r.start,
                    r.end,
                    r.end,
                    r.start,
                    r.start
                ],

                y=[
                    y - .35,
                    y - .35,
                    y + .35,
                    y + .35,
                    y - .35
                ],

                fill="toself",

                mode="lines",

                line=dict(
                    color=COL[r.region]
                ),

                name=r.region,

                legendgroup=r.region,

                showlegend=False,

                hovertext=(
                    f"{r.region}<br>"
                    f"{r.start}-{r.end}<br>"
                    f"GRAVY: {r.gravy}"
                ),

                hoverinfo="text"
            ),

            row=1,
            col=1
        )


    if not motifs.empty:

        fig.add_trace(
            go.Scatter(

                x=(
                    motifs.start +
                    motifs.end
                ) / 2,

                y=[
                    len(lanes)
                ] * len(motifs),

                mode="markers",

                marker=dict(
                    size=11,
                    symbol="diamond",
                    color="#e11d48"
                ),

                text=(
                    motifs.motif
                    + " "
                    + motifs.match
                    + " @"
                    + motifs.start.astype(str)
                ),

                hoverinfo="text",

                name="Motifs"
            ),

            row=1,
            col=1
        )


    fig.update_yaxes(
        tickvals=list(
            range(
                1,
                len(lanes) + 1
            )
        ),

        ticktext=lanes,

        range=[
            -0.6,
            len(lanes) + .6
        ],

        row=1,
        col=1
    )


    fig.add_trace(
        go.Scatter(
            x=hydro.position,
            y=hydro.kd,
            line=dict(
                color="#059669",
                width=3
            ),
            name="Kyte-Doolittle"
        ),

        row=2,
        col=1
    )


    fig.add_hline(
        y=0,
        line_dash="dot",
        row=2,
        col=1
    )


    fig.update_xaxes(
        title_text="Residue Position",
        row=2,
        col=1
    )

    fig.update_yaxes(
        title_text="Hydropathy",
        row=2,
        col=1
    )


    fig.update_layout(
        height=620,
        showlegend=False,
        title=f"Interactive Map — {row.id}"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.caption(
        "💡 Hover for details • Drag to zoom • Double-click to reset"
    )


# =========================================================
# REGIONS & MOTIFS
# =========================================================

with t4:

    st.subheader("🧩 Detected Regions")

    if not regions.empty:

        st.dataframe(
            regions,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "No regions detected with the current thresholds."
        )


    st.subheader("🎯 Detected Motifs")

    if not motifs.empty:

        st.dataframe(
            motifs,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "No motifs found."
        )


# =========================================================
# GRAPHS
# =========================================================

with t5:

    st.subheader("📊 Amino-acid Composition")

    bar = px.bar(
        comp,
        x="aa",
        y="percent",
        title="Amino-acid Composition (%)",
        color="percent",
        color_continuous_scale="Tealgrn"
    )

    st.plotly_chart(
        bar,
        use_container_width=True
    )


    st.subheader("🌊 Hydropathy Profile")

    line = px.line(
        hydro,
        x="position",
        y="kd",
        title=f"Hydropathy Profile — Window {kd_window}"
    )

    st.plotly_chart(
        line,
        use_container_width=True
    )


    if len(df) > 1:

        st.subheader("🔬 Multi-sequence Comparison")

        rows = []

        for r in df.itertuples():

            p = an.properties(
                r.cleaned_seq
            )

            rows.append(
                dict(
                    id=r.id,
                    length=p["Length (aa)"],
                    pI=p["Isoelectric point (pI)"],
                    gravy=p["GRAVY (hydropathy)"],
                    mw=p["Molecular weight (Da)"]
                )
            )


        comparison_df = pd.DataFrame(rows)


        scatter = px.scatter(
            comparison_df,
            x="pI",
            y="gravy",
            size="mw",
            hover_name="id",
            title="Multi-sequence Comparison (Size = Molecular Weight)"
        )


        st.plotly_chart(
            scatter,
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<hr>

<div style="
    text-align:center;
    color:#64748b;
    padding:15px;
    font-size:14px;
">

🧬 <b>Protein Profiler</b> |
Sequence Analysis • Protein Properties • Hydropathy • Motifs • Region Mapping

</div>
""", unsafe_allow_html=True)
