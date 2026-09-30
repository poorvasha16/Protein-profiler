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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GENERAL PAGE
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(219, 234, 254, 0.8),
                transparent 25%
            ),
            radial-gradient(
                circle at 95% 10%,
                rgba(204, 251, 241, 0.8),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #f8fbff 0%,
                #f0f9ff 50%,
                #f8f7ff 100%
            );
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       MAIN TITLE
       ======================================================== */

    .main-title {
        font-size: 3.2rem;
        font-weight: 850;
        color: #172554;
        letter-spacing: -1.5px;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 22px;
    }


    /* ========================================================
       HEADER BANNER
       ======================================================== */

    .protein-banner {
        background: linear-gradient(
            135deg,
            #dbeafe 0%,
            #e0f2fe 48%,
            #ccfbf1 100%
        );

        border: 1px solid #bae6fd;
        border-radius: 22px;

        padding: 24px 28px;
        margin: 12px 0 24px 0;

        box-shadow:
            0 8px 25px rgba(37, 99, 235, 0.08);
    }

    .protein-banner-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #075985;
        margin-bottom: 8px;
    }

    .protein-banner-text {
        font-size: 0.98rem;
        line-height: 1.6;
        color: #475569;
    }


    /* ========================================================
       INPUT CARD
       ======================================================== */

    .input-card {
        background: rgba(255, 255, 255, 0.96);

        border: 1px solid #c7d2fe;
        border-radius: 20px;

        padding: 22px 24px;
        margin-bottom: 25px;

        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.06);
    }

    .input-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #3730a3;
        margin-bottom: 6px;
    }

    .input-description {
        color: #64748b;
        margin-bottom: 16px;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
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


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.96);

        border: 1px solid #bfdbfe;
        border-radius: 17px;

        padding: 18px;

        box-shadow:
            0 6px 18px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 650;
    }

    div[data-testid="stMetricValue"] {
        color: #2563eb;
        font-weight: 800;
    }


    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {
        font-size: 0.95rem;
        font-weight: 700;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563eb;
        border-bottom: 3px solid #2563eb;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

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

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #2563eb;
        color: #1e40af;

        box-shadow:
            0 5px 15px rgba(37, 99, 235, 0.12);
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    div[data-testid="stFileUploader"] {
        background: #f8fafc;

        border: 1px solid #dbeafe;
        border-radius: 14px;

        padding: 8px;
    }


    /* ========================================================
       TEXT AREA
       ======================================================== */

    textarea {
        border-radius: 12px !important;
    }


    /* ========================================================
       SELECT BOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        border-radius: 12px;
        border-color: #bfdbfe;
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #dbeafe;
    }


    /* ========================================================
       SECTION HEADINGS
       ======================================================== */

    .section-heading {
        font-size: 1.35rem;
        font-weight: 800;

        color: #1e3a8a;

        margin-top: 8px;
        margin-bottom: 14px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;

        color: #64748b;

        font-size: 0.85rem;

        margin-top: 40px;
        padding-top: 20px;

        border-top: 1px solid #dbeafe;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PAGE TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🧬 Protein Profiler</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Interactive protein sequence profiling, physicochemical analysis,
        hydropathy mapping and motif detection.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROTEIN INFORMATION BANNER
# ============================================================

st.markdown(
    """
    <div class="protein-banner">

        <div class="protein-banner-title">
            🔬 Protein Sequence Analysis
        </div>

        <div class="protein-banner-text">
            Explore amino-acid composition, molecular properties,
            hydrophobic regions, low-complexity regions and sequence
            motifs from your protein FASTA sequence.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SAMPLE PROTEINS
# ============================================================

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


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    """
    <div class="input-card">

        <div class="input-title">
            📥 Protein Sequence Input
        </div>

        <div class="input-description">
            Upload a FASTA file or paste your protein sequence below.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

input_col1, input_col2 = st.columns(2)


# ------------------------------------------------------------
# FILE UPLOAD
# ------------------------------------------------------------

with input_col1:

    uploaded_file = st.file_uploader(
        "📁 Upload FASTA",
        type=["fasta", "fa", "faa", "txt"],
        help="Upload a protein FASTA file."
    )


# ------------------------------------------------------------
# PASTE SEQUENCE
# ------------------------------------------------------------

with input_col2:

    pasted_sequence = st.text_area(
        "📝 Paste FASTA sequence",
        height=120,
        placeholder=(
            ">Protein_ID Protein_name\n"
            "MKTIIALSYIFCLVFADYKDDDD..."
        )
    )


# ------------------------------------------------------------
# SAMPLE BUTTON
# ------------------------------------------------------------

button_col1, button_col2, button_col3 = st.columns(
    [1.2, 1.2, 3]
)

with button_col1:

    sample_button = st.button(
        "🧪 Load Sample",
        use_container_width=True
    )


with button_col2:

    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


if sample_button:

    st.session_state["use_sample"] = True

    st.rerun()


if clear_button:

    st.session_state["use_sample"] = False

    st.rerun()


# ============================================================
# SIDEBAR PARAMETERS
# ============================================================

with st.sidebar:

    st.markdown(
        "## ⚙️ Analysis Parameters"
    )

    st.write(
        "Adjust the parameters used for protein-region detection."
    )

    st.markdown("---")

    kd_window = st.slider(
        "Hydropathy window",
        min_value=5,
        max_value=25,
        value=9,
        step=2
    )

    tm_cut = st.slider(
        "Hydrophobic region cutoff",
        min_value=1.0,
        max_value=2.5,
        value=1.6,
        step=0.1
    )

    lc_cut = st.slider(
        "Low-complexity entropy cutoff",
        min_value=1.5,
        max_value=3.5,
        value=2.2,
        step=0.1
    )

    st.markdown("---")

    st.markdown(
        "### 🧬 Analysis Includes"
    )

    st.markdown(
        """
        • Amino-acid composition  
        • Molecular weight  
        • Isoelectric point  
        • GRAVY  
        • Hydropathy  
        • Protein regions  
        • Sequence motifs  
        • Low-complexity regions
        """
    )


# ============================================================
# DETERMINE INPUT
# ============================================================

if st.session_state.get("use_sample", False):

    sequence_text = SAMPLE

elif uploaded_file is not None:

    sequence_text = uploaded_file.getvalue().decode(
        "utf-8",
        errors="ignore"
    )

elif pasted_sequence.strip():

    sequence_text = pasted_sequence

else:

    sequence_text = ""


# ============================================================
# NO INPUT MESSAGE
# ============================================================

if not sequence_text.strip():

    st.info(
        "👆 Upload a FASTA file, paste a protein sequence, "
        "or click **Load Sample** to begin."
    )

    st.stop()


# ============================================================
# FASTA PARSING
# ============================================================

@st.cache_data(show_spinner="🔬 Parsing FASTA sequence...")
def load_fasta(text):

    return an.parse_fasta(text)


df, engine = load_fasta(sequence_text)


df = df[
    df.clean_length > 0
].reset_index(drop=True)


# ============================================================
# VALIDATION
# ============================================================

if df.empty:

    st.error(
        "❌ No valid protein sequences were found."
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
        "⚠️ The selected sequence is very short. "
        "Some analysis results may be limited."
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

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📋 Overview",
        "🔬 Fingerprint",
        "🗺️ Protein Map",
        "📑 Regions & Motifs",
        "📈 Graphs"
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-heading">📋 Protein Overview</div>',
        unsafe_allow_html=True
    )

    st.subheader(row.id)

    st.write(row.description)

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:

        st.metric(
            "🧬 Sequence Length",
            row.clean_length
        )

    with metric2:

        st.metric(
            "✂️ Removed Characters",
            row.removed_chars
        )

    with metric3:

        st.metric(
            "⚖️ Molecular Weight",
            f"{props['Molecular weight (Da)'] / 1000:.2f} kDa"
        )

    with metric4:

        st.metric(
            "⚡ Isoelectric Point",
            props["Isoelectric point (pI)"]
        )

    st.markdown(
        "### 🔍 Physicochemical Properties"
    )

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
# TAB 2 — FINGERPRINT
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-heading">🔬 Protein Fingerprint</div>',
        unsafe_allow_html=True
    )

    chart1, chart2 = st.columns(2)


    # --------------------------------------------------------
    # RADAR CHART
    # --------------------------------------------------------

    with chart1:

        radar = go.Figure(
            go.Scatterpolar(
                r=list(comp.percent) + [comp.percent[0]],
                theta=list(comp.aa) + [comp.aa[0]],
                fill="toself"
            )
        )

        radar.update_layout(
            title="Amino-acid Fingerprint (%)",
            height=430,
            polar=dict(
                radialaxis=dict(
                    visible=True
                )
            )
        )

        st.plotly_chart(
            radar,
            use_container_width=True
        )


    # --------------------------------------------------------
    # PIE CHART
    # --------------------------------------------------------

    with chart2:

        grouped = an.group_composition(seq)

        pie = px.pie(
            grouped,
            names="group",
            values="percent",
            hole=0.45,
            title="Physicochemical Groups"
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )


    # --------------------------------------------------------
    # HEATMAP
    # --------------------------------------------------------

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

    mat = np.array(
        [
            [
                seq[
                    edges[i]:edges[i + 1]
                ].count(aa)
                /
                max(
                    1,
                    edges[i + 1] - edges[i]
                )

                for i in range(nb)
            ]

            for aa in an.AA
        ]
    )

    heatmap = px.imshow(
        mat,

        x=[
            f"{edges[i] + 1}-{edges[i + 1]}"
            for i in range(nb)
        ],

        y=list(an.AA),

        aspect="auto",

        color_continuous_scale="Viridis",

        title="Residue Frequency Along Protein Sequence"
    )

    st.plotly_chart(
        heatmap,
        use_container_width=True
    )


# ============================================================
# TAB 3 — PROTEIN MAP
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-heading">🗺️ Interactive Protein Map</div>',
        unsafe_allow_html=True
    )

    REGION_COLORS = {
        "Hydrophobic / TM-like": "#f97316",
        "Low complexity": "#8b5cf6",
        "Charged-rich": "#2563eb"
    }

    lanes = list(
        REGION_COLORS
    ) + ["Motifs"]


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


    # --------------------------------------------------------
    # PROTEIN BASE LINE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # REGIONS
    # --------------------------------------------------------

    for region in regions.itertuples():

        y_position = (
            lanes.index(
                region.region
            ) + 1
        )

        fig.add_trace(
            go.Scatter(

                x=[
                    region.start,
                    region.end,
                    region.end,
                    region.start,
                    region.start
                ],

                y=[
                    y_position - 0.35,
                    y_position - 0.35,
                    y_position + 0.35,
                    y_position + 0.35,
                    y_position - 0.35
                ],

                fill="toself",

                mode="lines",

                line=dict(
                    color=REGION_COLORS[
                        region.region
                    ]
                ),

                name=region.region,

                showlegend=False,

                hovertext=(
                    f"{region.region}<br>"
                    f"Position: {region.start}-{region.end}"
                    f"<br>GRAVY: {region.gravy}"
                ),

                hoverinfo="text"
            ),

            row=1,
            col=1
        )


    # --------------------------------------------------------
    # MOTIFS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Y AXIS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # HYDROPATHY
    # --------------------------------------------------------

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

        title=f"Protein Map — {row.id}"
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
# TAB 4 — REGIONS & MOTIFS
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-heading">📑 Detected Protein Regions</div>',
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
            "No regions were detected with the current thresholds."
        )


    st.markdown(
        '<div class="section-heading">🎯 Detected Sequence Motifs</div>',
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
            "No sequence motifs were found."
        )


# ============================================================
# TAB 5 — GRAPHS
# ============================================================

with tab5:

    st.markdown(
        '<div class="section-heading">📈 Protein Analysis Graphs</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # AMINO ACID COMPOSITION
    # --------------------------------------------------------

    composition_bar = px.bar(
        comp,

        x="aa",

        y="percent",

        title="Amino-acid Composition (%)",

        color="percent",

        color_continuous_scale="Tealgrn"
    )

    st.plotly_chart(
        composition_bar,
        use_container_width=True
    )


    # --------------------------------------------------------
    # HYDROPATHY PROFILE
    # --------------------------------------------------------

    hydropathy_line = px.line(
        hydro,

        x="position",

        y="kd",

        title=(
            f"Hydropathy Profile "
            f"(Window = {kd_window})"
        )
    )

    st.plotly_chart(
        hydropathy_line,
        use_container_width=True
    )


    # --------------------------------------------------------
    # MULTI-SEQUENCE COMPARISON
    # --------------------------------------------------------

    if len(df) > 1:

        comparison_rows = []

        for protein in df.itertuples():

            protein_properties = an.properties(
                protein.cleaned_seq
            )

            comparison_rows.append(
                {
                    "id": protein.id,

                    "length": protein_properties[
                        "Length (aa)"
                    ],

                    "pI": protein_properties[
                        "Isoelectric point (pI)"
                    ],

                    "gravy": protein_properties[
                        "GRAVY (hydropathy)"
                    ],

                    "mw": protein_properties[
                        "Molecular weight (Da)"
                    ]
                }
            )


        comparison_df = pd.DataFrame(
            comparison_rows
        )


        comparison_plot = px.scatter(

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
            comparison_plot,
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        🧬 <b>Protein Profiler</b>
        · Interactive Protein Sequence Analysis

        <br><br>

        Amino-acid composition
        • Physicochemical properties
        • Hydropathy
        • Protein regions
        • Sequence motifs

    </div>
    """,
    unsafe_allow_html=True
)
