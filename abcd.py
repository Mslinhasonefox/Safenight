import branca.colormap as cm  # 加图例用
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Population Map", layout="wide")
CENTER = [22.284, 114.137]

def population_map():
    roads = gpd.read_file("zip://safenight/HKU_ROUTE_MEAN_PopDen.zip!HKU_ROUTE_MEAN_PopDen/HKU_ROUTE_MEAN_PopDen.shp")
    
    # 检查数据字段
    if 'MEAN' not in roads.columns:
        st.error("字段 'MEAN' 不存在，无法可视化人口密度")
        return folium.Map(location=CENTER, zoom_start=15)

    # 构建线性颜色映射
    vmin, vmax = roads["MEAN"].min(), roads["MEAN"].max()
    colormap = cm.linear.YlOrRd_09.scale(vmin, vmax)
    colormap.caption = 'Population Density (MEAN)'

    m = folium.Map(location=CENTER, zoom_start=15, tiles="cartodb positron")

    for _, row in roads.iterrows():
        folium.GeoJson(
            row.geometry,
            style_function=lambda feature, value=row["MEAN"]: {
                "color": colormap(value),
                "weight": 4,
                "opacity": 0.8
            },
            tooltip=f"Population density: {row['MEAN']}"
        ).add_to(m)

    colormap.add_to(m)
    return m

# 渲染地图
st_folium(population_map(), height=750)
