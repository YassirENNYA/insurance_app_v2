import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsurAnalytics — Biais & Coûts",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design System ─────────────────────────────────────────────────────────────
PALETTE = {
    "primary":   "#0D47A1",
    "accent":    "#1565C0",
    "teal":      "#00695C",
    "amber":     "#F57F17",
    "coral":     "#C62828",
    "violet":    "#4527A0",
    "surface":   "#F8F9FC",
    "card":      "#FFFFFF",
    "border":    "#E3E8F0",
    "text":      "#0F172A",
    "muted":     "#64748B",
    "smoker_yes":"#C62828",
    "smoker_no": "#00695C",
    "male":      "#0D47A1",
    "female":    "#AD1457",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    color: {PALETTE['text']};
}}
.stApp {{ background: {PALETTE['surface']}; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {PALETTE['primary']} !important;
    border-right: none;
}}
[data-testid="stSidebar"] * {{ color: #fff !important; }}
[data-testid="stSidebar"] .stRadio label {{
    background: rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 12px;
    margin: 2px 0;
    transition: background 0.2s;
    cursor: pointer;
    display: block;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(255,255,255,0.18);
}}
[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.2) !important; }}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {{
    color: rgba(255,255,255,0.75) !important;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}}

/* Main content */
.block-container {{ padding: 2rem 2.5rem 2rem; max-width: 1400px; }}

/* Page header */
.page-hero {{
    margin-bottom: 2rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid {PALETTE['border']};
}}
.page-hero h1 {{
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    font-weight: 400;
    color: {PALETTE['text']};
    margin: 0 0 0.25rem;
    letter-spacing: -0.02em;
}}
.page-hero .sub {{
    font-size: 0.95rem;
    color: {PALETTE['muted']};
    font-weight: 300;
    margin: 0;
}}

/* KPI cards */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}}
.kpi-card {{
    background: {PALETTE['card']};
    border: 1px solid {PALETTE['border']};
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    position: relative;
    overflow: hidden;
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent-color, {PALETTE['primary']});
    border-radius: 12px 12px 0 0;
}}
.kpi-label {{
    font-size: 0.72rem;
    font-weight: 600;
    color: {PALETTE['muted']};
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin: 0 0 0.4rem;
}}
.kpi-value {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.75rem;
    color: {PALETTE['text']};
    line-height: 1;
    margin: 0;
}}
.kpi-delta {{
    font-size: 0.78rem;
    color: {PALETTE['muted']};
    margin: 0.3rem 0 0;
}}
.kpi-delta.up {{ color: {PALETTE['teal']}; }}
.kpi-delta.down {{ color: {PALETTE['coral']}; }}

/* Section titles */
.section-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    font-weight: 400;
    color: {PALETTE['text']};
    margin: 2rem 0 0.75rem;
    padding-left: 0.75rem;
    border-left: 3px solid {PALETTE['primary']};
    line-height: 1.3;
}}

/* Info / Insight box */
.insight-box {{
    background: #EEF2FF;
    border-left: 3px solid {PALETTE['primary']};
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1rem;
    font-size: 0.88rem;
    color: #1E3A5F;
    margin: 0.5rem 0 1rem;
    line-height: 1.6;
}}
.warn-box {{
    background: #FFF8E1;
    border-left: 3px solid {PALETTE['amber']};
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1rem;
    font-size: 0.88rem;
    color: #4A3000;
    margin: 0.5rem 0 1rem;
    line-height: 1.6;
}}
.danger-box {{
    background: #FFEBEE;
    border-left: 3px solid {PALETTE['coral']};
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1rem;
    font-size: 0.88rem;
    color: #4A0000;
    margin: 0.5rem 0 1rem;
    line-height: 1.6;
}}
.success-box {{
    background: #E8F5E9;
    border-left: 3px solid {PALETTE['teal']};
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1rem;
    font-size: 0.88rem;
    color: #00311E;
    margin: 0.5rem 0 1rem;
    line-height: 1.6;
}}

/* Badge */
.badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}}
.badge-blue {{ background: #DBEAFE; color: #1E40AF; }}
.badge-red {{ background: #FEE2E2; color: #991B1B; }}
.badge-green {{ background: #D1FAE5; color: #065F46; }}
.badge-amber {{ background: #FEF3C7; color: #92400E; }}

/* Filter bar */
.filter-bar {{
    background: {PALETTE['card']};
    border: 1px solid {PALETTE['border']};
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
}}
.filter-title {{
    font-size: 0.72rem;
    font-weight: 600;
    color: {PALETTE['muted']};
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}}

/* Plotly charts */
.js-plotly-plot {{ border-radius: 12px; }}

/* Metric overrides */
[data-testid="stMetric"] {{
    background: {PALETTE['card']};
    border: 1px solid {PALETTE['border']};
    border-radius: 12px;
    padding: 1rem 1.25rem;
}}
[data-testid="stMetricLabel"] {{ font-size: 0.78rem; color: {PALETTE['muted']}; font-weight: 600; }}
[data-testid="stMetricValue"] {{ font-family: 'DM Serif Display', serif; font-size: 1.6rem; }}

/* Data table */
[data-testid="stDataFrame"] {{ border-radius: 12px; overflow: hidden; }}

/* Divider */
hr {{ border-color: {PALETTE['border']} !important; margin: 1.5rem 0 !important; }}

/* Sidebar filter section label */
.sidebar-section {{
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin: 1.2rem 0 0.5rem;
}}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def chart_layout(fig, title="", height=380):
    fig.update_layout(
        title=dict(text=title, font=dict(family="DM Serif Display", size=15, color=PALETTE["text"]), x=0),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=height,
        margin=dict(l=10, r=10, t=44, b=10),
        font=dict(family="DM Sans", size=12, color=PALETTE["muted"]),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
        xaxis=dict(gridcolor="#F1F5F9", linecolor=PALETTE["border"], zeroline=False),
        yaxis=dict(gridcolor="#F1F5F9", linecolor=PALETTE["border"], zeroline=False),
    )
    return fig

def kpi(label, value, delta=None, delta_up=True, accent=None):
    accent_color = accent or PALETTE["primary"]
    delta_class = ("up" if delta_up else "down") if delta else ""
    delta_html = f'<p class="kpi-delta {delta_class}">{delta}</p>' if delta else ""
    return f"""
    <div class="kpi-card" style="--accent-color:{accent_color}">
        <p class="kpi-label">{label}</p>
        <p class="kpi-value">{value}</p>
        {delta_html}
    </div>"""

def section(title):
    st.markdown(f'<p class="section-title">{title}</p>', unsafe_allow_html=True)

def insight(msg, kind="info"):
    css = {"info": "insight-box", "warn": "warn-box", "danger": "danger-box", "success": "success-box"}
    st.markdown(f'<div class="{css.get(kind, "insight-box")}">{msg}</div>', unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("insurance.csv")
    df["age_group"] = pd.cut(df["age"], bins=[17, 30, 45, 64],
                             labels=["18-30 ans", "31-45 ans", "46-64 ans"])
    df["bmi_category"] = pd.cut(df["bmi"], bins=[0, 18.5, 25, 30, 100],
                                labels=["Sous-poids", "Normal", "Surpoids", "Obèse"])
    df["charge_group"] = pd.qcut(df["charges"], q=4,
                                 labels=["Bas (<Q1)", "Modéré (Q1-Q2)", "Élevé (Q2-Q3)", "Très élevé (>Q3)"])
    df["children_group"] = df["children"].apply(lambda x: "0" if x == 0 else ("1-2" if x <= 2 else "3+"))
    return df

df_full = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='display:flex; align-items:center; gap:10px; margin-bottom:1rem;'>
        <span style='font-size:1.8rem;'>🏥</span>
        <div>
            <div style='font-weight:600; font-size:1rem;'>InsurAnalytics</div>
            <div style='font-size:0.75rem; opacity:0.65;'>Biais & Coûts d'assurance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🏠 Tableau de bord",
        "🔍 Exploration",
        "⚠️ Détection de Biais",
        "🤖 Modélisation",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="sidebar-section">🎛 Filtres globaux</div>', unsafe_allow_html=True)

    sexes = st.multiselect("Genre", ["male", "female"], default=["male", "female"])
    smoker_filter = st.multiselect("Statut fumeur", ["yes", "no"], default=["yes", "no"])
    regions = st.multiselect("Région", df_full["region"].unique().tolist(), default=df_full["region"].unique().tolist())
    age_range = st.slider("Tranche d'âge", int(df_full["age"].min()), int(df_full["age"].max()),
                          (int(df_full["age"].min()), int(df_full["age"].max())))
    charge_range = st.slider("Charges ($)", int(df_full["charges"].min()), int(df_full["charges"].max()),
                              (int(df_full["charges"].min()), int(df_full["charges"].max())), step=500)

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:0.78rem; opacity:0.7; line-height:1.7;'>
        <b>Dataset</b> Medical Insurance Cost<br>
        <b>Source</b> Kaggle<br>
        <b>Lignes</b> {len(df_full):,}<br>
        <b>Colonnes</b> {df_full.shape[1]}
    </div>
    """, unsafe_allow_html=True)

# Apply global filters
df = df_full[
    df_full["sex"].isin(sexes) &
    df_full["smoker"].isin(smoker_filter) &
    df_full["region"].isin(regions) &
    df_full["age"].between(*age_range) &
    df_full["charges"].between(*charge_range)
].copy()

n_filtered = len(df)
pct_kept = n_filtered / len(df_full) * 100


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 : TABLEAU DE BORD
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Tableau de bord":
    st.markdown("""<div class="page-hero">
        <h1>Tableau de bord — Coûts d'Assurance Médicale</h1>
        <p class="sub">Analyse des déterminants de coût et détection de biais dans les données de tarification</p>
    </div>""", unsafe_allow_html=True)

    # Filter notice
    if n_filtered < len(df_full):
        st.markdown(f'<div class="warn-box">⚡ Filtres actifs — <b>{n_filtered:,} assurés</b> affichés sur {len(df_full):,} ({pct_kept:.0f}%)</div>', unsafe_allow_html=True)

    # KPIs row 1
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(kpi("Assurés (filtrés)", f"{n_filtered:,}", accent=PALETTE["primary"]), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi("Coût moyen", f"${df['charges'].mean():,.0f}", accent=PALETTE["accent"]), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi("Coût médian", f"${df['charges'].median():,.0f}", accent=PALETTE["teal"]), unsafe_allow_html=True)
    with k4:
        pct_s = df['smoker'].value_counts(normalize=True).get('yes', 0) * 100
        st.markdown(kpi("% Fumeurs", f"{pct_s:.1f}%", accent=PALETTE["coral"]), unsafe_allow_html=True)
    with k5:
        st.markdown(kpi("IMC moyen", f"{df['bmi'].mean():.1f}", accent=PALETTE["violet"]), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # KPIs row 2
    k6, k7, k8, k9, k10 = st.columns(5)
    with k6:
        coût_fumeur = df[df["smoker"]=="yes"]["charges"].mean()
        st.markdown(kpi("Coût moy. fumeurs", f"${coût_fumeur:,.0f}", accent=PALETTE["coral"]), unsafe_allow_html=True)
    with k7:
        coût_nonfumeur = df[df["smoker"]=="no"]["charges"].mean()
        st.markdown(kpi("Coût moy. non-fumeurs", f"${coût_nonfumeur:,.0f}", accent=PALETTE["teal"]), unsafe_allow_html=True)
    with k8:
        coût_homme = df[df["sex"]=="male"]["charges"].mean()
        st.markdown(kpi("Coût moy. hommes", f"${coût_homme:,.0f}", accent=PALETTE["primary"]), unsafe_allow_html=True)
    with k9:
        coût_femme = df[df["sex"]=="female"]["charges"].mean()
        st.markdown(kpi("Coût moy. femmes", f"${coût_femme:,.0f}", accent="#AD1457"), unsafe_allow_html=True)
    with k10:
        ratio_smoke = coût_fumeur / coût_nonfumeur if coût_nonfumeur else 0
        st.markdown(kpi("Ratio fumeur/non-fumeur", f"×{ratio_smoke:.2f}", accent=PALETTE["amber"]), unsafe_allow_html=True)

    st.markdown("---")

    # Overview charts
    col_l, col_r = st.columns([3, 2])

    with col_l:
        section("Distribution des charges médicales")
        fig = px.histogram(df, x="charges", nbins=60, color="smoker",
                           color_discrete_map={"yes": PALETTE["smoker_yes"], "no": PALETTE["smoker_no"]},
                           barmode="overlay", opacity=0.75,
                           labels={"charges": "Charges ($)", "count": "Assurés", "smoker": "Fumeur"},
                           marginal="rug")
        chart_layout(fig, height=320)
        st.plotly_chart(fig, use_container_width=True)
        insight("La distribution est bimodale : non-fumeurs (<$20k) et fumeurs (>$30k) forment deux populations distinctes.", "info")

    with col_r:
        section("Répartition par groupe d'âge")
        age_counts = df["age_group"].value_counts().reset_index()
        age_counts.columns = ["age_group", "count"]
        fig2 = px.pie(age_counts, names="age_group", values="count",
                      color_discrete_sequence=["#0D47A1", "#1565C0", "#90CAF9"],
                      hole=0.55)
        fig2.update_traces(textposition="outside", textinfo="percent+label")
        chart_layout(fig2, height=320)
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        section("Coût moyen par région et genre")
        reg_data = df.groupby(["region", "sex"])["charges"].mean().reset_index()
        fig3 = px.bar(reg_data, x="region", y="charges", color="sex", barmode="group",
                      color_discrete_map={"male": PALETTE["male"], "female": PALETTE["female"]},
                      text_auto=".0f",
                      labels={"charges": "Coût moyen ($)", "region": "Région", "sex": "Genre"})
        chart_layout(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        section("Coût moyen par catégorie d'IMC")
        bmi_data = df.groupby(["bmi_category", "smoker"])["charges"].mean().reset_index()
        fig4 = px.bar(bmi_data, x="bmi_category", y="charges", color="smoker", barmode="group",
                      color_discrete_map={"yes": PALETTE["smoker_yes"], "no": PALETTE["smoker_no"]},
                      text_auto=".0f",
                      labels={"charges": "Coût moyen ($)", "bmi_category": "Catégorie IMC", "smoker": "Fumeur"})
        chart_layout(fig4)
        st.plotly_chart(fig4, use_container_width=True)

    section("Évolution du coût moyen selon l'âge")
    age_trend = df.groupby(["age", "smoker"])["charges"].mean().reset_index()
    fig5 = px.line(age_trend, x="age", y="charges", color="smoker",
                   color_discrete_map={"yes": PALETTE["smoker_yes"], "no": PALETTE["smoker_no"]},
                   labels={"age": "Âge", "charges": "Coût moyen ($)", "smoker": "Fumeur"},
                   markers=True)
    fig5.update_traces(line_width=2.5)
    chart_layout(fig5, height=340)
    st.plotly_chart(fig5, use_container_width=True)
    insight("Les coûts augmentent linéairement avec l'âge pour les deux groupes, mais avec un écart constant et massif (~$20k) entre fumeurs et non-fumeurs.", "warn")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 : EXPLORATION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Exploration":
    st.markdown("""<div class="page-hero">
        <h1>Exploration des Données</h1>
        <p class="sub">Analyse multivariée des facteurs influençant les coûts d'assurance</p>
    </div>""", unsafe_allow_html=True)

    # Filter inline
    st.markdown('<div class="filter-bar"><div class="filter-title">🎨 Options de visualisation</div>', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        x_axis = st.selectbox("Axe X", ["age", "bmi", "children", "charges"], index=0)
    with fc2:
        y_axis = st.selectbox("Axe Y", ["charges", "bmi", "age"], index=0)
    with fc3:
        color_by = st.selectbox("Colorier par", ["smoker", "sex", "age_group", "bmi_category", "region"], index=0)
    st.markdown('</div>', unsafe_allow_html=True)

    # Scatter interactif
    section(f"Nuage de points : {x_axis} vs {y_axis}")
    color_map = {}
    if color_by == "smoker":
        color_map = {"yes": PALETTE["smoker_yes"], "no": PALETTE["smoker_no"]}
    elif color_by == "sex":
        color_map = {"male": PALETTE["male"], "female": PALETTE["female"]}
    fig_sc = px.scatter(df, x=x_axis, y=y_axis, color=color_by,
                        color_discrete_map=color_map,
                        opacity=0.55, trendline="lowess",
                        hover_data=["age", "sex", "bmi", "smoker", "region", "charges"],
                        labels={x_axis: x_axis.capitalize(), y_axis: y_axis.capitalize()})
    chart_layout(fig_sc, height=420)
    st.plotly_chart(fig_sc, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        section("Distribution des charges — Boxplots")
        group_box = st.selectbox("Grouper par", ["sex", "smoker", "age_group", "bmi_category", "region"], key="box_group")
        color_map_box = {}
        if group_box == "smoker":
            color_map_box = {"yes": PALETTE["smoker_yes"], "no": PALETTE["smoker_no"]}
        elif group_box == "sex":
            color_map_box = {"male": PALETTE["male"], "female": PALETTE["female"]}
        fig_box = px.box(df, x=group_box, y="charges", color=group_box,
                         color_discrete_map=color_map_box,
                         points="outliers",
                         labels={group_box: group_box.capitalize(), "charges": "Charges ($)"})
        chart_layout(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        section("Violons : distribution complète")
        fig_vio = px.violin(df, x=group_box, y="charges", color=group_box,
                            color_discrete_map=color_map_box,
                            box=True, points="all",
                            labels={group_box: group_box.capitalize(), "charges": "Charges ($)"})
        chart_layout(fig_vio)
        st.plotly_chart(fig_vio, use_container_width=True)

    # Corrélations
    section("Matrice de corrélations")
    corr_cols = ["age", "bmi", "children", "charges"]
    corr_df = df[corr_cols].corr()
    fig_corr = px.imshow(corr_df, text_auto=".2f",
                         color_continuous_scale=["#C62828", "#FFFFFF", "#0D47A1"],
                         zmin=-1, zmax=1,
                         labels=dict(color="Corr."))
    fig_corr.update_traces(textfont_size=14)
    chart_layout(fig_corr, height=380)
    st.plotly_chart(fig_corr, use_container_width=True)

    # Analyse multivariée
    section("Carte thermique : coût moyen par croisement de variables")
    hc1, hc2 = st.columns(2)
    with hc1:
        heat_x = st.selectbox("Variable ligne", ["age_group", "bmi_category", "region"], key="hx")
    with hc2:
        heat_y = st.selectbox("Variable colonne", ["sex", "smoker", "children_group"], key="hy")

    heat_data = df.groupby([heat_x, heat_y])["charges"].mean().reset_index()
    heat_pivot = heat_data.pivot(index=heat_x, columns=heat_y, values="charges")
    fig_heat = px.imshow(heat_pivot, text_auto=".0f",
                         color_continuous_scale="Blues",
                         labels={"color": "Coût moyen ($)"})
    chart_layout(fig_heat, height=340)
    st.plotly_chart(fig_heat, use_container_width=True)

    # Bubble chart
    section("Bubble chart : IMC × Âge × Charges")
    fig_bub = px.scatter(df.sample(min(500, len(df))), x="age", y="bmi", size="charges",
                         color="smoker", color_discrete_map={"yes": PALETTE["smoker_yes"], "no": PALETTE["smoker_no"]},
                         opacity=0.7, size_max=30,
                         labels={"age": "Âge", "bmi": "IMC", "charges": "Charges ($)", "smoker": "Fumeur"},
                         hover_data=["sex", "region", "charges"])
    chart_layout(fig_bub, height=420)
    st.plotly_chart(fig_bub, use_container_width=True)
    insight("La taille des bulles représente le montant des charges. Les fumeurs (rouge) cumulent âge élevé, IMC haut et charges maximales.", "warn")

    # Données brutes
    section("📄 Données filtrées")
    st.markdown(f"<span class='badge badge-blue'>{len(df):,} lignes</span>", unsafe_allow_html=True)
    st.dataframe(df.drop(columns=["charge_group"]), use_container_width=True, height=320)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 : DÉTECTION DE BIAIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚠️ Détection de Biais":
    from utils.fairness import demographic_parity_difference, disparate_impact_ratio

    st.markdown("""<div class="page-hero">
        <h1>Détection de Biais — Fairness Analysis</h1>
        <p class="sub">Métriques de parité démographique et d'impact disparate sur les attributs sensibles</p>
    </div>""", unsafe_allow_html=True)

    bc1, bc2 = st.columns([2, 1])
    with bc1:
        sensitive = st.selectbox("Attribut sensible à analyser",
                                 ["Genre (sex)", "Statut fumeur (smoker)", "Groupe d'âge (age_group)"])
    with bc2:
        threshold = st.slider("Seuil DI (règle des 4/5)", 0.5, 1.0, 0.8, 0.05)

    attr_map = {
        "Genre (sex)": ("sex", "female", "male"),
        "Statut fumeur (smoker)": ("smoker", "yes", "no"),
        "Groupe d'âge (age_group)": ("age_group", "18-30 ans", "46-64 ans"),
    }
    attr_col, unpriv, priv = attr_map[sensitive]

    y_pred = df["charges"].values
    sensitive_vals = df[attr_col].astype(str).values

    result_dp = demographic_parity_difference(y_true=y_pred, y_pred=y_pred, sensitive_attribute=sensitive_vals)
    result_di = disparate_impact_ratio(y_true=y_pred, y_pred=y_pred, sensitive_attribute=sensitive_vals,
                                       unprivileged_value=str(unpriv), privileged_value=str(priv))

    di_ok = result_di["ratio"] >= threshold
    gap_pct = abs(result_di["privileged_mean"] - result_di["unprivileged_mean"]) / result_di["privileged_mean"] * 100 if result_di["privileged_mean"] else 0

    st.markdown("---")

    # KPI biais
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.markdown(kpi("Différence de parité", f"${result_dp['difference']:,.0f}", accent=PALETTE["coral"]), unsafe_allow_html=True)
    with b2:
        acc = PALETTE["teal"] if di_ok else PALETTE["coral"]
        st.markdown(kpi("Ratio d'impact disparate", f"{result_di['ratio']:.3f}", accent=acc), unsafe_allow_html=True)
    with b3:
        st.markdown(kpi("Écart relatif", f"{gap_pct:.1f}%", accent=PALETTE["amber"]), unsafe_allow_html=True)
    with b4:
        verdict = "✅ Équitable" if di_ok else "⚠️ Biais détecté"
        acc2 = PALETTE["teal"] if di_ok else PALETTE["coral"]
        st.markdown(kpi(f"Verdict (seuil {threshold})", verdict, accent=acc2), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if di_ok:
        insight(f"Le ratio d'impact disparate ({result_di['ratio']:.3f}) est au-dessus du seuil ({threshold}). L'écart de tarification observé est dans les limites acceptables selon la règle des 4/5.", "success")
    else:
        insight(f"⚠️ Biais significatif détecté — ratio DI = {result_di['ratio']:.3f} < seuil {threshold}. Le groupe '{unpriv}' paie {gap_pct:.0f}% de plus que le groupe '{priv}'.", "danger")

    # Graphiques biais
    col_v1, col_v2 = st.columns(2)

    with col_v1:
        section("Coût moyen par groupe")
        group_data = df.groupby(attr_col)["charges"].agg(["mean", "median", "std", "count"]).reset_index()
        group_data.columns = [attr_col, "Moyenne", "Médiane", "Écart-type", "Effectif"]
        fig_bar = px.bar(group_data, x=attr_col, y="Moyenne", color=attr_col,
                         text_auto=".0f", error_y="Écart-type",
                         color_discrete_sequence=["#0D47A1", "#AD1457", "#00695C", "#F57F17"],
                         labels={attr_col: "", "Moyenne": "Coût moyen ($)"})
        chart_layout(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_v2:
        section("Distribution complète (violin)")
        fig_vio = px.violin(df, x=attr_col, y="charges", color=attr_col,
                            box=True, points="outliers",
                            color_discrete_sequence=["#0D47A1", "#AD1457", "#00695C", "#F57F17"],
                            labels={attr_col: "", "charges": "Charges ($)"})
        chart_layout(fig_vio)
        st.plotly_chart(fig_vio, use_container_width=True)

    # Radar des biais multi-attributs
    section("Radar de fairness — comparaison multi-attributs")
    attrs = [
        ("sex", "female", "male"),
        ("smoker", "yes", "no"),
        ("age_group", "18-30 ans", "46-64 ans"),
    ]
    radar_vals = []
    radar_labels = []
    for a_col, a_unpriv, a_priv in attrs:
        r = disparate_impact_ratio(
            y_true=df["charges"].values, y_pred=df["charges"].values,
            sensitive_attribute=df[a_col].astype(str).values,
            unprivileged_value=str(a_unpriv), privileged_value=str(a_priv))
        radar_vals.append(round(r["ratio"], 3))
        radar_labels.append(a_col)

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=radar_vals + [radar_vals[0]],
                                        theta=radar_labels + [radar_labels[0]],
                                        fill="toself", name="Ratio DI",
                                        line_color=PALETTE["primary"],
                                        fillcolor=f"rgba(13,71,161,0.15)"))
    fig_radar.add_trace(go.Scatterpolar(r=[threshold]*len(radar_labels) + [threshold],
                                        theta=radar_labels + [radar_labels[0]],
                                        mode="lines", name=f"Seuil ({threshold})",
                                        line=dict(color=PALETTE["coral"], dash="dash", width=2)))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1.2])),
                            showlegend=True, plot_bgcolor="white", paper_bgcolor="white",
                            height=400, margin=dict(l=40, r=40, t=40, b=40),
                            font=dict(family="DM Sans"))
    st.plotly_chart(fig_radar, use_container_width=True)
    insight("Le radar montre en un coup d'œil quels attributs franchissent le seuil de fairness. Plus le polygone bleu est proche du centre sur un attribut, plus le biais est fort.", "info")

    # Analyse croisée
    section("Analyse croisée : Genre × Fumeur × Âge")
    cross = df.groupby(["sex", "smoker", "age_group"])["charges"].mean().reset_index()
    fig_cross = px.bar(cross, x="age_group", y="charges", color="sex", facet_col="smoker",
                       barmode="group", text_auto=".0f",
                       color_discrete_map={"male": PALETTE["male"], "female": PALETTE["female"]},
                       labels={"age_group": "Groupe d'âge", "charges": "Coût moyen ($)", "sex": "Genre", "smoker": "Fumeur"})
    chart_layout(fig_cross, height=380)
    st.plotly_chart(fig_cross, use_container_width=True)

    # Tableau récapitulatif
    section("Tableau des métriques par groupe")
    rows = []
    for a_col, a_unpriv, a_priv in attrs:
        for grp in df[a_col].dropna().unique():
            sub = df[df[a_col] == grp]
            rows.append({
                "Attribut": a_col,
                "Groupe": str(grp),
                "Effectif": len(sub),
                "Coût moyen ($)": round(sub["charges"].mean()),
                "Coût médian ($)": round(sub["charges"].median()),
                "Écart-type ($)": round(sub["charges"].std()),
                "% de l'effectif total": f"{len(sub)/len(df)*100:.1f}%",
            })
    df_recap = pd.DataFrame(rows)
    st.dataframe(df_recap, use_container_width=True, height=320)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 : MODÉLISATION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 Modélisation":
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
    from utils.fairness import demographic_parity_difference, disparate_impact_ratio

    st.markdown("""<div class="page-hero">
        <h1>Modélisation Prédictive</h1>
        <p class="sub">Entraînement, comparaison de modèles et analyse de fairness sur les prédictions</p>
    </div>""", unsafe_allow_html=True)

    mc1, mc2 = st.columns(2)
    with mc1:
        models_selected = st.multiselect("Modèles à entraîner",
                                         ["Random Forest", "Gradient Boosting", "Régression Linéaire", "Ridge"],
                                         default=["Random Forest", "Gradient Boosting"])
    with mc2:
        test_size = st.slider("Taille du jeu de test (%)", 10, 40, 20, 5)

    @st.cache_data
    def train_models(test_sz, selected):
        df_model = df_full.copy()
        le = LabelEncoder()
        for col in ["sex", "smoker", "region"]:
            df_model[col] = le.fit_transform(df_model[col])
        df_model = df_model.drop(columns=["age_group", "bmi_category", "charge_group", "children_group"])
        X = df_model.drop("charges", axis=1)
        y = df_model["charges"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_sz/100, random_state=42)

        trained = {}
        if "Random Forest" in selected:
            m = RandomForestRegressor(n_estimators=100, random_state=42)
            m.fit(X_train, y_train)
            trained["Random Forest"] = (m, m.predict(X_test))
        if "Gradient Boosting" in selected:
            m = GradientBoostingRegressor(n_estimators=100, random_state=42)
            m.fit(X_train, y_train)
            trained["Gradient Boosting"] = (m, m.predict(X_test))
        if "Régression Linéaire" in selected:
            m = LinearRegression()
            m.fit(X_train, y_train)
            trained["Régression Linéaire"] = (m, m.predict(X_test))
        if "Ridge" in selected:
            m = Ridge()
            m.fit(X_train, y_train)
            trained["Ridge"] = (m, m.predict(X_test))

        return X_train, X_test, y_train, y_test, trained, X.columns.tolist()

    with st.spinner("Entraînement en cours…"):
        X_train, X_test, y_train, y_test, trained_models, feature_names = train_models(test_size, tuple(models_selected))

    if not trained_models:
        st.warning("Sélectionnez au moins un modèle.")
        st.stop()

    # Performances
    section("Performances des modèles")
    perf_rows = []
    for name, (m, y_pred) in trained_models.items():
        perf_rows.append({
            "Modèle": name,
            "MAE ($)": int(mean_absolute_error(y_test, y_pred)),
            "RMSE ($)": int(np.sqrt(mean_squared_error(y_test, y_pred))),
            "R²": round(r2_score(y_test, y_pred), 4),
        })
    df_perf = pd.DataFrame(perf_rows).sort_values("R²", ascending=False)

    best_model_name = df_perf.iloc[0]["Modèle"]
    p1, p2, p3, p4 = st.columns(4)
    best_row = df_perf.iloc[0]
    with p1: st.markdown(kpi("Meilleur modèle", best_model_name, accent=PALETTE["teal"]), unsafe_allow_html=True)
    with p2: st.markdown(kpi("MAE (meilleur)", f"${best_row['MAE ($)']:,}", accent=PALETTE["primary"]), unsafe_allow_html=True)
    with p3: st.markdown(kpi("RMSE (meilleur)", f"${best_row['RMSE ($)']:,}", accent=PALETTE["accent"]), unsafe_allow_html=True)
    with p4: st.markdown(kpi("R² (meilleur)", f"{best_row['R²']:.4f}", accent=PALETTE["violet"]), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df_perf, use_container_width=True, hide_index=True)

    # Comparaison graphique
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        section("Comparaison R² des modèles")
        fig_r2 = px.bar(df_perf, x="Modèle", y="R²", color="Modèle",
                        text_auto=".4f",
                        color_discrete_sequence=["#0D47A1", "#00695C", "#C62828", "#4527A0"])
        chart_layout(fig_r2)
        st.plotly_chart(fig_r2, use_container_width=True)
    with col_m2:
        section("Comparaison MAE des modèles")
        fig_mae = px.bar(df_perf, x="Modèle", y="MAE ($)", color="Modèle",
                         text_auto=",.0f",
                         color_discrete_sequence=["#0D47A1", "#00695C", "#C62828", "#4527A0"])
        chart_layout(fig_mae)
        st.plotly_chart(fig_mae, use_container_width=True)

    # Prédictions vs réelles
    section(f"Prédictions vs Valeurs réelles — {best_model_name}")
    _, y_pred_best = trained_models[best_model_name]
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=y_test.values, y=y_pred_best, mode="markers",
                                  name=best_model_name,
                                  marker=dict(color=PALETTE["primary"], opacity=0.4, size=5)))
    fig_pred.add_trace(go.Scatter(x=[y_test.min(), y_test.max()],
                                  y=[y_test.min(), y_test.max()],
                                  mode="lines", name="Parfait",
                                  line=dict(color=PALETTE["coral"], dash="dash", width=2)))
    chart_layout(fig_pred, height=400)
    st.plotly_chart(fig_pred, use_container_width=True)

    # Résidus
    section("Analyse des résidus")
    residuals = y_test.values - y_pred_best
    fig_res = px.histogram(pd.DataFrame({"résidu": residuals}), x="résidu", nbins=60,
                           color_discrete_sequence=[PALETTE["primary"]], marginal="rug",
                           labels={"résidu": "Résidu ($)"})
    chart_layout(fig_res, height=320)
    st.plotly_chart(fig_res, use_container_width=True)

    # Importance des features
    best_m = trained_models[best_model_name][0]
    if hasattr(best_m, "feature_importances_"):
        section(f"Importance des variables — {best_model_name}")
        feat_imp = pd.DataFrame({
            "Variable": feature_names, "Importance": best_m.feature_importances_
        }).sort_values("Importance", ascending=True)
        fig_imp = px.bar(feat_imp, x="Importance", y="Variable", orientation="h",
                         color="Importance", color_continuous_scale="Blues",
                         text_auto=".3f")
        chart_layout(fig_imp, height=380)
        st.plotly_chart(fig_imp, use_container_width=True)
        insight(f"Le tabagisme (<b>smoker</b>) est de loin la variable la plus prédictive des charges médicales, suivi de l'âge et de l'IMC.", "warn")

    # Fairness sur prédictions
    st.markdown("---")
    section("⚖️ Fairness sur les prédictions du modèle")
    df_test_full = df_full.iloc[X_test.index].copy()
    df_test_full["y_pred"] = y_pred_best

    fair_rows = []
    for a_col, a_unpriv, a_priv in [("sex", "female", "male"), ("smoker", "yes", "no"), ("age_group", "18-30 ans", "46-64 ans")]:
        r_di = disparate_impact_ratio(
            y_true=df_test_full["charges"].values, y_pred=df_test_full["y_pred"].values,
            sensitive_attribute=df_test_full[a_col].astype(str).values,
            unprivileged_value=str(a_unpriv), privileged_value=str(a_priv))
        r_dp = demographic_parity_difference(
            y_true=df_test_full["charges"].values, y_pred=df_test_full["y_pred"].values,
            sensitive_attribute=df_test_full[a_col].astype(str).values)
        fair_rows.append({
            "Attribut": a_col,
            "Groupe défavorisé": a_unpriv,
            "Groupe référence": a_priv,
            "Ratio DI": round(r_di["ratio"], 3),
            "Diff. parité ($)": int(r_dp["difference"]),
            "Verdict": "✅ OK" if r_di["ratio"] >= 0.8 else "⚠️ Biais",
        })
    df_fair = pd.DataFrame(fair_rows)
    st.dataframe(df_fair, use_container_width=True, hide_index=True)

    # Performances par sous-groupe
    section("Performances par sous-groupe (genre)")
    for grp in ["male", "female"]:
        mask = df_test_full["sex"] == grp
        if mask.sum() > 0:
            mae_g = mean_absolute_error(df_test_full.loc[mask, "charges"], df_test_full.loc[mask, "y_pred"])
            r2_g = r2_score(df_test_full.loc[mask, "charges"], df_test_full.loc[mask, "y_pred"])
            badge = "badge-blue" if grp == "male" else "badge-red"
            st.markdown(f"""<span class='badge {badge}'>{grp.capitalize()}</span>
            &nbsp; MAE : <b>${mae_g:,.0f}</b> &nbsp;|&nbsp; R² : <b>{r2_g:.4f}</b>
            <br><br>""", unsafe_allow_html=True)
