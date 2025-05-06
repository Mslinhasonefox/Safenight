# ---------- Safenight interactive dashboard ----------
import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components

# --- page & global style ----------------------------------------------------
st.set_page_config(page_title="Safenight – Night‑route Safety",
                   layout="wide")
st.markdown(
    """
    <style>
    body       { background-color:#ffffff; }
    .titlebox  { font-family: monospace; font-size:60px;
                 text-align:center; margin:10px 0 30px 0;
                 letter-spacing:2px; color:#555;
                 text-shadow:0 0 8px rgba(0,0,0,.25);}
    </style>""",
    unsafe_allow_html=True
)
st.markdown('<div class="titlebox">Safenight</div>', unsafe_allow_html=True)

# --- build 4 main modules (tabs) -------------------------------------------
tab_density, tab_lamp, tab_cctv, tab_score = st.tabs(
    ["Population‑density roads", "Lamp posts", "CCTV layer", "Safety score map"]
)

# ---------------------------------------------------------------------------
# helper: embed folium map in Streamlit
def show_map(fmap, height=700):
    components.html(fmap._repr_html_(), height=height, scrolling=False)

# base location for centering
CENTER = [22.284, 114.137]
TILES  = "cartodb dark_matter"

# ---------------------------------------------------------------------------
# 1) Population‑density roads (Line layer)
with tab_density:
    st.subheader("Population‑density road segments")
    with st.spinner("Loading road layer …"):
        roads = gpd.read_file("safenight/HKU_ROUTE_MEAN_PopDen.zip")
        m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
        for _, r in roads.iterrows():
            folium.GeoJson(
                r.geometry,
                style_function=lambda f: {"color": "orange", "weight": 3},
                tooltip=f"Population density: {r['MEAN']}"
            ).add_to(m)
        show_map(m)

# ---------------------------------------------------------------------------
# 2) Lamp posts (Point layer)
with tab_lamp:
    st.subheader("Lamp‑post distribution and scores")
    with st.spinner("Loading lamp layer …"):
        lamps = gpd.read_file("safenight/Lamppost_HKU.zip")
        m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
        cluster = MarkerCluster().add_to(m)
        for _, r in lamps.iterrows():
            folium.Marker(
                location=[r.geometry.y, r.geometry.x],
                popup=f"Lamp type: {r['Lamp_Type']}<br>Score: {r['Safety_Score']}",
                icon=folium.Icon(color="lightgray", icon="lightbulb", prefix="fa")
            ).add_to(cluster)
        show_map(m)

# ---------------------------------------------------------------------------
# 3) CCTV layer (Point layer, no pop‑up)
with tab_cctv:
    st.subheader("CCTV camera locations")
    with st.spinner("Loading CCTV layer …"):
        cams = gpd.read_file("safenight/CCTV_all_fc.zip")
        m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
        for _, r in cams.iterrows():
            folium.CircleMarker(
                location=[r.geometry.y, r.geometry.x],
                radius=3, color="cyan", fill=True, fill_opacity=0.7
            ).add_to(m)
        show_map(m)

# ---------------------------------------------------------------------------
# 4) Safety‑score road layer (Line + 4 scores pop‑up)
with tab_score:
    st.subheader("Composite safety‑score map")
    with st.spinner("Loading score layer …"):
        scored = gpd.read_file("safenight/roads_scored_new.geojson")
        m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
        for _, r in scored.iterrows():
            popup = (
                f"<b>Total score:</b> {r['total_safety_score']}<br>"
                f"<b>Lamp score:</b> {r['lamp_score']}<br>"
                f"<b>CCTV score:</b> {r['cctv_score']}<br>"
                f"<b>Pop score:</b> {r['pop_score']}"
            )
            folium.GeoJson(
                r.geometry,
                style_function=lambda f: {"color": "limegreen", "weight": 4, "opacity": 0.7},
                tooltip=popup
            ).add_to(m)
        show_map(m)