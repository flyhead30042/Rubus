import os
import folium
import folium.plugins as plugins
import streamlit as st
from streamlit_folium import st_folium, folium_static
from typing.io import IO
import rubus
from rubus import search_place, Geogpx, TRACKLOGS_DIR
from typing import List, AnyStr, Hashable, Any
import plotly.express as px
import geopandas as gpd

st.set_page_config(page_title="GPX", page_icon="📈", layout="wide", initial_sidebar_state="expanded")
# st.markdown("# GPX")
# st.sidebar.header("GPX")
st.write(
    """
    Load GPX files and show on the selected based map 
    """
)

m:folium.Map = folium.Map(location=[25.13891, 121.58833], zoom_start=16, tiles=None)


# GPX file
def mark_wpt(wpt):
    folium.Marker(location=[wpt.latitude, wpt.longitude],
                  tooltip=f"<b>{wpt.display_name} {wpt.description} </b>",
                  popup=f"<b>{wpt.display_name} {wpt.description} </b><br>" +
                        f"<li>座標:{wpt.longitude, wpt.latitude}</li>" +
                        f"<li>高度:{wpt.elevation}</li>" +
                        f"<li>時間:{wpt.time}</li>",
                  icon=folium.Icon(icon='info-sign', color='blue')).add_to(m)

def add_tilelayer(tiles: list[dict[AnyStr, Any]]):
    for tls in tiles:
        if tls["enabled"]:
            folium.raster_layers.TileLayer(
                tiles=tls["tiles"],
                name=tls["name"],
                max_zoom=tls["max_zoom"],
                subdomains=tls["subdomains"],
                overlay=tls["overlay"],
                control=tls["control"],
                attr=tls["attr"],
            ).add_to(m)

def add_gpxlayer(upload_file: AnyStr | IO[str]):
    geogpx = rubus.load_gpx(upload_file)

    trkpt_loc: List = geogpx.trkpt_location()
    m.location = (trkpt_loc[0])
    folium.vector_layers.PolyLine(locations=trkpt_loc, color="red", weight=2.5, opacity=1).add_to(m)
    geogpx.wpt.apply(mark_wpt, axis="columns")
    return geogpx


def add_vectorlayers(vectors: list[dict[AnyStr, Any]]):
    for vls in vectors:
        if vls["enabled"]:
            source = os.path.join(rubus.CONFIGURATIONS_DIR,vls["source"])
            layer = gpd.read_file(source, encoding='utf-8')
            folium.GeoJson(
                data=layer["geometry"],
                name=vls["name"]
            ).add_to(m)

def main():
    geogpx: Geogpx = None
    #############
    #  Sidebar  #
    #############
    with st.sidebar:
        # upload gpx
        upload_file = st.file_uploader('Upload a file containing gpx data')
        if upload_file:
            dest = os.path.join(TRACKLOGS_DIR, upload_file.name)
            with open(dest, "w", encoding="utf-8") as stream:
                string_data = upload_file.getvalue().decode("utf-8")
                stream.write(string_data)

        # Load gpx
        l = os.listdir(TRACKLOGS_DIR)
        l.insert(0, "----")
        idx = l.index(upload_file.name) if upload_file else 0

        track_name = st.sidebar.radio("Track List", options=l, index=idx)
        if track_name and not track_name.startswith("----"):
            upload_file = os.path.join(TRACKLOGS_DIR, track_name)
            geogpx = add_gpxlayer(upload_file)

    ###############
    #  Main win   #
    ###############
    with st.container():
        r = rubus.load_config(os.path.join(rubus.CONFIGURATIONS_DIR, "resource.yaml"))
        # add title layers
        add_tilelayer(r["TileLayers"])
        add_vectorlayers(r["VectorLayers"])

        # add controller
        folium.LayerControl().add_to(m)
        folium.LatLngPopup().add_to(m)
        plugins.Fullscreen(position='topleft',
                           title='Expand me',
                           title_cancel='Exit me',
                           force_separate_button=True
                           ).add_to(m)
        plugins.MeasureControl(position='topleft', ).add_to(m)

        # show folium map on Streamlit
        # st_data = folium_static(m, width=1050, height=500)
        st_data = st_folium(m, width=1050, height=500)
        # st.write(st_data)

        if geogpx:
            c1, c2= st.columns(2, gap="small")
            options = ("elevation","elevation_diff", "distance","distance_diff", "time")
            optiony = c1.selectbox("-- Y Axis --",
                                  options= options,
                                  index = 0)
            optionx = c2.selectbox("-- X Axix --",
                                  options= options,
                                  index = 1)
            fig1 = px.scatter(geogpx.trkpt, x= optionx, y=optiony, color="elevation")
            st.plotly_chart(fig1, use_container_width=True)
            # fig2 = px.scatter_matrix(geogpx.trkpt, dimensions=["elevation_diff", "distance_diff", "time"])
            # st.plotly_chart(fig2, use_container_width=True)

            col1, col2, col3 = st.columns(3, gap="large")
            col1.metric("總上升", "{:.0f}m".format(geogpx.sum_elevation()[0]))
            col2.metric("總下降", "{:.0f}m".format(geogpx.sum_elevation()[1]))
            col3.metric("距離", "{:.2f}km".format(geogpx.sum_distance() / 1000))

            with st.expander("Way points"):
                st.dataframe(geogpx.wpt[["display_name", "description", "latitude", "longitude", "elevation","time"]],
                         use_container_width=True)

            with st.expander("Track points"):
                st.dataframe(geogpx.trkpt[["latitude", "longitude", "elevation","elevation_diff","distance","distance_diff","time"]],
                         use_container_width=True)



main()
