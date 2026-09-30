import os
import tempfile
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

st.markdown("""
<style>

    /* -------------------- MAIN PAGE -------------------- */

    .stApp {
        background: linear-gradient(135deg, #f4f8ff 0%, #eef7f6 100%);
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* -------------------- HEADER -------------------- */

    .brand-wrapper {
        text-align: center;
        padding: 10px 10px 20px 10px;
    }

    .brand-icon {
        font-size: 3rem;
        margin-bottom: 4px;
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #17324d;
        line-height: 1.1;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #60758a;
        margin-top: 8px;
        font-weight: 500;
    }

    .header-line {
        width: 120px;
        height: 4px;
        margin: 18px auto 0 auto;
        border-radius: 10px;
        background: linear-gradient(90deg, #3978ff, #18b7a0);
    }


    /* -------------------- INPUT CARD -------------------- */

    .input-card {
        background: rgba(255,255,255,0.97);
        border: 1px solid #dce7f1;
        border-radius: 22px;
        padding: 26px 30px;
        margin-top: 10px;
        margin-bottom: 25px;
        box-shadow: 0 8px 30px rgba(31, 64, 104, 0.08);
    }

    .input-card-title {
        font-size: 1.45rem;
        font-weight: 750;
        color: #17324d;
        margin-bottom: 5px;
    }

    .input-card-subtitle {
        color: #6b7d8f;
        font-size: 0.95rem;
        margin-bottom: 20px;
    }


    /* -------------------- ANALYSIS INTRO -------------------- */

    .intro-card {
        background: linear-gradient(
            135deg,
            rgba(57,120,255,0.10),
            rgba(24,183,160,0.10)
        );
        border: 1px solid rgba(57,120,255,0.20);
        border-radius: 20px;
        padding: 24px 28px;
        margin: 25px 0 25px 0;
        box-shadow: 0 5px 20px rgba(31,64,104,0.05);
    }

    .intro-title {
        font-size: 1.55rem;
        font-weight: 800;
        color: #17324d;
        margin-bottom: 8px;
    }

    .intro-text {
        font-size: 0.98rem;
        color: #5f7182;
        line-height: 1.65;
    }


    /* -------------------- SECTION HEADINGS -------------------- */

    .section-title {
        font-size: 1.5rem;
        font-weight: 750;
        color: #17324d;
        margin-top: 15px;
        margin-bottom: 15px;
    }


    /* -------------------- STATUS CARD -------------------- */

    .status-card {
        background: white;
        border-radius: 18px;
        border: 1px solid #dce7f1;
        padding: 18px 22px;
        margin: 12px 0;
        box-shadow: 0 5px 20px rgba(31,64,104,0.05);
    }

    .status-title {
        font-weight: 750;
        color: #17324d;
        font-size: 1.05rem;
    }

    .status-text {
        color: #68798a;
        font-size: 0.9rem;
        margin-top: 4px;
    }


    /* -------------------- METRIC CARDS -------------------- */

    .metric-card {
        background: white;
        border: 1px solid #dce7f1;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(31,64,104,0.06);
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #17324d;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #708090;
        margin-top: 5px;
    }


    /* -------------------- STREAMLIT ELEMENTS -------------------- */

    div[data-testid="stFileUploader"] {
        border-radius: 15px;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 14px;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 650;
        min-height: 44px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border-radius: 15px;
        padding: 10px;
        border: 1px solid #dce7f1;
    }


    /* -------------------- SIDEBAR -------------------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f7fbff 0%, #edf7f5 100%);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #17324d;
    }


    /* -------------------- FOOTER -------------------- */

    .footer {
        text-align: center;
        color: #789;
        font-size: 0.82rem;
        padding: 35px 10px 10px 10px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# MAIN HEADER
# ============================================================

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


# ============================================================
# SAMPLE FASTA
# ============================================================

SAMPLE = """>HBA_HUMAN
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHF
DLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVD
PVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR

>P53_FRAGMENT
MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDD
IEQWFTEDPGPDEAPRMPEAAPPVAPAPAAPAPAEAPAPAPSWPLSSSV
PSQAMDDLMLSPDDIEQWFTEDPGPDEAPRMPEAAPPVAPAPA
"""


# ============================================================
# PROTEIN INPUT CARD
# ============================================================

st.markdown("""
<div class="input-card">

    <div class="input-card-title">
        🧬 Protein Sequence Input
    </div>

    <div class="input-card-subtitle">
        Upload a FASTA file, paste your protein sequence,
        or load the example sequences to begin analysis.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUT AREA
# ============================================================

input_col1, input_col2 = st.columns(2, gap="large")


with input_col1:

    st.markdown("### 📁 Upload FASTA")

    uploaded_file = st.file_uploader(
        "Choose a FASTA file",
        type=["fasta", "fa", "faa", "txt"],
        help="Upload a protein FASTA file."
    )


with input_col2:

    st.markdown("### 📝 Paste FASTA")

    pasted = st.text_area(
        "Paste your protein sequence",
        height=150,
        placeholder=(
            ">Protein_1\n"
            "MKWVTFISLLFLFSSAYS..."
        )
    )


st.markdown("")


# ============================================================
# SAMPLE BUTTON
# ============================================================

sample_col1, sample_col2, sample_col3 = st.columns([1, 1, 1])

with sample_col2:

    load_sample = st.button(
        "🧪 Load Sample Proteins",
        use_container_width=True
    )


# ============================================================
# DETERMINE INPUT
# ============================================================

if uploaded_file is not None:

    text = uploaded_file.getvalue().decode(
        "utf-8",
        errors="ignore"
    )

elif pasted.strip():

    text = pasted

elif load_sample:

    text = SAMPLE

else:

    text = ""


# ============================================================
# ANALYSIS INTRODUCTION
# THIS IS NOW BELOW THE PROTEIN INPUT CARD
# ============================================================

if text:

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


# ============================================================
# SIDEBAR SETTINGS
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Analysis Settings")

    st.markdown("---")

    hydro_window = st.slider(
        "Hydropathy Window",
        min_value=5,
        max_value=31,
        value=9,
        step=2
    )

    hydro_cutoff = st.slider(
        "Hydrophobic Cutoff",
        min_value=0.5,
        max_value=2.5,
        value=1.2,
        step=0.1
    )

    entropy_cutoff = st.slider(
        "Low-Complexity Entropy Cutoff",
        min_value=1.0,
        max_value=4.0,
        value=2.0,
        step=0.1
    )

    st.markdown("---")

    st.markdown(
        """
        **Analysis includes**

        • Amino-acid composition  
        • Physicochemical properties  
        • Hydrophobicity  
        • Sequence regions  
        • Motif detection  
        • Interactive visualizations
        """
    )


# ============================================================
# EMPTY INPUT MESSAGE
# ============================================================

if not text:

    st.markdown("""
    <div class="status-card">

        <div class="status-title">
            👋 Ready for analysis
        </div>

        <div class="status-text">
            Upload a FASTA file, paste a protein sequence,
            or click <b>Load Sample Proteins</b> to begin.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ============================================================
# PARSE FASTA
# ============================================================

try:

    df, engine = an.parse_fasta(text)

except Exception as e:

    st.error(f"Unable to parse the FASTA input: {e}")
    st.stop()


# ============================================================
# CHECK PARSED DATA
# ============================================================

if df is None or df.empty:

    st.error(
        "No valid protein sequences were detected. "
        "Please check your FASTA input."
    )

    st.stop()


# ============================================================
# PROTEIN SELECTION
# ============================================================

if "ID" in df.columns:

    protein_ids = df["ID"].tolist()

elif "id" in df.columns:

    protein_ids = df["id"].tolist()

else:

    protein_ids = [str(i + 1) for i in range(len(df))]


st.markdown("### 🧬 Select Protein")

selected_index = st.selectbox(
    "Choose a protein for detailed analysis",
    range(len(protein_ids)),
    format_func=lambda x: protein_ids[x]
)

selected_row = df.iloc[selected_index]


# ============================================================
# ANALYSIS CALCULATIONS
# ============================================================

try:

    comp = an.amino_acid_composition(selected_row)

except Exception:

    try:
        comp = an.amino_acid_composition(
            selected_row.get("Sequence", "")
        )
    except Exception:
        comp = pd.DataFrame()


try:

    props = an.physicochemical_properties(selected_row)

except Exception:

    try:
        props = an.physicochemical_properties(
            selected_row.get("Sequence", "")
        )
    except Exception:
        props = {}


try:

    regions = an.find_regions(
        selected_row,
        hydro_window=hydro_window,
        hydrophobic_cutoff=hydro_cutoff,
        entropy_cutoff=entropy_cutoff
    )

except Exception:

    try:
        regions = an.find_regions(
            selected_row.get("Sequence", ""),
            hydro_window=hydro_window,
            hydrophobic_cutoff=hydro_cutoff,
            entropy_cutoff=entropy_cutoff
        )
    except Exception:
        regions = pd.DataFrame()


try:

    motifs = an.find_motifs(selected_row)

except Exception:

    try:
        motifs = an.find_motifs(
            selected_row.get("Sequence", "")
        )
    except Exception:
        motifs = pd.DataFrame()


try:

    hydro = an.hydropathy(
        selected_row,
        window=hydro_window
    )

except Exception:

    try:
        hydro = an.hydropathy(
            selected_row.get("Sequence", ""),
            window=hydro_window
        )
    except Exception:
        hydro = pd.DataFrame()


# ============================================================
# ANALYSIS STATUS
# ============================================================

st.markdown("""
<div class="status-card">

    <div class="status-title">
        ✅ Analysis completed
    </div>

    <div class="status-text">
        Protein sequence successfully processed and ready
        for interactive exploration.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Overview",
        "🧬 Fingerprint",
        "🗺️ Protein Map",
        "🔎 Regions & Motifs",
        "📈 Graphs"
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">Protein Overview</div>',
        unsafe_allow_html=True
    )

    sequence = ""

    for key in ["Sequence", "sequence", "SEQ", "seq"]:

        if key in selected_row.index:

            sequence = str(selected_row[key])
            break

    sequence = "".join(
        sequence.split()
    ).upper()

    sequence_length = len(sequence)

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Sequence Length",
            f"{sequence_length} aa"
        )

    with m2:

        molecular_weight = props.get(
            "Molecular Weight",
            props.get("MW", "—")
        ) if isinstance(props, dict) else "—"

        st.metric(
            "Molecular Weight",
            str(molecular_weight)
        )

    with m3:

        pI = props.get(
            "pI",
            props.get("Isoelectric Point", "—")
        ) if isinstance(props, dict) else "—"

        st.metric(
            "Theoretical pI",
            str(pI)
        )

    with m4:

        gravy = props.get(
            "GRAVY",
            props.get("gravy", "—")
        ) if isinstance(props, dict) else "—"

        st.metric(
            "GRAVY",
            str(gravy)
        )

    st.markdown("")

    # --------------------------------------------------------
    # PROPERTY TABLE
    # --------------------------------------------------------

    if isinstance(props, dict) and props:

        st.markdown("### 🧪 Physicochemical Properties")

        property_df = pd.DataFrame(
            {
                "Property": list(props.keys()),
                "Value": list(props.values())
            }
        )

        st.dataframe(
            property_df,
            hide_index=True,
            use_container_width=True
        )

    # --------------------------------------------------------
    # SEQUENCE
    # --------------------------------------------------------

    st.markdown("### 🧬 Protein Sequence")

    st.code(
        sequence,
        language="text"
    )


# ============================================================
# TAB 2 — FINGERPRINT
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">Amino-Acid Fingerprint</div>',
        unsafe_allow_html=True
    )

    if isinstance(comp, pd.DataFrame) and not comp.empty:

        st.dataframe(
            comp,
            hide_index=True,
            use_container_width=True
        )

        # ----------------------------------------------------
        # AMINO ACID BAR CHART
        # ----------------------------------------------------

        try:

            if comp.shape[1] >= 2:

                aa_col = comp.columns[0]
                value_col = comp.columns[1]

                fig = px.bar(
                    comp,
                    x=aa_col,
                    y=value_col,
                    title="Amino-Acid Composition"
                )

                fig.update_layout(
                    height=450,
                    template="plotly_white",
                    xaxis_title="Amino Acid",
                    yaxis_title="Composition"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        except Exception as e:

            st.info(
                f"Composition chart could not be generated: {e}"
            )

    else:

        st.info(
            "Amino-acid composition data is not available."
        )


# ============================================================
# TAB 3 — PROTEIN MAP
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">Protein Sequence Map</div>',
        unsafe_allow_html=True
    )

    if sequence:

        positions = np.arange(
            1,
            len(sequence) + 1
        )

        # Amino acid numeric mapping
        aa_order = list(
            "ACDEFGHIKLMNPQRSTVWY"
        )

        aa_values = [
            aa_order.index(aa)
            if aa in aa_order
            else -1
            for aa in sequence
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=positions,
                y=aa_values,
                mode="markers",
                text=list(sequence),
                hovertemplate=(
                    "Position: %{x}<br>"
                    "Residue: %{text}<extra></extra>"
                ),
                marker=dict(
                    size=8
                )
            )
        )

        fig.update_layout(
            title="Residue Distribution Along Protein Sequence",
            xaxis_title="Sequence Position",
            yaxis_title="Amino Acid Index",
            template="plotly_white",
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # SEQUENCE BLOCKS
        # ----------------------------------------------------

        st.markdown("### Sequence Blocks")

        block_size = 50

        for start in range(
            0,
            len(sequence),
            block_size
        ):

            end = min(
                start + block_size,
                len(sequence)
            )

            st.code(
                f"{start + 1:>6}  "
                f"{sequence[start:end]}  "
                f"{end}"
            )


# ============================================================
# TAB 4 — REGIONS & MOTIFS
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">Biologically Relevant Regions</div>',
        unsafe_allow_html=True
    )

    if isinstance(regions, pd.DataFrame) and not regions.empty:

        st.dataframe(
            regions,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "No major sequence regions were detected."
        )

    st.markdown("")

    st.markdown(
        '<div class="section-title">Motif Detection</div>',
        unsafe_allow_html=True
    )

    if isinstance(motifs, pd.DataFrame) and not motifs.empty:

        st.dataframe(
            motifs,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "No predefined motifs were detected."
        )


# ============================================================
# TAB 5 — GRAPHS
# ============================================================

with tab5:

    st.markdown(
        '<div class="section-title">Interactive Graphs</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # HYDROPATHY
    # --------------------------------------------------------

    st.markdown("### 💧 Hydropathy Profile")

    if isinstance(hydro, pd.DataFrame) and not hydro.empty:

        st.dataframe(
            hydro.head(20),
            hide_index=True,
            use_container_width=True
        )

        try:

            x_col = hydro.columns[0]
            y_col = hydro.columns[1]

            fig_hydro = px.line(
                hydro,
                x=x_col,
                y=y_col,
                title="Hydropathy Across Protein Sequence"
            )

            fig_hydro.update_layout(
                template="plotly_white",
                height=450,
                xaxis_title="Sequence Position",
                yaxis_title="Hydropathy"
            )

            st.plotly_chart(
                fig_hydro,
                use_container_width=True
            )

        except Exception as e:

            st.info(
                f"Hydropathy graph could not be generated: {e}"
            )

    else:

        st.info(
            "Hydropathy data is not available."
        )

    # --------------------------------------------------------
    # COMPOSITION PIE
    # --------------------------------------------------------

    if isinstance(comp, pd.DataFrame) and not comp.empty:

        st.markdown("### 🥧 Amino-Acid Composition")

        try:

            if comp.shape[1] >= 2:

                aa_col = comp.columns[0]
                value_col = comp.columns[1]

                fig_pie = px.pie(
                    comp,
                    names=aa_col,
                    values=value_col,
                    title="Amino-Acid Composition"
                )

                fig_pie.update_layout(
                    template="plotly_white",
                    height=550
                )

                st.plotly_chart(
                    fig_pie,
                    use_container_width=True
                )

        except Exception as e:

            st.info(
                f"Composition pie chart could not be generated: {e}"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    🧬 <b>Protein Profiler</b><br>
    Interactive Protein Sequence Profiling & Region Mapping

</div>
""", unsafe_allow_html=True)
