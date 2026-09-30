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
# PROFESSIONAL BLUE BIOINFORMATICS THEME
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL BACKGROUND
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(37, 99, 235, 0.16),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(6, 182, 212, 0.14),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #f8fbff 0%,
                #eef6ff 45%,
                #f0fdfa 100%
            );

        min-height: 100vh;
    }


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       ANIMATED AMINO ACID BACKGROUND
       ===================================================== */

    .amino-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }


    .amino {
        position: absolute;

        display: flex;
        align-items: center;
        justify-content: center;

        width: 42px;
        height: 42px;

        border-radius: 50%;

        font-weight: 800;
        font-size: 15px;

        color: rgba(37, 99, 235, 0.35);

        background: rgba(255,255,255,0.45);

        border: 1px solid rgba(37,99,235,0.12);

        box-shadow:
            0 0 25px rgba(37,99,235,0.08);

        animation:
            floatAmino 14s infinite ease-in-out;
    }


    .a1 {
        left: 5%;
        top: 18%;
        animation-delay: 0s;
    }

    .a2 {
        left: 18%;
        top: 70%;
        animation-delay: 3s;
    }

    .a3 {
        left: 35%;
        top: 12%;
        animation-delay: 6s;
    }

    .a4 {
        left: 60%;
        top: 78%;
        animation-delay: 2s;
    }

    .a5 {
        left: 78%;
        top: 22%;
        animation-delay: 5s;
    }

    .a6 {
        left: 90%;
        top: 62%;
        animation-delay: 8s;
    }

    .a7 {
        left: 48%;
        top: 45%;
        animation-delay: 4s;
    }


    @keyframes floatAmino {

        0% {
            transform:
                translateY(0px)
                rotate(0deg);
            opacity: 0.25;
        }

        50% {
            transform:
                translateY(-35px)
                rotate(12deg);
            opacity: 0.55;
        }

        100% {
            transform:
                translateY(0px)
                rotate(0deg);
            opacity: 0.25;
        }
    }


    /* =====================================================
       HERO SECTION
       ===================================================== */

    .hero {
        position: relative;
        z-index: 2;

        padding: 30px 35px;

        border-radius: 28px;

        background:
            linear-gradient(
                135deg,
                #0f3d91,
                #2563eb 50%,
                #0891b2
            );

        color: white;

        box-shadow:
            0 20px 50px rgba(37,99,235,0.25);

        overflow: hidden;

        margin-bottom: 25px;
    }


    .hero::before {
        content: "";

        position: absolute;

        width: 280px;
        height: 280px;

        right: -80px;
        top: -100px;

        border-radius: 50%;

        background:
            rgba(255,255,255,0.12);

        animation:
            heroPulse 6s infinite ease-in-out;
    }


    .hero::after {
        content: "";

        position: absolute;

        width: 180px;
        height: 180px;

        left: -80px;
        bottom: -80px;

        border-radius: 50%;

        background:
            rgba(255,255,255,0.08);

        animation:
            heroPulse 8s infinite ease-in-out reverse;
    }


    @keyframes heroPulse {

        0%,100% {
            transform: scale(1);
        }

        50% {
            transform: scale(1.2);
        }
    }


    .hero-content {
        position: relative;
        z-index: 3;
    }


    .hero-title {
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }


    .hero-subtitle {
        font-size: 18px;
        opacity: 0.92;
        margin-bottom: 18px;
    }


    .hero-badge {
        display: inline-block;

        padding: 7px 14px;

        border-radius: 999px;

        background:
            rgba(255,255,255,0.15);

        border:
            1px solid rgba(255,255,255,0.25);

        font-size: 13px;
        font-weight: 700;

        backdrop-filter: blur(8px);
    }


    /* =====================================================
       HEADINGS
       ===================================================== */

    h1 {
        color: #0f3d91 !important;
        font-weight: 900 !important;
    }


    h2 {
        color: #123f82 !important;
        font-weight: 850 !important;
    }


    h3 {
        color: #075985 !important;
        font-weight: 800 !important;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #eaf3ff 0%,
                #eff8ff 50%,
                #ecfeff 100%
            );

        border-right:
            2px solid rgba(37,99,235,0.15);

        box-shadow:
            8px 0 30px rgba(15,23,42,0.05);
    }


    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {

        color: #0f3d91 !important;
        font-weight: 850 !important;
    }


    section[data-testid="stSidebar"] label {

        font-weight: 700 !important;
        color: #164e63 !important;
    }


    /* =====================================================
       SIDEBAR CARD
       ===================================================== */

    .sidebar-card {

        padding: 18px;

        margin-bottom: 18px;

        border-radius: 18px;

        background:
            rgba(255,255,255,0.72);

        border:
            1px solid rgba(37,99,235,0.12);

        box-shadow:
            0 8px 25px rgba(15,23,42,0.06);

        backdrop-filter: blur(10px);
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {

        min-height: 46px;

        border-radius: 13px;

        border:
            1px solid #2563eb;

        background:
            linear-gradient(
                90deg,
                #2563eb,
                #0891b2
            );

        color: white;

        font-weight: 800;

        box-shadow:
            0 8px 20px rgba(37,99,235,0.18);

        transition:
            all 0.2s ease;
    }


    .stButton > button:hover {

        transform:
            translateY(-3px)
            scale(1.01);

        box-shadow:
            0 12px 28px rgba(37,99,235,0.30);

        color: white;
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    section[data-testid="stFileUploaderDropzone"] {

        border-radius: 18px;

        border:
            2px dashed #60a5fa;

        background:
            rgba(239,246,255,0.8);

        transition:
            all 0.2s ease;
    }


    section[data-testid="stFileUploaderDropzone"]:hover {

        border-color: #2563eb;

        background:
            rgba(219,234,254,0.9);

        transform:
            translateY(-2px);
    }


    /* =====================================================
       TEXT AREA
       ===================================================== */

    textarea {

        border-radius: 14px !important;

        border:
            1px solid #bfdbfe !important;

        background:
            rgba(255,255,255,0.9) !important;
    }


    /* =====================================================
       SELECT BOX
       ===================================================== */

    div[data-baseweb="select"] > div {

        border-radius: 13px;

        border-color: #bfdbfe;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.96),
                rgba(239,246,255,0.94)
            );

        border:
            1px solid #bfdbfe;

        border-radius: 20px;

        padding: 20px;

        box-shadow:
            0 10px 28px rgba(15,23,42,0.07);

        transition:
            all 0.25s ease;
    }


    div[data-testid="stMetric"]:hover {

        transform:
            translateY(-5px);

        box-shadow:
            0 15px 35px rgba(37,99,235,0.16);

        border-color:
            #60a5fa;
    }


    div[data-testid="stMetricLabel"] {

        color: #64748b;

        font-weight: 700;
    }


    div[data-testid="stMetricValue"] {

        color: #1558c0;

        font-weight: 900;
    }


    /* =====================================================
       LARGE DASHBOARD TABS
       ===================================================== */

    button[data-baseweb="tab"] {

        font-size: 17px !important;

        font-weight: 850 !important;

        padding:
            15px 18px !important;

        color:
            #475569 !important;

        transition:
            all 0.2s ease !important;
    }


    button[data-baseweb="tab"]:hover {

        color:
            #2563eb !important;

        transform:
            translateY(-2px);
    }


    button[data-baseweb="tab"][aria-selected="true"] {

        color:
            #0759d4 !important;

        font-weight:
            900 !important;
    }


    /* =====================================================
       TAB AREA
       ===================================================== */

    div[data-baseweb="tab-list"] {

        gap: 10px;

        padding:
            8px 10px;

        border-radius:
            18px;

        background:
            rgba(255,255,255,0.75);

        border:
            1px solid #dbeafe;

        box-shadow:
            0 8px 25px rgba(15,23,42,0.05);
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    div[data-testid="stDataFrame"] {

        border-radius: 16px;

        overflow: hidden;

        border:
            1px solid #dbeafe;

        box-shadow:
            0 8px 25px rgba(15,23,42,0.05);
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {

        border-radius: 15px;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {

        border-color:
            #bfdbfe;
    }


    /* =====================================================
       SECTION TITLE
       ===================================================== */

    .section-title {

        display: flex;

        align-items: center;

        gap: 12px;

        margin-top: 20px;

        margin-bottom: 15px;
    }


    .section-icon {

        width: 42px;
        height: 42px;

        display: flex;

        align-items: center;
        justify-content: center;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #06b6d4
            );

        color: white;

        font-size: 20px;

        box-shadow:
            0 7px 18px rgba(37,99,235,0.22);
    }


    .section-name {

        font-size: 25px;

        font-weight: 900;

        color: #123f82;
    }


    /* =====================================================
       STEP BADGE
       ===================================================== */

    .step {

        display: inline-flex;

        align-items: center;

        gap: 8px;

        padding:
            8px 14px;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                #dbeafe,
                #cffafe
            );

        color:
            #075985;

        font-size:
            13px;

        font-weight:
            900;

        margin-bottom:
            10px;
    }


    /* =====================================================
       INFO CARD
       ===================================================== */

    .info-card {

        padding:
            22px;

        border-radius:
            20px;

        background:
            rgba(255,255,255,0.86);

        border:
            1px solid #dbeafe;

        box-shadow:
            0 10px 30px rgba(15,23,42,0.06);

        transition:
            all 0.25s ease;
    }


    .info-card:hover {

        transform:
            translateY(-3px);

        box-shadow:
            0 15px 35px rgba(37,99,235,0.12);
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {

        text-align: center;

        padding:
            20px;

        color:
            #64748b;

        font-size:
            13px;
    }

    </style>


    <!-- Animated amino-acid particles -->

    <div class="amino-background">

        <div class="amino a1">M</div>
        <div class="amino a2">K</div>
        <div class="amino a3">A</div>
        <div class="amino a4">G</div>
        <div class="amino a5">F</div>
        <div class="amino a6">Y</div>
        <div class="amino a7">L</div>

    </div>

    """,
    unsafe_allow_html=True
)


# =========================================================
# HERO HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-content">

            <div class="hero-badge">
                🧬 BIOINFORMATICS • PROTEIN ANALYSIS
            </div>

            <div class="hero-title">
                Protein Profiler
            </div>

            <div class="hero-subtitle">
                Interactive Protein Sequence Profiling &
                Region Mapping Platform
            </div>

            <div style="
                font-size:14px;
                opacity:0.88;
                max-width:850px;
            ">
                Explore amino-acid composition, molecular
                properties, hydropathy, motifs and
                biologically relevant protein regions
                through interactive visualizations.
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INTRODUCTION
# =========================================================

st.markdown(
    """
    <div class="info-card">

        <div style="
            font-size:22px;
            font-weight:900;
            color:#123f82;
            margin-bottom:8px;
        ">
            🔬 Protein Sequence Analysis Platform
        </div>

        <div style="
            color:#475569;
            font-size:15px;
            line-height:1.7;
        ">
            Analyze protein sequences and discover their
            composition, physicochemical properties,
            hydrophobic regions, low-complexity regions,
            motifs and sequence patterns.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


st.write("")


# =========================================================
# SAMPLE FASTA
# =========================================================

SAMPLE = """>sp|P69905|HBA_HUMAN Hemoglobin subunit alpha
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG
KKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTP
AVHASLDKFLASVSTVLTSKYR
>sp|P04637|P53_HUMAN Cellular tumor antigen p53
MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGP
DEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYQGSYGFRLGFLHSGTAK
SVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHE
RCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNS
SCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEENLRKKGEPHHELP
PGSTKRALPNNTSSSPQPKKKPLDGEYFTLQIRGRERFEMFRELNEALELKDAQAGKEPG
GSRAHSSHLKSKKGQSTSRHKKLMFKTEGPDSD
"""


# =========================================================
# STEP 1
# =========================================================

st.markdown(
    """
    <div class="section-title">

        <div class="section-icon">
            📄
        </div>

        <div class="section-name">
            STEP 1 — Input Protein Sequence
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


st.caption(
    "Upload a FASTA file or paste your protein sequence."
)


input_col1, input_col2 = st.columns(
    2,
    gap="large"
)


with input_col1:

    st.markdown("### 📂 FASTA File")

    up = st.file_uploader(
        "Upload protein FASTA",
        type=[
            "fasta",
            "fa",
            "faa",
            "txt"
        ],
        help="Supported: FASTA, FA, FAA and TXT",
        label_visibility="collapsed"
    )


with input_col2:

    st.markdown("### 📝 Paste FASTA")

    pasted = st.text_area(
        "Paste protein FASTA",
        height=140,
        placeholder=(
            ">Protein_1\n"
            "MVLSPADKTNVKAAWGKV..."
        ),
        label_visibility="collapsed"
    )


st.write("")


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

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px 0 20px 0;
        ">

            <div style="
                font-size:38px;
            ">
                🧬
            </div>

            <div style="
                font-size:23px;
                font-weight:900;
                color:#0f3d91;
            ">
                Analysis Settings
            </div>

            <div style="
                color:#64748b;
                font-size:13px;
                margin-top:5px;
            ">
                Tune your protein analysis
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.divider()


    # -----------------------------------------------------
    # HYDROPATHY
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-card">

            <div style="
                font-size:19px;
                font-weight:900;
                color:#075985;
            ">
                🌊 Hydropathy
            </div>

            <div style="
                font-size:12px;
                color:#64748b;
                margin-top:4px;
            ">
                Analyze hydrophobic behaviour
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    kd_window = st.slider(
        "Hydropathy window",
        min_value=5,
        max_value=25,
        value=9,
        step=2,
        help="Window size for Kyte-Doolittle hydropathy."
    )


    tm_cut = st.slider(
        "Hydrophobic region cutoff",
        min_value=1.0,
        max_value=2.5,
        value=1.6,
        step=0.1,
        help="Threshold for hydrophobic/TM-like regions."
    )


    st.divider()


    # -----------------------------------------------------
    # COMPLEXITY
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-card">

            <div style="
                font-size:19px;
                font-weight:900;
                color:#075985;
            ">
                🧩 Complexity
            </div>

            <div style="
                font-size:12px;
                color:#64748b;
                margin-top:4px;
            ">
                Detect low-complexity regions
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    lc_cut = st.slider(
        "Low-complexity entropy cutoff",
        min_value=1.5,
        max_value=3.5,
        value=2.2,
        step=0.1,
        help="Entropy threshold for low-complexity detection."
    )


    st.divider()


    st.info(
        "💡 Adjusting these values changes the "
        "detected protein regions."
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
# NO INPUT
# =========================================================

if not text.strip():

    st.markdown(
        """
        <div class="info-card" style="
            text-align:center;
            margin-top:25px;
        ">

            <div style="
                font-size:50px;
            ">
                🧬
            </div>

            <div style="
                font-size:22px;
                font-weight:900;
                color:#123f82;
            ">
                Ready for Protein Analysis
            </div>

            <div style="
                color:#64748b;
                margin-top:8px;
            ">
                Upload a FASTA file, paste a sequence,
                or load the sample dataset.
            </div>

        </div>
        """,
        unsafe_allow_html=True
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
# STEP 2
# =========================================================

st.markdown(
    """
    <div class="section-title">

        <div class="section-icon">
            🧬
        </div>

        <div class="section-name">
            STEP 2 — Select Protein
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


choice = st.selectbox(
    "Choose a protein for detailed analysis",
    df.id
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
# STEP 3
# =========================================================

st.markdown(
    """
    <div class="section-title">

        <div class="section-icon">
            📊
        </div>

        <div class="section-name">
            STEP 3 — Protein Analysis Dashboard
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


st.caption(
    "Explore protein properties, amino-acid fingerprint, "
    "regions, motifs and interactive graphs."
)


# =========================================================
# TABS
# =========================================================

t1, t2, t3, t4, t5 = st.tabs(
    [
        "📋  OVERVIEW",
        "🧬  FINGERPRINT",
        "🗺️  PROTEIN MAP",
        "🎯  REGIONS & MOTIFS",
        "📈  GRAPHS"
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


    st.write("")


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


    st.write("")


    st.markdown(
        """
        <div class="section-title">

            <div class="section-icon">
                🔎
            </div>

            <div class="section-name">
                Protein Properties
            </div>

        </div>
        """,
        unsafe_allow_html=True
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


    if len(df) > 1:

        st.markdown(
            """
            <div class="section-title">

                <div class="section-icon">
                    📊
                </div>

                <div class="section-name">
                    Sequences in Input
                </div>

            </div>
            """,
            unsafe_allow_html=True
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

    st.markdown(
        """
        <div class="section-title">

            <div class="section-icon">
                🧬
            </div>

            <div class="section-name">
                Amino-acid Fingerprint
            </div>

        </div>
        """,
        unsafe_allow_html=True
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

                name="Composition",

                line=dict(
                    color="#2563eb",
                    width=3
                ),

                fillcolor="rgba(37,99,235,0.25)"
            )
        )


        radar.update_layout(

            title="Amino-acid Composition (%)",

            height=440,

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
        """
        <div class="section-title">

            <div class="section-icon">
                🧩
            </div>

            <div class="section-name">
                Positional Fingerprint
            </div>

        </div>
        """,
        unsafe_allow_html=True
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

        color_continuous_scale="Blues",

        title="Residue Frequency Along the Sequence"
    )


    hm.update_layout(
        height=500
    )


    st.plotly_chart(
        hm,
        use_container_width=True
    )


# =========================================================
# TAB 3 — PROTEIN MAP
# =========================================================

with t3:

    st.markdown(
        """
        <div class="section-title">

            <div class="section-icon">
                🗺️
            </div>

            <div class="section-name">
                Interactive Protein Region Map
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    COL = {
        "Hydrophobic / TM-like": "#f97316",
        "Low complexity": "#8b5cf6",
        "Charged-rich": "#06b6d4"
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

        vertical_spacing=0.05
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

        fillcolor="#bfdbfe",

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
                    ],
                    width=2
                ),

                fillcolor=COL[
                    r.region
                ],

                name=r.region,

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
                    size=13,
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

        height=650,

        showlegend=False,

        title=dict(
            text=f"Protein Map — {row.id}",
            font=dict(
                size=22,
                color="#123f82"
            )
        ),

        plot_bgcolor="rgba(255,255,255,0.75)",

        paper_bgcolor="rgba(0,0,0,0)",

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


    st.info(
        "💡 Hover over regions for details • "
        "Drag to zoom • Double-click to reset"
    )


# =========================================================
# TAB 4 — REGIONS & MOTIFS
# =========================================================

with t4:

    st.markdown(
        """
        <div class="section-title">

            <div class="section-icon">
                🎯
            </div>

            <div class="section-name">
                Detected Regions & Motifs
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "### 🧩 Protein Regions"
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


    st.write("")


    st.markdown(
        "### 🎯 Sequence Motifs"
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

    st.markdown(
        """
        <div class="section-title">

            <div class="section-icon">
                📈
            </div>

            <div class="section-name">
                Interactive Graphs
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # AMINO ACID BAR
    # -----------------------------------------------------

    bar = px.bar(

        comp,

        x="aa",

        y="percent",

        title="Amino-acid Composition (%)",

        color="percent",

        color_continuous_scale="Blues"
    )


    bar.update_layout(

        height=450,

        plot_bgcolor="rgba(255,255,255,0.75)",

        paper_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=30,
            r=30,
            t=70,
            b=40
        )
    )


    st.plotly_chart(
        bar,
        use_container_width=True
    )


    # -----------------------------------------------------
    # HYDROPATHY
    # -----------------------------------------------------

    st.markdown(
        "### 🌊 Hydropathy Profile"
    )


    line = px.line(

        hydro,

        x="position",

        y="kd",

        title=(
            f"Kyte-Doolittle Hydropathy "
            f"Profile — Window {kd_window}"
        )
    )


    line.update_traces(
        line=dict(
            width=3
        )
    )


    line.update_layout(

        height=430,

        plot_bgcolor="rgba(255,255,255,0.75)",

        paper_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=30,
            r=30,
            t=70,
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

        st.markdown(
            """
            <div class="section-title">

                <div class="section-icon">
                    🔬
                </div>

                <div class="section-name">
                    Multi-sequence Comparison
                </div>

            </div>
            """,
            unsafe_allow_html=True
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
                "Protein Comparison "
                "(Bubble Size = Molecular Weight)"
            )
        )


        scatter.update_layout(
            height=480,

            plot_bgcolor="rgba(255,255,255,0.75)",

            paper_bgcolor="rgba(0,0,0,0)"
        )


        st.plotly_chart(
            scatter,
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.markdown(
    """
    <div class="footer">

        🧬 <b>Protein Profiler</b>
        &nbsp;•&nbsp;
        Sequence Analysis
        &nbsp;•&nbsp;
        Amino-acid Composition
        &nbsp;•&nbsp;
        Hydropathy
        &nbsp;•&nbsp;
        Motif Detection
        &nbsp;•&nbsp;
        Region Mapping

        <br><br>

        <span style="color:#2563eb;">
            Bioinformatics Project
        </span>

    </div>
    """,
    unsafe_allow_html=True
)
