import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

import analysis as an


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Protein Profiler",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM DESIGN / COLOURS
# ============================================================

st.markdown("""
<style>

    /* ---------- MAIN BACKGROUND ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, #eef2ff 0%, transparent 28%),
            radial-gradient(circle at 90% 10%, #ecfeff 0%, transparent 28%),
            linear-gradient(135deg, #f8faff 0%, #effcff 50%, #f5f3ff 100%);
    }


    /* ---------- MAIN CONTENT ---------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* ---------- TITLE ---------- */

    .main-title {
        font-size: 3rem;
        font-weight: 850;
        color: #172554;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }


    /* ---------- PROTEIN HEADER ---------- */

    .protein-banner {
        background: linear-gradient(
            135deg,
            #dbeafe 0%,
            #e0f2fe 45%,
            #ccfbf1 100%
        );

        border: 1px solid #bae6fd;
        border-radius: 22px;
        padding: 22px 28px;
        margin-bottom: 22px;

        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.08);
    }

    .protein-banner-title {
        font-size: 1.35rem;
        font-weight: 750;
        color: #075985;
        margin-bottom: 5px;
    }

    .protein-banner-text {
        color: #475569;
        font-size: 0.95rem;
    }


    /* ---------- INPUT CARD ---------- */

    .input-card {
        background: rgba(255,255,255,0.92);
        border: 1px solid #c7d2fe;
        border-radius: 20px;
        padding: 22px;
        margin-top: 10px;
        margin-bottom: 25px;

        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.07);
    }

    .input-title {
        font-size: 1.25rem;
        font-weight: 750;
        color: #3730a3;
        margin-bottom: 12px;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #e0f2fe 0%,
                #dbeafe 45%,
                #ccfbf1 100%
            );
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #075985;
    }


    /* ---------- METRIC CARDS ---------- */

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.95);
        border-radius: 17px;
        padding: 18px;

        border: 1px solid #bfdbfe;

        box-shadow:
            0 6px 18px rgba(15, 23, 42, 0.07);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #2563eb;
        font-weight: 800;
    }


    /* ---------- TABS ---------- */

    button[data-baseweb="tab"] {
        font-weight: 700;
        font-size: 0.95rem;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563eb;
        border-bottom: 3px solid #2563eb;
    }


    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        border: 1px solid #93c5fd;
        background: linear-gradient(
            135deg,
            #eff6ff,
            #ecfeff
        );
        color: #1d4ed8;
    }

    .stButton > button:hover {
        border-color: #2563eb;
        color: #1e40af;
    }


    /* ---------- DATAFRAMES ---------- */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #dbeafe;
    }


    /* ---------- ALERTS ---------- */

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }


    /* ---------- SELECT BOX ---------- */

    div[data-baseweb="select"] > div {
        border-radius: 12px;
        border-color: #bfdbfe;
    }


    /* ---------- TEXT AREA ---------- */

    textarea {
        border-radius: 12px !important;
    }


    /* ---------- FILE UPLOADER ---------- */

    div[data-testid="stFileUploader"] {
        background: #f8fafc;
        border-radius: 14px;
        padding: 8px;
        border: 1px solid #dbeafe;
    }


    /* ---------- SECTION HEADERS ---------- */

    .section-heading {
        font-size: 1.35rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-top: 10px;
        margin-bottom: 12px;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 35px;
        padding-top: 18px;
        border-top: 1px solid #dbeafe;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧬 Protein Profiler</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive protein sequence profiling, physicochemical analysis, '
    'hydropathy mapping and motif detection.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PROTEIN BANNER
# ============================================================

st.markdown("""
<div class="protein-banner">

    <div class="protein-banner-title">
        🔬 Protein Sequence Analysis
    </div>

    <div class="protein-banner-text">
        Explore amino-acid composition, molecular properties,
        hydrophobic regions, low-complexity regions and sequence motifs
        from your protein FASTA sequence.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SAMPLE PROTEINS
# ============================================================

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


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="input-card">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="input-title">📥 Protein Sequence Input</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload a FASTA file or paste your protein sequence below."
)

col1, col2 = st.columns(2)

with col1:

    up = st.file_uploader(
        "Upload FASTA",
        type=["fasta", "fa", "faa", "txt"]
    )

with col2:

    pasted = st.text_area(
        "Paste FASTA sequence",
        height=110,
        placeholder=(
            ">Protein_ID Protein_name\n"
            "MKTIIALSYIFCLVFADYKDDDD..."
        )
    )

sample_col1, sample_col2, sample_col3 = st.columns([1, 1, 3])

with sample_col1:

    if st.button(
        "🧪 Load sample proteins",
        use_container_width=True
    ):
        st.session_state["sample"] = True

with sample_col2:

    if st.button(
        "🗑️ Clear input",
        use_container_width=True
    ):
        st.session_state["sample"] = False

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# SIDEBAR PARAMETERS
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Analysis Parameters")

    st.write(
        "Adjust the parameters used for protein region detection."
    )

    st.markdown("---")

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

    lc_cut = st.slider(
        "Low-complexity entropy cutoff (bits)",
        1.5,
        3.5,
        2.2,
        0.1
    )

    st.markdown("---")

    st.markdown(
        "### 🧬 What is analysed?"
    )

    st.markdown("""
    - Amino-acid composition
    - Molecular weight
    - Isoelectric point
    - GRAVY
    - Hydropathy
    - Protein regions
    - Sequence motifs
    - Low-complexity regions
    """)


# ============================================================
# GET INPUT
# ============================================================

text = (
    up.getvalue().decode()
    if up
    else pasted
    or (SAMPLE if st.session_state.get("sample") else "")
)


if not text.strip():

    st.info(
        "👆 Upload or paste a protein FASTA sequence above "
        "to begin the analysis."
    )

    st.stop()


# ============================================================
# FASTA PARSING
# ============================================================

@st.cache_data(show_spinner="🔬 Parsing FASTA sequence…")
def load(t):

    return an.parse_fasta(t)


df, engine = load(text)

df = df[
    df.clean_length > 0
].reset_index(drop=True)


if df.empty:

    st.error(
        "No valid protein sequences were found."
    )

    st.stop()


st.success(
    f"✅ FASTA successfully parsed using **{engine}**"
)


# ============================================================
# SEQUENCE SELECTION
# ============================================================

choice = st.selectbox(
    "🧬 Select protein sequence",
    df.id
)

row = df[
    df.id == choice
].iloc[0]

seq = row.cleaned_seq


if len(seq) < 10:

    st.warning(
        "⚠️ Sequence is very short; results may be limited."
    )


# ============================================================
# ANALYSIS
# ============================================================

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


# ============================================================
# TABS
# ============================================================

t1, t2, t3, t4, t5 = st.tabs([
    "📋 Overview",
    "🔬 Fingerprint",
    "🗺️ Protein Map",
    "📑 Regions & Motifs",
    "📈 Graphs"
])


# ============================================================
# OVERVIEW
# ============================================================

with t1:

    st.markdown(
        '<div class="section-heading">'
        '📋 Protein Overview'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(row.id)

    st.write(row.description)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🧬 Cleaned length",
        row.clean_length
    )

    c2.metric(
        "✂️ Removed characters",
        row.removed_chars
    )

    c3.metric(
        "⚖️ MW (kDa)",
        round(
            props["Molecular weight (Da)"] / 1000,
            2
        )
    )

    c4.metric(
        "⚡ pI",
        props["Isoelectric point (pI)"]
    )

    st.markdown("### 🔍 Physicochemical Properties")

    properties_df = pd.DataFrame(
        props.items(),
        columns=["Property", "Value"]
    ).astype(str)

    st.dataframe(
        properties_df,
        hide_index=True,
        use_container_width=True
    )

    st.markdown(
        "### 📊 All Sequences in FASTA"
    )

    st.dataframe(
        df.drop(columns="cleaned_seq"),
        hide_index=True,
        use_container_width=True
    )


# ============================================================
# FINGERPRINT
# ============================================================

with t2:

    st.markdown(
        '<div class="section-heading">'
        '🔬 Protein Fingerprint'
        '</div>',
        unsafe_allow_html=True
    )

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
        title="Amino-acid fingerprint (%)",
        height=430,
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
        title="Physicochemical groups"
    )

    b.plotly_chart(
        pie,
        use_container_width=True
    )


    # Heatmap

    st.markdown(
        "### 🌡️ Positional Amino-acid Fingerprint"
    )

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
                edges[i]:edges[i + 1]
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
            f"{edges[i] + 1}-{edges[i + 1]}"
            for i in range(nb)
        ],
        y=list(an.AA),
        aspect="auto",
        color_continuous_scale="Viridis",
        title="Residue frequency along the protein sequence"
    )

    st.plotly_chart(
        hm,
        use_container_width=True
    )


# ============================================================
# PROTEIN MAP
# ============================================================

with t3:

    st.markdown(
        '<div class="section-heading">'
        '🗺️ Interactive Protein Map'
        '</div>',
        unsafe_allow_html=True
    )

    COL = {
        "Hydrophobic / TM-like": "#f97316",
        "Low complexity": "#8b5cf6",
        "Charged-rich": "#2563eb"
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

        y = lanes.index(
            r.region
        ) + 1

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
                    f"{r.start}-{r.end}"
                    f"<br>GRAVY: {r.gravy}"
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
                    motifs.start
                    +
                    motifs.end
                ) / 2,

                y=[
                    len(lanes)
                ] * len(motifs),

                mode="markers",

                marker=dict(
                    size=11,
                    symbol="diamond",
                    color="#dc2626"
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
                color="#0f766e",
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
        title_text="Residue position",
        row=2,
        col=1
    )

    fig.update_yaxes(
        title_text="Hydropathy",
        row=2,
        col=1
    )


    fig.update_layout(
        height=650,
        showlegend=False,
        title=f"Protein map — {row.id}"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "💡 Hover over regions for details. "
        "Drag to zoom and double-click to reset."
    )


# ============================================================
# REGIONS & MOTIFS
# ============================================================

with t4:

    st.markdown(
        '<div class="section-heading">'
        '📑 Detected Protein Regions'
        '</div>',
        unsafe_allow_html=True
    )

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


    st.markdown(
        '<div class="section-heading">'
        '🎯 Detected Sequence Motifs'
        '</div>',
        unsafe_allow_html=True
    )

    if not motifs.empty:

        st.dataframe(
            motifs,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "No sequence motifs found."
        )


# ============================================================
# GRAPHS
# ============================================================

with t5:

    st.markdown(
        '<div class="section-heading">'
        '📈 Protein Analysis Graphs'
        '</div>',
        unsafe_allow_html=True
    )


    # Amino acid composition

    bar = px.bar(
        comp,
        x="aa",
        y="percent",
        title="Amino-acid composition (%)",
        color="percent",
        color_continuous_scale="Tealgrn"
    )

    st.plotly_chart(
        bar,
        use_container_width=True
    )


    # Hydropathy

    line = px.line(
        hydro,
        x="position",
        y="kd",
        title=(
            f"Hydropathy profile "
            f"(window {kd_window})"
        )
    )

    st.plotly_chart(
        line,
        use_container_width=True
    )


    # Multi-sequence comparison

    if len(df) > 1:

        rows = []

        for r in df.itertuples():

            p = an.properties(
                r.cleaned_seq
            )

            rows.append(
                dict(
                    id=r.id,
                    length=p["Length (aa)"],
                    pI=p[
                        "Isoelectric point (pI)"
                    ],
                    gravy=p[
                        "GRAVY (hydropathy)"
                    ],
                    mw=p[
                        "Molecular weight (Da)"
                    ]
                )
            )

        comparison_df = pd.DataFrame(
            rows
        )

        scatter = px.scatter(
            comparison_df,
            x="pI",
            y="gravy",
            size="mw",
            hover_name="id",
            title=(
                "Multi-sequence comparison "
                "(bubble size = molecular weight)"
            )
        )

        st.plotly_chart(
            scatter,
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    🧬 <b>Protein Profiler</b> · Interactive Protein Sequence Analysis
    <br>
    Amino-acid composition • Physicochemical properties • Hydropathy •
    Regions • Motifs
</div>
""", unsafe_allow_html=True)
