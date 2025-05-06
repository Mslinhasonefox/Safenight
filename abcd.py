# streamlit_app.py
import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# 1) 页面配置
st.set_page_config(page_title="Safenight", layout="wide")

# 2) 全局 CSS
st.markdown("""
<style>
  /* 整体背景 */
  body { background-color: #1e1f22; }

  /* 标题 */
  .title {
    font-family: sans-serif;
    font-size: 56px;
    color: #fafafa;
    text-align: center;
    margin: 20px 0 40px;
  }

  /* 按钮样式 */
  .stButton > button {
    height: 150px;
    border-radius: 12px;
    border: none;
    font-size: 20px;
    font-weight: 500;
    color: #fff;
    margin-bottom: 1rem;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.5);
    transition: all 0.2s ease;
  }
  .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 4px 4px 10px rgba(0,0,0,0.7);
  }

  /* 各按钮的背景色 */
  #btn-pop { background-color: #2e7d32; }    /* 深绿 */
  #btn-lamp{ background-color: #6a1b9a; }    /* 紫罗兰 */
  #btn-cctv{ background-color: #1565c0; }    /* 深蓝 */
  #btn-score{background-color: #c62828; }    /* 暗红 */
</style>
""", unsafe_allow_html=True)

# 3) 主标题
st.markdown('<div class="title">Safenight</div>', unsafe_allow_html=True)

# 4) 地图公共参数
CENTER = [22.284, 114.137]
TILES  = "CartoDB dark_matter"

# 5) 各功能地图函数
def population_map():
    roads = gpd.read_file(
      "zip://safenight/HKU_ROUTE_MEAN_PopDen.zip!"
      "HKU_ROUTE_MEAN_PopDen/HKU_ROUTE_MEAN_PopDen.shp"
    )
    m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
    for _, r in roads.iterrows():
        folium.GeoJson(
          r.geometry,
          style_function=lambda f: {"color":"#ffa726","weight":3},
          tooltip=f"Population density: {r['MEAN']}"
        ).add_to(m)
    return m

def lamp_map():
    lamps = gpd.read_file(
      "zip://safenight/Lamppost_HKU.zip!"
      "Lamppost_HKU/Lamppost_HKU.shp"
    )
    m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
    cluster = MarkerCluster().add_to(m)
    for _, r in lamps.iterrows():
        folium.Marker(
          [r.geometry.y, r.geometry.x],
          popup=f"Lamp type: {r['Lamp_Type']}<br>Score: {r['Safety_Score']}",
          icon=folium.Icon(color="lightgray", icon="lightbulb", prefix="fa")
        ).add_to(cluster)
    return m

def cctv_map():
    cams = gpd.read_file(
      "zip://safenight/cctv.zip!"
      "CCTV_all_fc/CCTV_all_fc.shp"
    )
    m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
    for _, r in cams.iterrows():
        folium.CircleMarker(
          [r.geometry.y, r.geometry.x],
          radius=4, color="#00e5ff", fill=True, fill_opacity=0.8
        ).add_to(m)
    return m

def score_map():
    scored = gpd.read_file("safenight/roads_scored_new.geojson")
    m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
    for _, r in scored.iterrows():
        popup = (f"<b>Total:</b> {r['total_safety_score']}<br>"
                 f"<b>Lamp:</b> {r['lamp_score']}<br>"
                 f"<b>CCTV:</b> {r['cctv_score']}<br>"
                 f"<b>Pop:</b> {r['pop_score']}")
        folium.GeoJson(
          r.geometry,
          style_function=lambda f: {"color":"#66bb6a","weight":4,"opacity":0.7},
          tooltip=popup
        ).add_to(m)
    return m

# 6) 四宫格按钮
cols = st.columns(2, gap="large")
if cols[0].button("Population-density roads", key="pop",   help="Show pop-density map"):    st_folium(population_map(), height=650, width=0)
if cols[1].button("Lamp posts",                key="lamp",  help="Show lamp-posts map"):      st_folium(lamp_map(),       height=650, width=0)
if cols[0].button("CCTV layer",                key="cctv",  help="Show CCTV layer"):        st_folium(cctv_map(),        height=650, width=0)
if cols[1].button("Safety score map",          key="score", help="Show safety-score map"):  st_folium(score_map(),      height=650, width=0)

# 7) 初始提示
if not (st.session_state.get("pop") or st.session_state.get("lamp")
        or st.session_state.get("cctv") or st.session_state.get("score")):
    st.info("Click one of the four cards above to display its interactive map.")