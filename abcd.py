import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# 设置页面
st.set_page_config(page_title="Safenight - Population", layout="wide")

# 地图中心点与底图样式
CENTER = [22.284, 114.137]
TILES  = "cartodb dark_matter"

# 加载人口密度数据并绘制地图
def population_map():
    roads = gpd.read_file("zip://safenight/HKU_ROUTE_MEAN_PopDen.zip!HKU_ROUTE_MEAN_PopDen/HKU_ROUTE_MEAN_PopDen.shp")
    m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
    for _, r in roads.iterrows():
        folium.GeoJson(
            r.geometry,
            style_function=lambda f: {"color": "orange", "weight": 3},
            tooltip=f"Population density: {r['MEAN']}"
        ).add_to(m)
    return m

# 标题与地图显示
st.markdown(
    """
    <h1 style='text-align: center; color: white;'>Safenight - Population Density Map</h1>
    """, unsafe_allow_html=True
)

st_folium(population_map(), height=700)
