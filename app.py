# run with streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import time
import random
import re
from shapely import wkt
from shapely.geometry import Point

st.set_page_config(
    page_title="Illegal Sand Mining in India",
    page_icon="🏜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@300;400;600&display=swap');

    html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
    .stApp { background-color: #f9f5ef; }

    [data-testid="stSidebar"] { background-color: #1c1a17; color: #e8dcc8; }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span { color: #c9b99a !important; font-family: 'Source Sans 3', sans-serif; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2 {
        color: #e8a838 !important;
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        border-bottom: 1px solid #3a3530;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #1c1a17;
        border-radius: 8px 8px 0 0;
        padding: 4px 4px 0 4px;
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        color: #9a8c78;
        border-radius: 6px 6px 0 0;
        font-family: 'Source Sans 3', sans-serif;
        font-size: 0.9rem;
        letter-spacing: 0.04em;
        font-weight: 600;
        padding: 8px 20px;
        border: none;
    }
    .stTabs [aria-selected="true"] { background-color: #e8a838 !important; color: #1c1a17 !important; }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #f9f5ef;
        border: 1px solid #e0d5c4;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1.5rem;
    }

    h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.4rem !important;
        font-weight: 900 !important;
        color: #1c1a17 !important;
        letter-spacing: -0.01em;
        line-height: 1.1;
    }
    h2 { font-family: 'Playfair Display', serif !important; color: #2e2b26 !important; font-size: 1.6rem !important; }
    h3 {
        font-family: 'Source Sans 3', sans-serif !important;
        color: #5a4e3c !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    p, li { color: #3a3530; line-height: 1.75; }

    [data-testid="stMetric"] {
        background-color: #fff8ee;
        border: 1px solid #e0d5c4;
        border-left: 4px solid #e8a838;
        border-radius: 6px;
        padding: 1rem 1.25rem;
    }
    [data-testid="stMetricLabel"] { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: #7a6e5e !important; }
    [data-testid="stMetricValue"] { font-family: 'Playfair Display', serif; font-size: 2rem !important; color: #1c1a17 !important; }

    hr { border-color: #e0d5c4; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f0ebe0; }
    ::-webkit-scrollbar-thumb { background: #c9b99a; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# Original quotes
QUOTES = [
    "Sand is the second most exploited resource in the world, after water.",
    "If you remove sand from the river, you are digging your own grave. — Dinesh Kumar Mishra",
    "Unchecked sand extraction causes irreversible damage to river ecosystems. — Bidyut Mohanty",
    "It is a big challenge to stop illegal sand mining, because money drives everything. — S. Chandrasekhar",
    "We never know the worth of water until the well is dry. — Thomas Fuller",
    "Rivers are the soul of our civilization, and sand is their body.",
    "Over the years, India's rivers have been badly affected by unrestricted sand mining. — National Green Tribunal",
    "Mining jumped 14.7× after the PMAY-U housing scheme launched in 2015.",
]

def show_loading_page():
    st.markdown("<h1 style='text-align:center; margin-top:3rem;'> 🏜️Illegal Sand Mining in India</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#7a6e5e; font-size:1.1rem;'>Loading data & preparing your dashboard…</p>", unsafe_allow_html=True)
    quote_placeholder = st.empty()
    progress_bar = st.progress(0)
    for i in range(101):
        if i % 12 == 0:
            quote = random.choice(QUOTES)
            quote_placeholder.markdown(
                f"<blockquote style='border-left:4px solid #e8a838; padding:0.5rem 1rem; "
                f"color:#5a4e3c; font-style:italic; background:#fff8ee; border-radius:0 6px 6px 0;'>"
                f"{quote}</blockquote>",
                unsafe_allow_html=True
            )
        progress_bar.progress(i)
        time.sleep(0.04)
    st.success("✅ Data loaded successfully.")


# Geometry parsing — handles WKT, raw "lat,lon", and GeoJSON strings
def parse_geom_to_latlon(geom_val):
    """
    Try every known format for the geom column and return (lat, lon) or (nan, nan).
    Handles:
      - WKT:          POINT (lon lat)  /  POINT(lon lat)
      - raw pair:     "lat,lon"  or  "lon,lat"  (heuristic: lat is between -90..90 & lon -180..180)
      - GeoJSON str:  {"type":"Point","coordinates":[lon,lat]}
    """
    if pd.isna(geom_val) or str(geom_val).strip() == '':
        return np.nan, np.nan

    s = str(geom_val).strip()

    # ── WKT POINT ────────────────────────────────────────────────────
    wkt_match = re.match(r'POINT\s*\(\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*\)', s, re.IGNORECASE)
    if wkt_match:
        lon, lat = float(wkt_match.group(1)), float(wkt_match.group(2))
        return lat, lon

    # ── Two bare numbers (lat,lon or lon,lat) ────────────────────────
    pair_match = re.match(r'^\s*(-?\d+\.?\d*)\s*[,\s]\s*(-?\d+\.?\d*)\s*$', s)
    if pair_match:
        a, b = float(pair_match.group(1)), float(pair_match.group(2))
        # India bounding box heuristic: lat 6–36, lon 68–98
        if 6 <= a <= 36 and 68 <= b <= 98:
            return a, b
        if 6 <= b <= 36 and 68 <= a <= 98:
            return b, a
        return a, b   # best guess

    # ── GeoJSON-like string ───────────────────────────────────────────
    coord_match = re.search(r'"coordinates"\s*:\s*\[\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)', s)
    if coord_match:
        lon, lat = float(coord_match.group(1)), float(coord_match.group(2))
        return lat, lon

    # ── Try shapely wkt as last resort ───────────────────────────────
    try:
        geom = wkt.loads(s)
        return geom.y, geom.x
    except Exception:
        pass

    return np.nan, np.nan


# Data loading
@st.cache_data
def load_data():
    mining_df = pd.read_csv("data/final_unified_geo_data_rows.csv")

    # Parse geometry into lat/lon regardless of source format
    if 'geom' in mining_df.columns:
        latlon = mining_df['geom'].apply(parse_geom_to_latlon)
        mining_df['latitude']  = latlon.apply(lambda x: x[0])
        mining_df['longitude'] = latlon.apply(lambda x: x[1])
    elif 'latitude' in mining_df.columns and 'longitude' in mining_df.columns:
        mining_df['latitude']  = pd.to_numeric(mining_df['latitude'],  errors='coerce')
        mining_df['longitude'] = pd.to_numeric(mining_df['longitude'], errors='coerce')
    else:
        mining_df['latitude']  = np.nan
        mining_df['longitude'] = np.nan

    mining_df = mining_df.dropna(subset=['latitude', 'longitude'])

    india_gdf = gpd.read_file("india_district.geojson")

    court_df      = pd.read_csv("data/indiasandwatch/court_docs.csv",  header=1)
    news_df       = pd.read_csv("data/indiasandwatch/news_reports.csv", header=1)
    mining_obs_df = pd.read_csv("data/indiasandwatch/mining_obs.csv",   header=1)

    def parse_location(loc):
        if pd.isna(loc):
            return pd.Series([np.nan, np.nan])
        match = re.search(r"(-?\d+\.\d+),\s*(-?\d+\.\d+)", str(loc))
        if match:
            return pd.Series([float(match.group(1)), float(match.group(2))])
        return pd.Series([np.nan, np.nan])

    mining_obs_df[['latitude', 'longitude']] = mining_obs_df['Location'].apply(parse_location)
    mining_obs_df = mining_obs_df.dropna(subset=['latitude', 'longitude'])

    return mining_df, india_gdf, court_df, news_df, mining_obs_df


# Incident count per district — spatial join with name-match fallback
# +
def build_state_counts(mining_df, india_gdf):

    india_gdf = india_gdf.copy()

    # Find state column in shapefile
    state_field = next((c for c in ['state', 'STATE', 'NAME_1'] if c in india_gdf.columns), None)

    if state_field is None or 'state' not in mining_df.columns:
        india_gdf['incident_count'] = 0
        return india_gdf

    # Normalize names
    mining_states = (
        mining_df['state']
        .dropna()
        .str.strip()
        .str.lower()
    )

    counts = mining_states.value_counts()

    india_gdf['incident_count'] = (
        india_gdf[state_field]
        .str.strip()
        .str.lower()
        .map(counts)
        .fillna(0)
        .astype(int)
    )

    return india_gdf

def get_state_gdf(india_gdf):

    state_field = next((c for c in ['state', 'STATE', 'NAME_1'] if c in india_gdf.columns), None)

    if state_field is None:
        return india_gdf

    # Dissolve into state-level polygons
    state_gdf = india_gdf.dissolve(by=state_field, as_index=False)

    return state_gdf, state_field

def build_state_color_counts(mining_df, india_gdf):

    india_gdf = india_gdf.copy()

    state_field = next((c for c in ['state', 'STATE', 'NAME_1'] if c in india_gdf.columns), None)

    if state_field is None or 'state' not in mining_df.columns:
        india_gdf['state_color_count'] = 0
        return india_gdf

    # count incidents per state
    state_counts = (
        mining_df['state']
        .dropna()
        .str.strip()
        .str.lower()
        .value_counts()
    )

    # assign same state count to all districts in that state
    india_gdf['state_color_count'] = (
        india_gdf[state_field]
        .str.strip()
        .str.lower()
        .map(state_counts)
        .fillna(0)
        .astype(int)
    )

    return india_gdf

def build_incident_counts_all(mining_df, news_df, court_df, mining_obs_df, india_gdf):
    india_gdf = india_gdf.copy()
    india_gdf['incident_count'] = 0

    dist_field  = next((c for c in ['district', 'DISTRICT', 'dtname', 'NAME_2'] if c in india_gdf.columns), None)
    state_field = next((c for c in ['state', 'STATE', 'NAME_1'] if c in india_gdf.columns), None)

    total_counts = pd.Series(dtype=int)

    # ─────────────────────────────
    # 1. MINING DF (lat/lon → spatial)
    # ─────────────────────────────
    try:
        pts = gpd.GeoDataFrame(
            mining_df,
            geometry=gpd.points_from_xy(mining_df['longitude'], mining_df['latitude']),
            crs='EPSG:4326'
        )

        gdf = india_gdf.to_crs('EPSG:4326')
        joined = gpd.sjoin(pts, gdf[['geometry']], how='left', predicate='within')

        spatial_counts = joined['index_right'].value_counts()
        total_counts = total_counts.add(spatial_counts, fill_value=0)

    except Exception:
        pass

    # ─────────────────────────────
    # 2. NEWS DF (district-based)
    # ─────────────────────────────
    if 'District' in news_df.columns:
        news_counts = (
            news_df['District']
            .dropna()
            .str.strip().str.lower()
            .value_counts()
        )

        mapped = (
            india_gdf[dist_field]
            .str.strip().str.lower()
            .map(news_counts)
            .fillna(0)
        )

        total_counts = total_counts.add(mapped, fill_value=0)

    # ─────────────────────────────
    # 3. COURT DF (district-based)
    # ─────────────────────────────
    if 'District' in court_df.columns:
        court_counts = (
            court_df['District']
            .dropna()
            .str.strip().str.lower()
            .value_counts()
        )

        mapped = (
            india_gdf[dist_field]
            .str.strip().str.lower()
            .map(court_counts)
            .fillna(0)
        )

        total_counts = total_counts.add(mapped, fill_value=0)

    # ─────────────────────────────
    # 4. MINING OBS (lat/lon → spatial)
    # ─────────────────────────────
    try:
        pts_obs = gpd.GeoDataFrame(
            mining_obs_df,
            geometry=gpd.points_from_xy(mining_obs_df['longitude'], mining_obs_df['latitude']),
            crs='EPSG:4326'
        )

        gdf = india_gdf.to_crs('EPSG:4326')
        joined_obs = gpd.sjoin(pts_obs, gdf[['geometry']], how='left', predicate='within')

        obs_counts = joined_obs['index_right'].value_counts()
        total_counts = total_counts.add(obs_counts, fill_value=0)

    except Exception:
        pass

    # Apply counts
    india_gdf['incident_count'] = (
        india_gdf.index.map(total_counts)
        .fillna(0)
        .astype(int)
    )

    return india_gdf


# +
# Map builder
# +
def create_map(mining_df, news_df, court_df, mining_obs_df, india_gdf):

    m = folium.Map(location=[22.5, 78.9], zoom_start=5,
                   tiles='CartoDB positron', attr='© CartoDB')
    m.fit_bounds([[6.5, 68.1], [35.5, 97.4]])

    india_gdf = build_incident_counts_all(
    mining_df, news_df, court_df, mining_obs_df, india_gdf)
    india_gdf = build_state_color_counts(mining_df, india_gdf)

    dist_field  = next((c for c in ['district', 'DISTRICT', 'dtname', 'NAME_2'] if c in india_gdf.columns), None)
    state_field = next((c for c in ['state', 'STATE', 'NAME_1'] if c in india_gdf.columns), None)

    # Give every row a stable string key for Choropleth binding
    india_gdf = india_gdf.reset_index(drop=True)
    india_gdf['_id'] = india_gdf.index.astype(str)

    # ── Choropleth layer (handles data binding reliably) ─────────────
    folium.Choropleth(
    geo_data=india_gdf,
    name='District Shading',
    data=india_gdf,
    columns=[india_gdf.index, 'incident_count'],
    key_on='feature.id',   # 👈 important
    fill_color='YlOrRd',
    fill_opacity=0.65,
    line_opacity=0.3,
    nan_fill_color='#f5efe3',
    legend_name='Mining Incidents per District',
).add_to(m)

    # ── Invisible GeoJson overlay just for hover tooltips ─────────────
    tooltip_fields, tooltip_aliases = [], []
    if dist_field:
        tooltip_fields.append(dist_field);  tooltip_aliases.append('District:')
    if state_field:
        tooltip_fields.append(state_field); tooltip_aliases.append('State:')
    # tooltip_fields.append('incident_count'); tooltip_aliases.append('Incidents:')

    folium.GeoJson(
        india_gdf,
        name='District Tooltips',
        style_function=lambda _: {
            'fillColor': 'transparent', 'color': 'transparent',
            'weight': 0, 'fillOpacity': 0,
        },
        highlight_function=lambda _: {
            'fillColor': '#922b21', 'color': '#1c1a17',
            'weight': 2, 'fillOpacity': 0.25,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=tooltip_aliases,
            localize=True, sticky=True, labels=True,
            style=(
                "background-color: #1c1a17; color: #e8dcc8; "
                "font-family: 'Source Sans 3', sans-serif; "
                "font-size: 13px; padding: 8px 12px; border-radius: 4px;"
            ),
        ),
    ).add_to(m)

    # Mining observation markers
    if mining_obs_df is not None and len(mining_obs_df) > 0:
        cluster_obs = MarkerCluster(name='Mining Observations').add_to(m)
        for _, row in mining_obs_df.iterrows():
            title = row.get('Title', row.get('title', 'Mining Observation'))
            desc  = row.get('Description', row.get('description', ''))
            popup_html = (
                f"<div style='font-family:sans-serif; min-width:160px;'>"
                f"<b style='color:#c98a1a;'>⚠ Mining Obs</b><br>"
                f"<span style='font-size:13px;'>{title}</span>"
                f"{'<br><small>' + str(desc)[:120] + '…</small>' if desc else ''}"
                f"</div>"
            )
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=str(title)[:60],
                icon=folium.Icon(color='orange', icon='exclamation-sign', prefix='glyphicon'),
            ).add_to(cluster_obs)

    # Unified geo markers
    if len(mining_df) > 0:
        cluster_unified = MarkerCluster(name='Verified Incidents').add_to(m)
        for _, row in mining_df.iterrows():
            desc  = str(row.get('description', row.get('raw_location', 'N/A')))[:120]
            state = row.get('state', '')
            popup_html = (
                f"<div style='font-family:sans-serif; min-width:160px;'>"
                f"<b style='color:#c0392b;'>🔴 Mining Incident</b><br>"
                f"{'<small>📍 ' + str(state) + '</small><br>' if state else ''}"
                f"<small>{desc}…</small>"
                f"</div>"
            )
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=str(row.get('district', row.get('state', 'Incident')))[:60],
                icon=folium.Icon(color='red', icon='map-marker', prefix='glyphicon'),
            ).add_to(cluster_unified)

    folium.LayerControl().add_to(m)
    return m


# +
# Main
# +
def main():
    if 'loaded' not in st.session_state:
        show_loading_page()
        st.session_state.loaded = True
        st.rerun()

    mining_df, india_gdf, court_df, news_df, mining_obs_df = load_data()

    # ── Static sidebar ────────────────────────────────────────────────
    st.sidebar.markdown("## Map Legend")
    st.sidebar.markdown("""
<div style='color:#e8dcc8; font-size:0.88rem; line-height:1.8;'>

<div style='margin-bottom:14px;'>
<div style='font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; color:#7a6e5e; margin-bottom:6px;'>District shading</div>
<div style='display:flex; align-items:center; gap:10px; margin:5px 0;'>
  <div style='width:14px;height:14px;border-radius:3px;background:#c0392b;opacity:0.7;flex-shrink:0;'></div>
  <span>High incident density</span>
</div>
<div style='display:flex; align-items:center; gap:10px; margin:5px 0;'>
  <div style='width:14px;height:14px;border-radius:3px;background:#c0392b;opacity:0.35;flex-shrink:0;'></div>
  <span>Moderate incidents</span>
</div>
<div style='display:flex; align-items:center; gap:10px; margin:5px 0;'>
  <div style='width:14px;height:14px;border-radius:3px;background:#e8a838;opacity:0.15;flex-shrink:0;'></div>
  <span>No recorded incidents</span>
</div>
</div>

<div style='margin-bottom:14px;'>
<div style='font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; color:#7a6e5e; margin-bottom:6px;'>Markers</div>
<div style='display:flex; align-items:center; gap:10px; margin:5px 0;'>
  <span style='font-size:1rem;'>🔴</span><span>Verified mining incident</span>
</div>
<div style='display:flex; align-items:center; gap:10px; margin:5px 0;'>
  <span style='font-size:1rem;'>🟠</span><span>Field observation</span>
</div>
</div>

</div>
""", unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("## Data on Map")
    st.sidebar.markdown("""
<div style='color:#c9b99a; font-size:0.88rem; line-height:2;'>

<div style='font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; color:#7a6e5e; margin-bottom:2px;'>Boundaries</div>
India district polygons<br>
<span style='color:#7a6e5e; font-size:0.82rem;'>Hover any district to see its incident count</span>

<br>

<div style='font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; color:#7a6e5e; margin-bottom:2px; margin-top:8px;'>Verified incidents</div>
2,212 geo-coded cases · 2001–2026<br>
<span style='color:#7a6e5e; font-size:0.82rem;'>Source: IndiaSandWatch unified dataset</span>

<br>

<div style='font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; color:#7a6e5e; margin-bottom:2px; margin-top:8px;'>Field observations</div>
375 on-ground observation points<br>
<span style='color:#7a6e5e; font-size:0.82rem;'>Source: IndiaSandWatch mining_obs</span>

<br>

<div style='font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; color:#7a6e5e; margin-bottom:2px; margin-top:8px;'>Coverage</div>
28+ states · 36 states/UTs total

</div>
""", unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<small style='color:#6a5f4f;'>Clusters expand on click · Layer control top-right of map</small>",
        unsafe_allow_html=True
    )

    # ── Tabs ──────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["Illegal Sand Mining Map", "Correlations", "Study on Sand Mining"])

    with tab1:
        st.markdown(
            "<h1>Illegal Sand Mining Interactive Map</h1>"
            "<p style='color:#7a6e5e; margin-top:-0.5rem; font-size:1.05rem;'>"
            "Hover over any district to see its recorded incident count. "
            "Click clusters to expand individual markers.</p>",
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Incidents", "2,212")
        c2.metric("States Affected", "28+")
        c3.metric("Top State", "Bihar · 193")
        c4.metric("Post-PMAY Surge", "14.7×")

        st.markdown("<br>", unsafe_allow_html=True)

        m = create_map(mining_df, news_df, court_df, mining_obs_df, india_gdf)
        st_folium(m, width="100%", height=580, returned_objects=[])

    with tab2:
        st.markdown("<h1>Visualization Gallery</h1>", unsafe_allow_html=True)

        st.markdown("### Correlation Heatmap of Indicators")
        try:
            st.image("outputs/correlation_heatmap_indicators.png", width="stretch")
        except Exception:
            st.info("Image not found: outputs/correlation_heatmap_indicators.png")

        st.markdown("""
**What it shows:** Correlations between mining, construction, and socioeconomic indicators.

**How to read:** Red = positive correlation, blue = negative. Stronger colour = stronger relationship.

**Key finding:** Mining incidents correlate strongly with PMAY construction scale, but weakly with poverty or literacy rates, illegal mining is demand-driven, not desperation-driven.
        """)

        st.divider()

        gallery_items = [
            ("Mining Observations Heatmap",     "outputs/heatmap_mining_observations.png",
             "Density of mining observations across India.",
             "Darker areas = higher mining activity. Bihar and UP dominate.",
             "Mining hotspots are in economically vulnerable supply states."),
            ("Geographic Distribution by State", "outputs/geographic_distribution_bars.png",
             "Bar chart of mining incidents by state.",
             "Bar height = number of incidents. Bihar leads with 193.",
             "Mining concentrates in supply states, not demand/construction states."),
            ("Dilapidated Housing Choropleth",   "outputs/choropleth_housing_dilapidated.html",
             "Dilapidated housing percentage by state.",
             "Darker shading = higher share of poor housing stock.",
             "Poor housing states have more mining, but PMAY mediates the link."),
            ("Crime Intensity Heatmap",          "outputs/heatmap_crime_intensity.png",
             "Crime rates across Indian cities.",
             "Darker = higher crime intensity.",
             "Crime hotspots often overlap with mining areas."),
            ("Temporal Surge in Mining",         "sangam_ganga_figures/fig_temporal_surge.png",
             "Annual illegal mining incidents 2010–2025, split pre/post-PMAY.",
             "Blue = pre-2015 baseline, red = post-launch surge.",
             "Mining rose from 13/year pre-2015 to 191/year post-2015, a 14.7× increase."),
            ("Event Study: PMAY Impact",         "sangam_ganga_figures/fig_event_study.png",
             "DiD coefficients showing effect of high-PMAY states over time.",
             "Dots above zero post-2015 = significant mining increase after PMAY launch.",
             "Confirms causal impact of housing policy on illegal extraction."),
            ("Synthetic Control: Uttar Pradesh", "sangam_ganga_figures/fig_synthetic_control.png",
             "Actual UP mining vs. synthetic counterfactual.",
             "Gap post-2015 shows the causal PMAY effect on UP mining.",
             "UP mining is +158% above the counterfactual without PMAY."),
            ("Ganga Conductivity Time Series",   "sangam_ganga_figures/fig_ganga_sangam_timeseries.png",
             "Water quality sensors showing conductivity during dry seasons.",
             "Peaks in Nov–Feb coincide with peak mining and low water levels.",
             "Mining correlates with riverbed disturbance and water degradation."),
            ("Spatial Clusters: Construction vs Mining", "sangam_ganga_figures/fig_spatial_clusters.png",
             "Side-by-side: PMAY allocation vs mining incidents by state.",
             "Visual decoupling, mining and construction occur in different states.",
             "Supply and demand are spatially separated across state borders."),
        ]

        for title, path, desc, reading, insight in gallery_items:
            st.markdown(f"### {title}")
            try:
                if path.endswith('.html'):
                    st.components.v1.html(open(path).read(), height=420)
                else:
                    st.image(path, width="stretch")
            except Exception:
                st.info(f"📂 File not found: {path}")
            col_a, col_b, col_c = st.columns(3)
            col_a.markdown(f"**What it shows**\n\n{desc}")
            col_b.markdown(f"**How to read**\n\n{reading}")
            col_c.markdown(f"**Key finding**\n\n{insight}")
            st.divider()

    with tab3:
        st.markdown("<h1>Project Results & Findings</h1>", unsafe_allow_html=True)
        st.markdown("""
## Executive Summary

This study analysed illegal sand mining in India using spatial statistics, causal inference, and environmental monitoring.
The central finding: the 2015 PMAY-U housing scheme caused a **14.7× surge** in illegal mining, with extraction spatially
decoupled from construction demand, occurring primarily in economically vulnerable supply states.

---

## Key Findings

### 1. Causal Impact of Construction Policy
- **Difference-in-Differences:** High-PMAY states saw 158% more mining post-2015
- **Event Study:** Parallel trends hold pre-2015; mining diverges sharply after PMAY launch
- **Synthetic Control:** UP mining is +158% above its counterfactual without PMAY
- **Regression:** PMAY scale explains 58% of mining variance; socioeconomic factors are secondary

### 2. Spatial Patterns & Hotspots
- **Top states:** Bihar (193 incidents), Uttar Pradesh (48), West Bengal (48), Madhya Pradesh (43)
- **Spatial decoupling:** Bivariate Moran's I = 0.033 (p = 0.42), no co-clustering with construction
- **KDE analysis:** Hotspots concentrated in the Gangetic plain and central India
- **LISA:** Significant local spatial autocorrelation in mining clusters

### 3. Environmental Impacts
- Conductivity spikes at Ganga/Sangam sensors during dry seasons (Nov–Feb) correlate with peak mining
- Mining coincides with WQI deterioration and ecosystem stress
- Illegal extraction threatens aquifer recharge in riverbed sponges

### 4. Economic & Social Dimensions
- Crime hotspots spatially coincide with mining areas
- Poverty and literacy have weak direct effects; construction demand, not desperation, drives mining
- Urbanisation shows no significant independent effect

### 5. Methodological Approach
- **Spatial statistics:** Moran's I, LISA, GWR, KDE
- **Causal inference:** DiD, event studies, synthetic controls, IV regression
- **Machine learning:** Random Forest (PMAY most predictive feature)
- **Time series:** Seasonal decomposition, Granger causality

---

## Data Sources

| Dataset | Coverage | Scale |
|---|---|---|
| Mining incidents (IndiaSandWatch) | 2001–2026 | 2,212 verified cases |
| PMAY-U allocations | 2015–2024 | State / district |
| Economic indicators (Census 2011) | Literacy, BPL, urbanisation | State |
| Ganga/Sangam water sensors | 2019–2020 | Point locations |
| IPC crime statistics | 54 urban centres | City |
| Geographic coverage | 36 states/UTs | 375 mining obs. points |

---

## Policy Implications

**Immediate actions:**
1. Develop legal sand mining infrastructure in high-demand states to reduce illegal supply pressure
2. Focus enforcement on Bihar, UP, and MP, the primary sand mafia hotspots
3. Implement real-time river quality monitoring at active mining sites
4. Invest in economic alternatives for communities dependent on informal extraction

**Long-term reforms:**
1. Strengthen environmental clearances and monitoring for sand permits
2. Create a national sand supply coordination policy to address inter-state decoupling
3. Deploy satellite monitoring and AI for real-time illegal mining detection
4. Involve local communities in sustainable extraction governance

---

## Limitations & Future Research

- District-level analysis would reveal finer spatial patterns
- Pre-2015 mining data is sparse, a longer time series would sharpen causal estimates
- Sand mafia economics and enforcement failures warrant dedicated ethnographic research
- Experimental evaluation of alternative sand supply interventions is needed

---

*Research conducted using rigorous statistical methods across spatial analysis, causal inference, and environmental monitoring.*
        """)


if __name__ == "__main__":
    main()