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
# CUSTOM DESIGN / CSS
# =========================================================

st.markdown("""
<style>

/* =======================================================
   GLOBAL APP
   ======================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 0% 0%,
            rgba(219, 234, 254, 0.65),
            transparent 28%
        ),
        radial-gradient(
            circle at 100% 0%,
            rgba(224, 242, 254, 0.55),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #f8fbff 0%,
            #f8fafc 55%,
            #f0fdfa 100%
        );
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}


/* =======================================================
   HEADER
   ======================================================= */

.brand-wrapper {
    text-align: center;
    margin-bottom: 25px;
}

.brand-icon {
    font-size: 42px;
    margin-bottom: 2px;
}

.main-title {
    font-size: 46px;
    font-weight: 850;
    letter-spacing: -1px;
    margin: 0;

    background: linear-gradient(
        90deg,
        #1d4ed8,
        #2563eb,
        #0891b2
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-size: 17px;
    color: #64748b;
    margin-top: 6px;
}

.header-line {
    width: 90px;
    height: 4px;
    margin: 14px auto 0;

    background: linear-gradient(
        90deg,
        #2563eb,
        #06b6d4
    );

    border-radius: 20px;
}


/* =======================================================
   INTRO CARD
   ======================================================= */

.intro-card {
    background: rgba(255,255,255,0.90);
    border: 1px solid #dbeafe;
    border-radius: 20px;
    padding: 20px 24px;
    margin-bottom: 25px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.06);
}

.intro-title {
    font-size: 21px;
    font-weight: 800;
    color: #0f3d7a;
    margin-bottom: 5px;
}

.intro-text {
    font-size: 14px;
    line-height: 1.6;
    color: #64748b;
}


/* =======================================================
   INPUT CARD
   ======================================================= */

.input-card {
    background: rgba(255,255,255,0.94);

    border: 1px solid #bfdbfe;
    border-radius: 20px;

    padding: 24px;
    margin-top: 10px;
    margin-bottom: 18px;

    box-shadow:
        0 10px 30px rgba(37,99,235,0.08);
}

.input-title {
    font-size: 24px;
    font-weight: 800;
    color: #0f3d7a;
    margin-bottom: 5px;
}

.input-description {
    color: #64748b;
    font-size: 14px;
    line-height: 1.5;
}


/* =======================================================
   STEP LABELS
   ======================================================= */

.step-label {
    font-size: 12px;
    font-weight: 800;
    color: #2563eb;

    text-transform: uppercase;

    letter-spacing: 0.9px;

    margin-bottom: 4px;
}


/* =======================================================
   BUTTONS
   ======================================================= */

.stButton > button {
    border-radius: 12px;

    font-weight: 750;

    border: 1px solid #2563eb;

    background: linear-gradient(
        90deg,
        #2563eb,
        #0891b2
    );

    color: white;

    min-height: 44px;

    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);

    box-shadow:
        0 7px 18px rgba(37,99,235,0.20);

    color: white;
}


/* =======================================================
   METRIC CARDS
   ======================================================= */

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.96);

    border-radius: 16px;

    padding: 17px;

    border: 1px solid #dbeafe;

    box-shadow:
        0 5px 18px rgba(15,23,42,0.06);
}

div[data-testid="stMetricLabel"] {
    color: #64748b;
    font-weight: 650;
}

div[data-testid="stMetricValue"] {
    color: #1d4ed8;
    font-weight: 800;
}


/* =======================================================
   SIDEBAR
   ======================================================= */

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
    color: #0f3d7a;
    font-weight: 800;
}


/* =======================================================
   TABS
   ======================================================= */

button[data-baseweb="tab"] {
    font-weight: 700;
    font-size: 14px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #2563eb;
    border-bottom: 3px solid #2563eb;
}


/* =======================================================
   TEXT AREA
   ======================================================= */

textarea {
    border-radius: 12px !important;
}


/* =======================================================
   FILE UPLOADER
   ======================================================= */

section[data-testid="stFileUploaderDropzone"] {
    border-radius: 14px;

    border: 2px dashed #93c5fd;

    background: #f8fbff;
}


/* =======================================================
   SELECT BOX
   ======================================================= */

div[data-baseweb="select"] > div {
    border-radius: 11px;
}


/* =======================================================
   ALERTS
   ======================================================= */

div[data-testid="stAlert"] {
    border-radius: 13px;
}


/* =======================================================
   DATA TABLE
   ======================================================= */

div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #dbe3ef;
}


/* =======================================================
   SECTION HEADINGS
   ======================================================= */

h2,
h3 {
    color: #0f3d7a;
    font-weight: 800;
}


/* =======================================================
   STATUS CARD
   ======================================================= */

.status-card {
    background: #f0f9ff;

    border: 1px solid #bae6fd;

    border-radius: 14px;

    padding: 15px 18px;

    color: #075985;

    font-size: 14px;

    margin: 15px 0;
}


/* =======================================================
   FOOTER
   ======================================================= */

.footer {
    text-align: center;

    color: #64748b;

    padding: 22px 10px 5px;

    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="brand-wrapper">

    <div class="brand-icon">🧬</div>

    <div class="main-title">
        Protein Profiler
    </div>

    <div class="subtitle">
        Interactive Protein Sequence Profiling & Region Mapping
    </div>

    <div class="header-line"></div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INTRODUCTION
# =========================================================

st.markdown("""
<div class="intro-card">

    <div class="intro-title">
        🔬 Protein Sequence Analysis Platform
    </div>

    <div class="intro-text">
        Analyze protein sequences to explore sequence properties,
        amino-acid composition, hydropathy, motifs, and
        biologically relevant regions through interactive
        visualizations.
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

    <div class="step-label">
        STEP 1
    </div>

    <div class="input-title">
        📄 Input Protein Sequence
    </div>

    <div class="input-description">
        Upload a FASTA file or paste a protein sequence below.
        The sequence will be parsed and prepared for downstream
        analysis.
    </div>

</div>
""", unsafe_allow_html=True)


input_col1, input_col2 = st.columns(
    [1, 1],
    gap="large"
)


with input_col1:

    st.markdown(
        '<div class="step-label">FILE INPUT</div>',
        unsafe_allow_html=True
    )

    up = st.file_uploader(
        "📂 Upload FASTA file",
        type=[
            "fasta",
            "fa",
            "faa",
            "txt"
        ],
        help="Supported formats: FASTA, FA, FAA and TXT"
    )


with input_col2:

    st.markdown(
        '<div class="step-label">TEXT INPUT</div>',
        unsafe_allow_html=True
    )

    pasted = st.text_area(
        "📝 Paste FASTA sequence",
        height=120,
        placeholder=(
            ">Protein_1\n"
            "MVLSPADKTNVKAAWGKV..."
        )
    )


st.markdown("")


sample_col1, sample_col2, sample_col3 = st.columns(
    [1, 1, 1]
)

with sample_col2:

    load_sample = st.button(
        "🧬 Load Sample Proteins",
        use_container_width=True
    )


# =========================================================
# SIDEBAR PARAMETERS
# =========================================================

with st.sidebar:

    st.markdown("# ⚙️ Analysis Settings")

    st.caption(
        "Adjust parameters used for protein region detection "
        "and hydropathy analysis."
    )

    st.markdown("---")

    st.markdown("### 🌊 Hydropathy")

    kd_window = st.slider(
        "Hydropathy window",
        min_value=5,
        max_value=25,
        value=9,
        step=2,
        help="Window size used for Kyte-Doolittle hydropathy calculation."
    )

    tm_cut = st.slider(
        "Hydrophobic region cutoff",
        min_value=1.0,
        max_value=2.5,
        value=1.6,
        step=0.1,
        help="Threshold used to identify hydrophobic / TM-like regions."
    )

    st.markdown("---")

    st.markdown("### 🧩 Complexity")

    lc_cut = st.slider(
        "Low-complexity entropy cutoff",
        min_value=1.5,
        max_value=3.5,
        value=2.2,
        step=0.1,
        help="Entropy threshold used for low-complexity region detection."
    )

    st.markdown("---")

    st.info(
        "💡 Lower or higher thresholds can change the number "
        "of detected protein regions."
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

    st.markdown("""
    <div class="status-card"
         style="text-align:center; margin-top:25px;">

        🧬 <b>Ready for protein analysis</b>

        <br><br>

        Upload a FASTA file, paste a protein sequence,
        or load the sample dataset to begin.

    </div>
    """, unsafe_allow_html=True)

    st.stop()


# =========================================================
# FASTA PARSING
# =========================================================

@st.cache_data(show_spinner="🔬 Parsing FASTA sequence...")

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
# SEQUENCE SELECTION
# =========================================================

st.markdown(
    '<div class="step-label">STEP 2</div>',
    unsafe_allow_html=True
)

st.markdown(
    "### 🧬 Select Protein Sequence"
)


choice = st.selectbox(
    "Choose a protein for detailed analysis",
    df.id,
    help="Select one protein sequence from the uploaded FASTA file."
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

with st.spinner("🔬 Analyzing protein sequence..."):

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
# ANALYSIS DASHBOARD HEADER
# =========================================================

st.markdown(
    '<div class="step-label">STEP 3</div>',
    unsafe_allow_html=True
)

st.markdown(
    "## 📊 Protein Analysis Dashboard"
)

st.markdown(
    """
    <p style="
        color:#64748b;
        margin-top:-8px;
        margin-bottom:20px;
    ">
        Explore sequence properties, molecular fingerprints,
        detected regions, motifs and interactive visualizations.
    </p>
    """,
    unsafe_allow_html=True
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

    st.subheader(
        f"🧬 {row.id}"
    )

    if str(row.description).strip():

        st.caption(
            row.description
        )


    # -----------------------------------------------------
    # MAIN METRICS
    # -----------------------------------------------------

    c = st.columns(4)


    with c[0]:

        st.metric(
            "🧬 Sequence Length",
            f"{row.clean_length} aa"
        )


    with c[1]:

        st.metric(
            "✂️ Removed Characters",
            row.removed_chars
        )


    with c[2]:

        st.metric(
            "⚖️ Molecular Weight",
            f'{props["Molecular weight (Da)"] / 1000:.2f} kDa'
        )


    with c[3]:

        st.metric(
            "⚡ Isoelectric Point",
            props["Isoelectric point (pI)"]
        )


    st.markdown("---")


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
# FINGERPRINT
# =========================================================

with t2:

    st.markdown(
        "### 🧬 Amino-acid Fingerprint"
    )

    a, b = st.columns(
        2,
        gap="large"
    )


    # -----------------------------------------------------
    # RADAR CHART
    # -----------------------------------------------------

    with a:

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
    # PHYSICOCHEMICAL GROUPS
    # -----------------------------------------------------

    with b:

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

        title="Residue Frequency Along the Sequence"
    )


    hm.update_layout(
        margin=dict(
            l=40,
            r=20,
            t=60,
            b=80
        )
    )


    st.plotly_chart(
        hm,
        use_container_width=True
    )


# =========================================================
# PROTEIN MAP
# =========================================================

with t3:

    st.markdown(
        "### 🗺️ Interactive Protein Region Map"
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
    # DETECTED REGIONS
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
    # Y AXIS
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
# REGIONS & MOTIFS
# =========================================================

with t4:

    st.markdown(
        "### 🧩 Detected Protein Regions"
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
        "### 🎯 Detected Motifs"
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
# GRAPHS
# =========================================================

with t5:

    st.markdown(
        "### 📊 Amino-acid Composition"
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


    st.markdown(
        "### 🌊 Hydropathy Profile"
    )


    line = px.line(

        hydro,

        x="position",

        y="kd",

        title=f"Hydropathy Profile — Window {kd_window}"
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

        st.markdown(
            "### 🔬 Multi-sequence Comparison"
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

st.markdown("""
<hr>

<div class="footer">

    🧬 <b>Protein Profiler</b>

    <br>

    Interactive Protein Sequence Profiling & Region Mapping

    <br><br>

    <span style="font-size:12px;">
        Sequence Analysis • Protein Properties • Hydropathy
        • Motifs • Region Mapping
    </span>

</div>
""", unsafe_allow_html=True)
