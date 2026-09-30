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
    initial_sidebar_state="expanded",
)


# =========================================================
# PROFESSIONAL BLUE BIOINFORMATICS THEME
# IMPORTANT:
# All HTML is rendered through st.markdown(...,
# unsafe_allow_html=True). Do not use st.write/st.code for HTML.
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL PAGE
       ========================= */

    .stApp {
        background:
            radial-gradient(circle at 10% 5%, rgba(37,99,235,.13), transparent 25%),
            radial-gradient(circle at 90% 10%, rgba(6,182,212,.12), transparent 25%),
            linear-gradient(135deg, #f7fbff 0%, #eef6ff 48%, #f5fbff 100%);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    header[data-testid="stHeader"] {
        background: rgba(255,255,255,.55);
    }

    /* =========================
       ANIMATIONS
       ========================= */

    @keyframes floatUp {
        0%   { transform: translateY(30px) scale(.9); opacity: 0; }
        15%  { opacity: .9; }
        50%  { transform: translateY(-20px) scale(1); opacity: 1; }
        100% { transform: translateY(-90px) scale(.85); opacity: 0; }
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 rgba(37,99,235,0); }
        50% { box-shadow: 0 0 28px rgba(37,99,235,.28); }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes shimmer {
        0% { background-position: -600px 0; }
        100% { background-position: 600px 0; }
    }

    @keyframes dnaMove {
        0% { transform: translateX(-20px); }
        50% { transform: translateX(20px); }
        100% { transform: translateX(-20px); }
    }

    .fade-in {
        animation: slideIn .65s ease-out both;
    }

    /* =========================
       HERO
       ========================= */

    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        padding: 38px 42px;
        margin: 8px 0 22px 0;
        background:
            radial-gradient(circle at 80% 20%, rgba(34,211,238,.28), transparent 28%),
            radial-gradient(circle at 20% 90%, rgba(59,130,246,.22), transparent 30%),
            linear-gradient(135deg, #082f70 0%, #0b4aa2 48%, #075985 100%);
        border: 1px solid rgba(147,197,253,.55);
        box-shadow: 0 18px 45px rgba(15,64,120,.18);
        color: white;
        animation: pulseGlow 4s ease-in-out infinite;
    }

    .hero::before,
    .hero::after {
        content: "";
        position: absolute;
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,.16);
        pointer-events: none;
    }

    .hero::before {
        width: 310px;
        height: 310px;
        right: -100px;
        top: -140px;
    }

    .hero::after {
        width: 210px;
        height: 210px;
        right: 80px;
        bottom: -160px;
    }

    .hero-content {
        position: relative;
        z-index: 3;
        max-width: 850px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(255,255,255,.13);
        border: 1px solid rgba(255,255,255,.28);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.2px;
        margin-bottom: 15px;
    }

    .hero-title {
        font-size: clamp(34px, 5vw, 58px);
        line-height: 1;
        font-weight: 900;
        letter-spacing: -1.5px;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        font-size: 18px;
        line-height: 1.6;
        color: rgba(255,255,255,.86);
        max-width: 760px;
    }

    .hero-mini {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 20px;
    }

    .hero-chip {
        padding: 7px 11px;
        border-radius: 10px;
        background: rgba(255,255,255,.10);
        border: 1px solid rgba(255,255,255,.20);
        font-size: 12px;
        font-weight: 700;
    }

    /* =========================
       FLOATING AMINO ACIDS
       ========================= */

    .aa-field {
        position: absolute;
        right: 18px;
        bottom: 0;
        width: 390px;
        height: 250px;
        pointer-events: none;
        overflow: hidden;
        z-index: 2;
    }

    .aa {
        position: absolute;
        bottom: -25px;
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: rgba(255,255,255,.14);
        border: 1px solid rgba(255,255,255,.30);
        color: white;
        font-weight: 900;
        font-size: 12px;
        animation: floatUp 5s linear infinite;
    }

    .aa:nth-child(1)  { left: 5%;  animation-delay: 0s; }
    .aa:nth-child(2)  { left: 16%; animation-delay: 1.2s; }
    .aa:nth-child(3)  { left: 28%; animation-delay: 2.1s; }
    .aa:nth-child(4)  { left: 41%; animation-delay: .7s; }
    .aa:nth-child(5)  { left: 54%; animation-delay: 1.8s; }
    .aa:nth-child(6)  { left: 67%; animation-delay: 3s; }
    .aa:nth-child(7)  { left: 79%; animation-delay: 1.1s; }
    .aa:nth-child(8)  { left: 91%; animation-delay: 2.7s; }

    /* =========================
       SECTION HEADERS
       ========================= */

    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 24px 0 8px 0;
        color: #0b3b82;
        font-size: 25px;
        font-weight: 900;
        letter-spacing: -.3px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 16px;
    }

    .step-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 7px 12px;
        border-radius: 999px;
        background: #dbeafe;
        color: #174ea6;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: .6px;
    }

    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #eaf3ff 0%, #eef8ff 50%, #ecfeff 100%);
        border-right: 1px solid #bfdbfe;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.4rem;
    }

    .side-title {
        font-size: 22px;
        font-weight: 900;
        color: #0b3b82;
        margin-bottom: 5px;
    }

    .side-sub {
        color: #64748b;
        font-size: 13px;
        line-height: 1.55;
        margin-bottom: 18px;
    }

    .side-card {
        padding: 14px;
        border-radius: 15px;
        background: rgba(255,255,255,.78);
        border: 1px solid #bfdbfe;
        margin-bottom: 12px;
        box-shadow: 0 6px 18px rgba(30,64,175,.06);
    }

    /* =========================
       STREAMLIT WIDGETS
       ========================= */

    .stButton > button {
        border-radius: 12px;
        min-height: 44px;
        font-weight: 800;
        border: 1px solid #2563eb;
        color: white;
        background: linear-gradient(90deg, #2563eb, #0891b2);
        transition: all .18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 9px 22px rgba(37,99,235,.22);
        color: white;
    }

    textarea {
        border-radius: 14px !important;
        border: 1px solid #bfdbfe !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px;
        border-color: #bfdbfe;
    }

    section[data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #60a5fa;
        border-radius: 15px;
        background: rgba(248,251,255,.85);
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,.92);
        border: 1px solid #bfdbfe;
        border-radius: 17px;
        padding: 17px;
        box-shadow: 0 7px 22px rgba(15,23,42,.06);
        transition: transform .2s ease, box-shadow .2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(37,99,235,.13);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 700;
    }

    div[data-testid="stMetricValue"] {
        color: #155eef;
        font-weight: 900;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #bfdbfe;
        border-radius: 14px;
        overflow: hidden;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    button[data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 850;
        color: #475569;
        padding: 12px 14px;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #155eef;
    }

    /* =========================
       INFO CARDS
       ========================= */

    .info-card {
        background: rgba(255,255,255,.88);
        border: 1px solid #bfdbfe;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 9px 26px rgba(15,23,42,.055);
        transition: all .22s ease;
        height: 100%;
    }

    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 34px rgba(37,99,235,.11);
    }

    .info-icon {
        font-size: 28px;
        margin-bottom: 7px;
    }

    .info-title {
        color: #0b3b82;
        font-size: 17px;
        font-weight: 900;
        margin-bottom: 5px;
    }

    .info-text {
        color: #64748b;
        font-size: 13px;
        line-height: 1.6;
    }

    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        padding: 20px 0 5px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HERO HEADER
# =========================================================

st.markdown(
    """
    <div class="hero fade-in">
        <div class="hero-content">
            <div class="hero-badge">🧬 BIOINFORMATICS • PROTEIN ANALYSIS</div>

            <div class="hero-title">Protein Profiler</div>

            <div class="hero-subtitle">
                Interactive Protein Sequence Profiling & Region Mapping
            </div>

            <div class="hero-mini">
                <span class="hero-chip">Amino-acid composition</span>
                <span class="hero-chip">Hydropathy</span>
                <span class="hero-chip">Motifs</span>
                <span class="hero-chip">Region mapping</span>
            </div>
        </div>

        <div class="aa-field">
            <span class="aa">A</span>
            <span class="aa">G</span>
            <span class="aa">K</span>
            <span class="aa">L</span>
            <span class="aa">R</span>
            <span class="aa">F</span>
            <span class="aa">S</span>
            <span class="aa">Y</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# INTRO
# =========================================================

st.markdown(
    """
    <div class="info-card fade-in">
        <div class="info-icon">🔬</div>
        <div class="info-title">Protein Sequence Analysis Platform</div>
        <div class="info-text">
            Analyze protein sequences to explore sequence properties,
            amino-acid composition, hydropathy, motifs and potentially
            relevant protein regions using interactive visualizations.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SAMPLE FASTA
# =========================================================

SAMPLE = """>sp|P69905|HBA_HUMAN Hemoglobin subunit alpha
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG
KKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTP
AVHASLDKFLASVSTVLTSKYR
>sp|P01308|INS_HUMAN Insulin
MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAED
LQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN
"""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="side-title">⚙️ Analysis Settings</div>
        <div class="side-sub">
            Adjust the parameters used for hydropathy and
            protein-region detection.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-card">', unsafe_allow_html=True)

    st.markdown("### 🌊 Hydropathy")

    kd_window = st.slider(
        "Hydropathy window",
        min_value=5,
        max_value=25,
        value=9,
        step=2,
        help="Window size used for Kyte-Doolittle hydropathy.",
    )

    tm_cut = st.slider(
        "Hydrophobic region cutoff",
        min_value=1.0,
        max_value=2.5,
        value=1.6,
        step=0.1,
        help="Threshold used to identify hydrophobic / TM-like regions.",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="side-card">', unsafe_allow_html=True)

    st.markdown("### 🧩 Complexity")

    lc_cut = st.slider(
        "Low-complexity entropy cutoff",
        min_value=1.5,
        max_value=3.5,
        value=2.2,
        step=0.1,
        help="Entropy threshold used for low-complexity region detection.",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.info(
        "💡 Changing these values can change the detected protein regions."
    )


# =========================================================
# STEP 1 — INPUT
# =========================================================

st.markdown(
    '<div class="section-title"><span class="step-badge">STEP 1</span> 📄 Input Protein Sequence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">Upload a FASTA file, paste a sequence, or load the sample dataset.</div>',
    unsafe_allow_html=True,
)

input_col1, input_col2 = st.columns(2, gap="large")

with input_col1:
    st.markdown("**📂 FASTA File**")
    up = st.file_uploader(
        "Upload protein FASTA",
        type=["fasta", "fa", "faa", "txt"],
        help="Supported formats: FASTA, FA, FAA and TXT",
        label_visibility="collapsed",
    )

with input_col2:
    st.markdown("**📝 FASTA Sequence**")
    pasted = st.text_area(
        "Paste protein FASTA",
        height=130,
        placeholder=">Protein_1\nMVLSPADKTNVKAAWGKV...",
        label_visibility="collapsed",
    )

_, sample_col, _ = st.columns([1, 2, 1])

with sample_col:
    load_sample = st.button(
        "🧬 Load Sample Proteins",
        use_container_width=True,
    )


# =========================================================
# INPUT HANDLING
# =========================================================

if up is not None:
    text = up.getvalue().decode("utf-8", errors="ignore")
elif pasted.strip():
    text = pasted
elif load_sample:
    text = SAMPLE
else:
    text = ""


if not text.strip():
    st.info(
        "🧬 Upload a FASTA file, paste a protein sequence, "
        "or load the sample dataset to begin."
    )
    st.stop()


# =========================================================
# FASTA PARSING
# =========================================================

@st.cache_data(show_spinner="🔬 Parsing FASTA...")
def load_fasta(fasta_text):
    return an.parse_fasta(fasta_text)


df, engine = load_fasta(text)

df = df[df.clean_length > 0].reset_index(drop=True)

if df.empty:
    st.error(
        "❌ No valid protein sequences were found. Please check your FASTA input."
    )
    st.stop()

st.success(f"✅ FASTA successfully parsed using **{engine}**")


# =========================================================
# STEP 2 — SELECT PROTEIN
# =========================================================

st.markdown(
    '<div class="section-title"><span class="step-badge">STEP 2</span> 🧬 Select Protein Sequence</div>',
    unsafe_allow_html=True,
)

choice = st.selectbox(
    "Choose a protein for detailed analysis",
    df.id,
)

row = df[df.id == choice].iloc[0]
seq = row.cleaned_seq

if len(seq) < 10:
    st.warning(
        "⚠️ The selected sequence is very short; some analysis results may be limited."
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
        lc_cutoff=lc_cut,
    )

    motifs = an.detect_motifs(seq)

    hydro = an.hydrophobicity_profile(
        seq,
        kd_window,
    )


# =========================================================
# STEP 3 — DASHBOARD
# =========================================================

st.markdown(
    '<div class="section-title"><span class="step-badge">STEP 3</span> 📊 Protein Analysis Dashboard</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">Explore protein properties, amino-acid fingerprint, detected regions, motifs and interactive graphs.</div>',
    unsafe_allow_html=True,
)


# =========================================================
# TABS
# =========================================================

t1, t2, t3, t4, t5 = st.tabs(
    [
        "📋  OVERVIEW",
        "🧬  FINGERPRINT",
        "🗺️  PROTEIN MAP",
        "🧩  REGIONS & MOTIFS",
        "📈  GRAPHS",
    ]
)


# =========================================================
# TAB 1 — OVERVIEW
# =========================================================

with t1:

    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-icon">🧬</div>
            <div class="info-title">{row.id}</div>
            <div class="info-text">
                {str(row.description).strip()}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🧬 Sequence Length", f"{row.clean_length} aa")

    with c2:
        st.metric("✂️ Removed Characters", row.removed_chars)

    with c3:
        mw = float(props["Molecular weight (Da)"])
        st.metric("⚖️ Molecular Weight", f"{mw / 1000:.2f} kDa")

    with c4:
        st.metric("⚡ Isoelectric Point", props["Isoelectric point (pI)"])

    st.markdown("### 🔎 Protein Properties")

    properties_df = pd.DataFrame(
        props.items(),
        columns=["Property", "Value"],
    ).astype(str)

    st.dataframe(
        properties_df,
        hide_index=True,
        use_container_width=True,
    )

    if len(df) > 1:
        st.markdown("### 📊 Sequences in Input File")

        st.dataframe(
            df.drop(columns="cleaned_seq"),
            hide_index=True,
            use_container_width=True,
        )


# =========================================================
# TAB 2 — FINGERPRINT
# =========================================================

with t2:

    st.markdown("## 🧬 Amino-acid Fingerprint")

    col_a, col_b = st.columns(2, gap="large")

    with col_a:

        radar_values = list(comp.percent)
        radar_labels = list(comp.aa)

        radar = go.Figure(
            go.Scatterpolar(
                r=radar_values + [radar_values[0]],
                theta=radar_labels + [radar_labels[0]],
                fill="toself",
                name="Composition",
                line=dict(color="#2563eb", width=3),
            )
        )

        radar.update_layout(
            title="Amino-acid Composition (%)",
            height=430,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    gridcolor="#dbeafe",
                ),
                angularaxis=dict(
                    gridcolor="#dbeafe",
                ),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=30, r=30, t=60, b=30),
        )

        st.plotly_chart(radar, use_container_width=True)

    with col_b:

        g = an.group_composition(seq)

        pie = px.pie(
            g,
            names="group",
            values="percent",
            hole=0.48,
            title="Physicochemical Groups",
        )

        pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(pie, use_container_width=True)

    st.markdown("### 🧩 Positional Fingerprint")

    nb = min(60, len(seq))

    edges = np.linspace(
        0,
        len(seq),
        nb + 1,
        dtype=int,
    )

    mat = np.array(
        [
            [
                seq[edges[i]:edges[i + 1]].count(x)
                / max(1, edges[i + 1] - edges[i])
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
        title="Residue Frequency Along the Sequence",
    )

    hm.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(hm, use_container_width=True)


# =========================================================
# TAB 3 — PROTEIN MAP
# =========================================================

with t3:

    st.markdown("## 🗺️ Interactive Protein Region Map")

    region_colors = {
        "Hydrophobic / TM-like": "#f97316",
        "Low complexity": "#8b5cf6",
        "Charged-rich": "#0ea5e9",
    }

    lanes = list(region_colors.keys()) + ["Motifs"]

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.55, 0.45],
        vertical_spacing=0.08,
    )

    # Protein baseline
    fig.add_shape(
        type="rect",
        x0=1,
        x1=len(seq),
        y0=-0.05,
        y1=0.05,
        fillcolor="#93c5fd",
        line_width=0,
        row=1,
        col=1,
    )

    # Detected regions
    for r in regions.itertuples():

        if r.region not in region_colors:
            continue

        y = lanes.index(r.region) + 1

        fig.add_trace(
            go.Scatter(
                x=[
                    r.start,
                    r.end,
                    r.end,
                    r.start,
                    r.start,
                ],
                y=[
                    y - 0.35,
                    y - 0.35,
                    y + 0.35,
                    y + 0.35,
                    y - 0.35,
                ],
                fill="toself",
                mode="lines",
                line=dict(
                    color=region_colors[r.region],
                    width=2,
                ),
                fillcolor=region_colors[r.region],
                opacity=0.72,
                name=r.region,
                showlegend=False,
                hovertext=(
                    f"<b>{r.region}</b><br>"
                    f"Position: {r.start}-{r.end}<br>"
                    f"GRAVY: {r.gravy}"
                ),
                hoverinfo="text",
            ),
            row=1,
            col=1,
        )

    # Motifs
    if not motifs.empty:

        fig.add_trace(
            go.Scatter(
                x=(motifs.start + motifs.end) / 2,
                y=[len(lanes)] * len(motifs),
                mode="markers",
                marker=dict(
                    size=12,
                    symbol="diamond",
                    color="#e11d48",
                ),
                text=(
                    motifs.motif
                    + " "
                    + motifs.match
                    + " @"
                    + motifs.start.astype(str)
                ),
                hoverinfo="text",
                name="Motifs",
            ),
            row=1,
            col=1,
        )

    fig.update_yaxes(
        tickvals=list(range(1, len(lanes) + 1)),
        ticktext=lanes,
        range=[-0.6, len(lanes) + 0.6],
        row=1,
        col=1,
    )

    # Hydropathy
    fig.add_trace(
        go.Scatter(
            x=hydro.position,
            y=hydro.kd,
            line=dict(
                color="#0891b2",
                width=3,
            ),
            name="Kyte-Doolittle",
            fill="tozeroy",
            fillcolor="rgba(8,145,178,.10)",
        ),
        row=2,
        col=1,
    )

    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="#94a3b8",
        row=2,
        col=1,
    )

    fig.update_xaxes(
        title_text="Residue Position",
        row=2,
        col=1,
    )

    fig.update_yaxes(
        title_text="Hydropathy",
        row=2,
        col=1,
    )

    fig.update_layout(
        height=650,
        showlegend=False,
        title=f"Interactive Protein Map — {row.id}",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.45)",
        margin=dict(l=30, r=30, t=70, b=40),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.caption(
        "💡 Hover over regions for details • Drag to zoom • Double-click to reset"
    )


# =========================================================
# TAB 4 — REGIONS & MOTIFS
# =========================================================

with t4:

    st.markdown("## 🧩 Detected Protein Regions")

    if not regions.empty:
        st.dataframe(
            regions,
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info(
            "No regions detected with the current thresholds."
        )

    st.markdown("## 🎯 Detected Motifs")

    if not motifs.empty:
        st.dataframe(
            motifs,
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info(
            "No motifs found in the selected sequence."
        )


# =========================================================
# TAB 5 — GRAPHS
# =========================================================

with t5:

    st.markdown("## 📈 Protein Graphs")

    bar = px.bar(
        comp,
        x="aa",
        y="percent",
        title="Amino-acid Composition (%)",
        color="percent",
        color_continuous_scale="Blues",
    )

    bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.45)",
        margin=dict(l=30, r=30, t=60, b=40),
    )

    st.plotly_chart(
        bar,
        use_container_width=True,
    )

    st.markdown("## 🌊 Hydropathy Profile")

    line = px.line(
        hydro,
        x="position",
        y="kd",
        title=f"Hydropathy Profile — Window {kd_window}",
    )

    line.update_traces(
        line=dict(
            color="#2563eb",
            width=3,
        )
    )

    line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.45)",
        margin=dict(l=30, r=30, t=60, b=40),
    )

    st.plotly_chart(
        line,
        use_container_width=True,
    )

    # Multi-sequence comparison
    if len(df) > 1:

        st.markdown("## 🔬 Multi-sequence Comparison")

        rows = []

        for r in df.itertuples():

            p = an.properties(r.cleaned_seq)

            rows.append(
                {
                    "id": r.id,
                    "length": p["Length (aa)"],
                    "pI": p["Isoelectric point (pI)"],
                    "gravy": p["GRAVY (hydropathy)"],
                    "mw": p["Molecular weight (Da)"],
                }
            )

        comparison_df = pd.DataFrame(rows)

        scatter = px.scatter(
            comparison_df,
            x="pI",
            y="gravy",
            size="mw",
            hover_name="id",
            title="Multi-sequence Comparison",
        )

        scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,.45)",
        )

        st.plotly_chart(
            scatter,
            use_container_width=True,
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🧬 <b>Protein Profiler</b> &nbsp;•&nbsp;
        Sequence Analysis &nbsp;•&nbsp;
        Protein Properties &nbsp;•&nbsp;
        Hydropathy &nbsp;•&nbsp;
        Motifs &nbsp;•&nbsp;
        Region Mapping
    </div>
    """,
    unsafe_allow_html=True,
)
