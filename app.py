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
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROFESSIONAL CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------------------------------------------------
       MAIN APPLICATION
       --------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 0% 0%,
                rgba(219, 234, 254, 0.55),
                transparent 28%
            ),
            radial-gradient(
                circle at 100% 0%,
                rgba(224, 242, 254, 0.45),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #f8fbff 0%,
                #f8fafc 55%,
                #f0fdfa 100%
            );
    }


    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ---------------------------------------------------
       TITLE
       --------------------------------------------------- */

    h1 {
        color: #174ea6 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }


    h2 {
        color: #0f3d7a !important;
        font-weight: 750 !important;
    }


    h3 {
        color: #164e63 !important;
        font-weight: 750 !important;
    }


    /* ---------------------------------------------------
       SIDEBAR
       --------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #eff6ff 0%,
                #f0f9ff 50%,
                #ecfeff 100%
            );

        border-right: 1px solid #dbeafe;
    }


    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0f3d7a !important;
    }


    /* ---------------------------------------------------
       BUTTONS
       --------------------------------------------------- */

    .stButton > button {
        border-radius: 12px;
        min-height: 44px;

        font-weight: 700;

        background: linear-gradient(
            90deg,
            #2563eb,
            #0891b2
        );

        color: white;

        border: 1px solid #2563eb;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }


    .stButton > button:hover {
        color: white;

        transform: translateY(-1px);

        box-shadow:
            0 7px 18px rgba(37, 99, 235, 0.20);
    }


    /* ---------------------------------------------------
       METRICS
       --------------------------------------------------- */

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.96);

        border: 1px solid #dbeafe;

        border-radius: 16px;

        padding: 16px;

        box-shadow:
            0 5px 18px rgba(15, 23, 42, 0.06);
    }


    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 650;
    }


    div[data-testid="stMetricValue"] {
        color: #1d4ed8;
        font-weight: 800;
    }


    /* ---------------------------------------------------
       TABS
       --------------------------------------------------- */

    button[data-baseweb="tab"] {
        font-size: 14px;
        font-weight: 700;
    }


    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563eb;
    }


    /* ---------------------------------------------------
       TEXT AREA
       --------------------------------------------------- */

    textarea {
        border-radius: 12px !important;
    }


    /* ---------------------------------------------------
       FILE UPLOADER
       --------------------------------------------------- */

    section[data-testid="stFileUploaderDropzone"] {
        border-radius: 14px;

        border: 2px dashed #93c5fd;

        background: #f8fbff;
    }


    /* ---------------------------------------------------
       SELECT BOX
       --------------------------------------------------- */

    div[data-baseweb="select"] > div {
        border-radius: 11px;
    }


    /* ---------------------------------------------------
       ALERTS
       --------------------------------------------------- */

    div[data-testid="stAlert"] {
        border-radius: 13px;
    }


    /* ---------------------------------------------------
       DATAFRAME
       --------------------------------------------------- */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #dbe3ef;
    }


    /* ---------------------------------------------------
       DIVIDER
       --------------------------------------------------- */

    hr {
        border-color: #dbeafe;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PROFESSIONAL ANIMATED HEADER
# =========================================================

import streamlit.components.v1 as components

components.html(
    """
    <style>

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        background: transparent;
        font-family: Arial, sans-serif;
        overflow: hidden;
    }

    .hero {
        position: relative;
        width: 100%;
        height: 300px;
        overflow: hidden;

        border-radius: 28px;

        background:
            radial-gradient(
                circle at 15% 30%,
                rgba(59,130,246,0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 70%,
                rgba(6,182,212,0.18),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #f8fbff,
                #eff6ff,
                #ecfeff
            );

        border: 1px solid rgba(147,197,253,0.55);

        box-shadow:
            0 12px 35px rgba(30,64,175,0.10);
    }


    /* ---------- HEADER TEXT ---------- */

    .hero-title {
        position: absolute;

        top: 28px;
        left: 0;
        right: 0;

        text-align: center;

        font-size: 38px;
        font-weight: 800;

        letter-spacing: -1px;

        background:
            linear-gradient(
                90deg,
                #2563eb,
                #0891b2,
                #7c3aed
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-subtitle {
        position: absolute;

        top: 80px;
        left: 0;
        right: 0;

        text-align: center;

        color: #64748b;

        font-size: 15px;

        letter-spacing: 0.5px;
    }


    /* ---------- PROTEIN CHAIN ---------- */

    .protein-chain {
        position: absolute;

        left: 6%;
        right: 6%;

        top: 155px;

        height: 3px;

        background:
            linear-gradient(
                90deg,
                transparent,
                #60a5fa,
                #06b6d4,
                #60a5fa,
                transparent
            );

        box-shadow:
            0 0 12px rgba(6,182,212,0.35);
    }


    /* ---------- AMINO ACIDS ---------- */

    .aa {
        position: absolute;

        width: 42px;
        height: 42px;

        border-radius: 50%;

        display: flex;

        justify-content: center;
        align-items: center;

        color: white;

        font-weight: 800;

        font-size: 15px;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #0891b2
            );

        box-shadow:
            0 5px 18px rgba(37,99,235,0.25);

        animation:
            aaFloat 3s ease-in-out infinite;
    }


    .aa1 {
        left: 10%;
        top: 135px;
    }

    .aa2 {
        left: 21%;
        top: 168px;
        animation-delay: .3s;
    }

    .aa3 {
        left: 32%;
        top: 132px;
        animation-delay: .6s;
    }

    .aa4 {
        left: 43%;
        top: 168px;
        animation-delay: .9s;
    }

    .aa5 {
        left: 54%;
        top: 132px;
        animation-delay: 1.2s;
    }

    .aa6 {
        left: 65%;
        top: 168px;
        animation-delay: 1.5s;
    }

    .aa7 {
        left: 76%;
        top: 132px;
        animation-delay: 1.8s;
    }

    .aa8 {
        left: 87%;
        top: 168px;
        animation-delay: 2.1s;
    }


    @keyframes aaFloat {

        0%, 100% {
            transform:
                translateY(0px)
                scale(1);
        }

        50% {
            transform:
                translateY(-12px)
                scale(1.08);
        }

    }


    /* ---------- FLOATING PARTICLES ---------- */

    .particle {
        position: absolute;

        width: 5px;
        height: 5px;

        border-radius: 50%;

        background: #38bdf8;

        opacity: 0.5;

        animation:
            particleFloat 7s linear infinite;
    }


    .p1 {
        left: 12%;
        top: 45%;
    }

    .p2 {
        left: 35%;
        top: 75%;
        animation-delay: 2s;
    }

    .p3 {
        left: 58%;
        top: 35%;
        animation-delay: 4s;
    }

    .p4 {
        left: 82%;
        top: 65%;
        animation-delay: 1s;
    }


    @keyframes particleFloat {

        0% {
            transform:
                translate(0, 0);

            opacity: 0;
        }

        30% {
            opacity: 0.6;
        }

        70% {
            opacity: 0.6;
        }

        100% {
            transform:
                translate(60px, -40px);

            opacity: 0;
        }

    }


    /* ---------- SMALL LABEL ---------- */

    .hero-label {
        position: absolute;

        bottom: 18px;

        left: 0;
        right: 0;

        text-align: center;

        color: #0f766e;

        font-size: 12px;

        font-weight: 700;

        letter-spacing: 1.5px;
    }

    </style>


    <div class="hero">

        <div class="hero-title">
            🧬 Protein Profiler
        </div>

        <div class="hero-subtitle">
            Interactive Protein Sequence Profiling & Region Mapping
        </div>


        <div class="protein-chain"></div>


        <div class="aa aa1">M</div>
        <div class="aa aa2">V</div>
        <div class="aa aa3">L</div>
        <div class="aa aa4">S</div>
        <div class="aa aa5">P</div>
        <div class="aa aa6">A</div>
        <div class="aa aa7">D</div>
        <div class="aa aa8">K</div>


        <div class="particle p1"></div>
        <div class="particle p2"></div>
        <div class="particle p3"></div>
        <div class="particle p4"></div>


        <div class="hero-label">
            SEQUENCE ANALYSIS • PROTEIN PROPERTIES • MOTIFS • REGION MAPPING
        </div>

    </div>
    """,
    height=320,
    scrolling=False
)


# =========================================================
# INTRODUCTION
# =========================================================

with st.container(border=True):

    st.subheader("🔬 Protein Sequence Analysis Platform")

    st.write(
        "Analyze protein sequences to explore sequence properties, "
        "amino-acid composition, hydropathy, motifs, and "
        "biologically relevant regions through interactive "
        "visualizations."
    )


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
# STEP 1 — INPUT
# =========================================================

st.subheader("STEP 1 — 📄 Input Protein Sequence")

st.caption(
    "Upload a FASTA file or paste a protein sequence below."
)


input_col1, input_col2 = st.columns(
    2,
    gap="large"
)


with input_col1:

    st.markdown("**📂 FASTA File**")

    up = st.file_uploader(
        "Upload protein FASTA",
        type=[
            "fasta",
            "fa",
            "faa",
            "txt"
        ],
        help="Supported formats: FASTA, FA, FAA and TXT",
        label_visibility="collapsed"
    )


with input_col2:

    st.markdown("**📝 FASTA Sequence**")

    pasted = st.text_area(
        "Paste protein FASTA",
        height=130,
        placeholder=(
            ">Protein_1\n"
            "MVLSPADKTNVKAAWGKV..."
        ),
        label_visibility="collapsed"
    )


sample_col1, sample_col2, sample_col3 = st.columns(
    [1, 1, 1]
)


with sample_col2:

    load_sample = st.button(
        "🧬 Load Sample Proteins",
        use_container_width=True
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Analysis Settings")

    st.caption(
        "Adjust parameters used for hydropathy "
        "and protein-region detection."
    )

    st.divider()


    # -----------------------------------------------------
    # HYDROPATHY
    # -----------------------------------------------------

    st.subheader("🌊 Hydropathy")

    kd_window = st.slider(
        "Hydropathy window",
        min_value=5,
        max_value=25,
        value=9,
        step=2,
        help=(
            "Window size used for "
            "Kyte-Doolittle hydropathy."
        )
    )


    tm_cut = st.slider(
        "Hydrophobic region cutoff",
        min_value=1.0,
        max_value=2.5,
        value=1.6,
        step=0.1,
        help=(
            "Threshold used to identify "
            "hydrophobic / TM-like regions."
        )
    )


    st.divider()


    # -----------------------------------------------------
    # COMPLEXITY
    # -----------------------------------------------------

    st.subheader("🧩 Complexity")

    lc_cut = st.slider(
        "Low-complexity entropy cutoff",
        min_value=1.5,
        max_value=3.5,
        value=2.2,
        step=0.1,
        help=(
            "Entropy threshold used for "
            "low-complexity region detection."
        )
    )


    st.divider()


    st.info(
        "💡 Changing these thresholds can alter "
        "the number of detected protein regions."
    )


# =========================================================
# INPUT HANDLING
# =========================================================

if up is not None:

    text = up.getvalue().decode(
        "utf-8",
        errors="ignore"
    )

elif pasted.strip():

    text = pasted

elif load_sample:

    text = SAMPLE

else:

    text = ""


# =========================================================
# START MESSAGE
# =========================================================

if not text.strip():

    st.info(
        "🧬 Upload a FASTA file, paste a protein sequence, "
        "or load the sample dataset to begin analysis."
    )

    st.stop()


# =========================================================
# FASTA PARSING
# =========================================================

@st.cache_data(show_spinner="🔬 Parsing FASTA...")


def load(t):

    return an.parse_fasta(t)


df, engine = load(text)


df = df[
    df.clean_length > 0
].reset_index(drop=True)


# =========================================================
# VALIDATION
# =========================================================

if df.empty:

    st.error(
        "❌ No valid protein sequences were found. "
        "Please check your FASTA input."
    )

    st.stop()


st.success(
    f"✅ FASTA successfully parsed using **{engine}**"
)


# =========================================================
# STEP 2 — SELECT PROTEIN
# =========================================================

st.subheader("STEP 2 — 🧬 Select Protein Sequence")


choice = st.selectbox(
    "Choose a protein for detailed analysis",
    df.id,
    help=(
        "Select one protein sequence from "
        "the uploaded FASTA file."
    )
)


row = df[
    df.id == choice
].iloc[0]


seq = row.cleaned_seq


if len(seq) < 10:

    st.warning(
        "⚠️ The selected sequence is very short; "
        "some analysis results may be limited."
    )


# =========================================================
# ANALYSIS
# =========================================================

with st.spinner(
    "🔬 Analyzing protein sequence..."
):

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
# STEP 3 — DASHBOARD
# =========================================================

st.subheader(
    "STEP 3 — 📊 Protein Analysis Dashboard"
)

st.caption(
    "Explore protein properties, molecular fingerprint, "
    "detected regions, motifs and interactive graphs."
)


# =========================================================
# TABS
# =========================================================

t1, t2, t3, t4, t5 = st.tabs(
    [
        "📋 Overview",
        "🔬 Fingerprint",
        "🗺️ Protein Map",
        "📑 Regions & Motifs",
        "📈 Graphs"
    ]
)


# =========================================================
# TAB 1 — OVERVIEW
# =========================================================

with t1:

    st.subheader(
        f"🧬 {row.id}"
    )


    if str(row.description).strip():

        st.caption(
            row.description
        )


    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "🧬 Sequence Length",
            f"{row.clean_length} aa"
        )


    with c2:

        st.metric(
            "✂️ Removed Characters",
            row.removed_chars
        )


    with c3:

        st.metric(
            "⚖️ Molecular Weight",
            f'{props["Molecular weight (Da)"] / 1000:.2f} kDa'
        )


    with c4:

        st.metric(
            "⚡ Isoelectric Point",
            props["Isoelectric point (pI)"]
        )


    st.divider()


    # -----------------------------------------------------
    # PROTEIN PROPERTIES
    # -----------------------------------------------------

    st.markdown(
        "### 🔎 Protein Properties"
    )


    properties_df = pd.DataFrame(
        props.items(),
        columns=[
            "Property",
            "Value"
        ]
    ).astype(str)


    st.dataframe(
        properties_df,
        hide_index=True,
        use_container_width=True
    )


    # -----------------------------------------------------
    # ALL SEQUENCES
    # -----------------------------------------------------

    if len(df) > 1:

        st.markdown(
            "### 📊 Sequences in Input File"
        )


        st.dataframe(
            df.drop(
                columns="cleaned_seq"
            ),
            hide_index=True,
            use_container_width=True
        )


# =========================================================
# TAB 2 — FINGERPRINT
# =========================================================

with t2:

    st.subheader(
        "🧬 Amino-acid Fingerprint"
    )


    col_a, col_b = st.columns(
        2,
        gap="large"
    )


    # -----------------------------------------------------
    # RADAR
    # -----------------------------------------------------

    with col_a:

        radar_values = list(
            comp.percent
        )

        radar_labels = list(
            comp.aa
        )


        radar = go.Figure(
            go.Scatterpolar(
                r=radar_values + [
                    radar_values[0]
                ],

                theta=radar_labels + [
                    radar_labels[0]
                ],

                fill="toself",

                name="Composition"
            )
        )


        radar.update_layout(
            title="Amino-acid Composition (%)",

            height=420,

            polar=dict(
                radialaxis=dict(
                    visible=True
                )
            ),

            margin=dict(
                l=30,
                r=30,
                t=60,
                b=30
            )
        )


        st.plotly_chart(
            radar,
            use_container_width=True
        )


    # -----------------------------------------------------
    # PIE
    # -----------------------------------------------------

    with col_b:

        g = an.group_composition(
            seq
        )


        pie = px.pie(
            g,
            names="group",
            values="percent",
            hole=0.45,
            title="Physicochemical Groups"
        )


        pie.update_layout(
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )


        st.plotly_chart(
            pie,
            use_container_width=True
        )


    # -----------------------------------------------------
    # POSITIONAL FINGERPRINT
    # -----------------------------------------------------

    st.markdown(
        "### 🧩 Positional Fingerprint"
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


    mat = np.array(
        [
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
        ]
    )


    hm = px.imshow(
        mat,

        x=[
            f"{edges[i] + 1}-{edges[i + 1]}"
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
# TAB 3 — PROTEIN MAP
# =========================================================

with t3:

    st.subheader(
        "🗺️ Interactive Protein Region Map"
    )


    COL = {
        "Hydrophobic / TM-like": "#f97316",
        "Low complexity": "#8b5cf6",
        "Charged-rich": "#0ea5e9"
    }


    lanes = list(COL) + [
        "Motifs"
    ]


    fig = make_subplots(
        rows=2,
        cols=1,

        shared_xaxes=True,

        row_heights=[
            0.55,
            0.45
        ],

        vertical_spacing=0.04
    )


    # -----------------------------------------------------
    # PROTEIN BASELINE
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # REGIONS
    # -----------------------------------------------------

    for r in regions.itertuples():

        if r.region not in COL:

            continue


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
                    y - 0.35,
                    y - 0.35,
                    y + 0.35,
                    y + 0.35,
                    y - 0.35
                ],

                fill="toself",

                mode="lines",

                line=dict(
                    color=COL[
                        r.region
                    ]
                ),

                name=r.region,

                legendgroup=r.region,

                showlegend=False,

                hovertext=(
                    f"<b>{r.region}</b><br>"
                    f"Position: {r.start}-{r.end}<br>"
                    f"GRAVY: {r.gravy}"
                ),

                hoverinfo="text"
            ),

            row=1,

            col=1
        )


    # -----------------------------------------------------
    # MOTIFS
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # REGION AXIS
    # -----------------------------------------------------

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
            len(lanes) + 0.6
        ],

        row=1,

        col=1
    )


    # -----------------------------------------------------
    # HYDROPATHY
    # -----------------------------------------------------

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

        title=f"Interactive Protein Map — {row.id}",

        margin=dict(
            l=30,
            r=30,
            t=70,
            b=40
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.caption(
        "💡 Hover over regions for details • "
        "Drag to zoom • Double-click to reset"
    )


# =========================================================
# TAB 4 — REGIONS & MOTIFS
# =========================================================

with t4:

    st.subheader(
        "🧩 Detected Protein Regions"
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


    st.subheader(
        "🎯 Detected Motifs"
    )


    if not motifs.empty:

        st.dataframe(
            motifs,

            hide_index=True,

            use_container_width=True
        )

    else:

        st.info(
            "No motifs found in the selected sequence."
        )


# =========================================================
# TAB 5 — GRAPHS
# =========================================================

with t5:

    st.subheader(
        "📊 Amino-acid Composition"
    )


    bar = px.bar(
        comp,

        x="aa",

        y="percent",

        title="Amino-acid Composition (%)",

        color="percent",

        color_continuous_scale="Tealgrn"
    )


    bar.update_layout(
        margin=dict(
            l=30,
            r=30,
            t=60,
            b=40
        )
    )


    st.plotly_chart(
        bar,
        use_container_width=True
    )


    st.subheader(
        "🌊 Hydropathy Profile"
    )


    line = px.line(
        hydro,

        x="position",

        y="kd",

        title=(
            f"Hydropathy Profile — "
            f"Window {kd_window}"
        )
    )


    line.update_layout(
        margin=dict(
            l=30,
            r=30,
            t=60,
            b=40
        )
    )


    st.plotly_chart(
        line,
        use_container_width=True
    )


    # -----------------------------------------------------
    # MULTI-SEQUENCE COMPARISON
    # -----------------------------------------------------

    if len(df) > 1:

        st.subheader(
            "🔬 Multi-sequence Comparison"
        )


        rows = []


        for r in df.itertuples():

            p = an.properties(
                r.cleaned_seq
            )


            rows.append(
                {
                    "id": r.id,

                    "length": p[
                        "Length (aa)"
                    ],

                    "pI": p[
                        "Isoelectric point (pI)"
                    ],

                    "gravy": p[
                        "GRAVY (hydropathy)"
                    ],

                    "mw": p[
                        "Molecular weight (Da)"
                    ]
                }
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
                "Multi-sequence Comparison "
                "(Bubble Size = Molecular Weight)"
            )
        )


        st.plotly_chart(
            scatter,
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🧬 Protein Profiler  •  "
    "Sequence Analysis  •  Protein Properties  •  "
    "Hydropathy  •  Motifs  •  Region Mapping"
)
