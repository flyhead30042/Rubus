import geopandas
import gpxpy
from gpxpy.gpx import GPX
from geopandas import GeoDataFrame
import pandas as pd
from pandas import DataFrame
from typing import Iterator, Dict, TypeVar, Tuple, Hashable, Any, List, Union, AnyStr, IO
import rubus


class Geogpx():
    def __init__(self):
        self.gpx: GPX = None
        self.trkpt: GeoDataFrame = None
        self.wpt: GeoDataFrame = None

    def load(self, xml_or_fileobj_or_filename: Union[AnyStr, IO[str]]):
        if hasattr(xml_or_fileobj_or_filename, 'read'):
            # file object
            data = xml_or_fileobj_or_filename.read()
        elif hasattr(xml_or_fileobj_or_filename, 'getvalue'):
            # BaseIO
            data = xml_or_fileobj_or_filename.getvalue()
        elif xml_or_fileobj_or_filename.lower().endswith(".gpx"):
            # file path
            with open(xml_or_fileobj_or_filename, "r", encoding='UTF-8') as f:
                data = f.read()
        else:
            # xml
            data = xml_or_fileobj_or_filename

        if isinstance(data, bytes):
            data = data.decode("UTF-8")

        self.gpx = gpxpy.parse(data)
        self.parse_gpx()
        return self

    def __parse_trkpt(self):
        # track points
        data_trkpt: List = []
        for track in self.gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    data_trkpt.append([point.latitude, point.longitude, point.elevation, point.time])

        df_trkpt = DataFrame(data=data_trkpt, columns=["latitude", "longitude", "elevation", "time"])
        self.trkpt = GeoDataFrame(data=df_trkpt,
                                  geometry=geopandas.points_from_xy(df_trkpt.longitude, df_trkpt.latitude,
                                                                    df_trkpt.elevation, crs=4326))

    def __diff_distance(self):
        df1 = self.trkpt.to_crs(3826)
        df2 = df1.shift(periods=1)
        dis = df1.distance(df2)
        self.trkpt = pd.concat([self.trkpt, dis.rename('distance_diff')], axis=1)
        self.trkpt["distance"] = self.trkpt["distance_diff"].cumsum()

    def __diff_elevation(self):
        df2 = self.trkpt.shift(periods=1)
        h = self.trkpt["elevation"] - df2["elevation"]
        self.trkpt = pd.concat([self.trkpt, h.rename('elevation_diff')], axis=1)

    def __parse_wpt(self):
        # waypoints
        data_wpt: List = []
        for waypoint in self.gpx.waypoints:
            data_wpt.append([waypoint.name, waypoint.latitude, waypoint.longitude, waypoint.elevation, waypoint.time,
                             waypoint.description])

        df_wpt = DataFrame(data=data_wpt,
                           columns=["display_name", "latitude", "longitude", "elevation", "time", "description"])
        self.wpt = GeoDataFrame(data=df_wpt, geometry=geopandas.points_from_xy(df_wpt.longitude, df_wpt.latitude, df_wpt.elevation),
                                crs=4326)

    def parse_gpx(self, gpx: GPX = None):
        if gpx:
            self.gpx = gpx
        self.__parse_trkpt()
        self.__diff_distance()
        self.__diff_elevation()
        self.__parse_wpt()

        return self

    def trkpt_location(self) -> list[list[float, float]]:
        return [[a.y, a.x] for a in self.trkpt.geometry.to_numpy()]

    def wpt_location(self) -> list[list[float, float]]:
        return [[a.y, a.x] for a in self.wpt.geometry.to_numpy()]

    def sum_distance(self) -> float:
        return self.trkpt["distance_diff"].sum()

    def sum_elevation(self) -> tuple[float, float]:
        rise = round(self.trkpt.loc[self.trkpt["elevation_diff"] > 0]["elevation_diff"].sum())
        drop = round(abs(self.trkpt.loc[self.trkpt["elevation_diff"] < 0]["elevation_diff"].sum()))
        return (rise, drop)


if __name__ == "__main__":
    fname = "E:\\Users\\Flyhead\\citest\\Rubus\\backup\\那結山貴妃山O縱走.gpx"
    geogpx: Geogpx = rubus.load_gpx(fname)

    print(geogpx.trkpt_location()[:4])
    print(geogpx.wpt.iloc[0].longitude)
    rubus.display_df(geogpx.trkpt)
    rubus.display_df(geogpx.wpt)
    print(f"rise = {geogpx.sum_elevation()[0]}m, drop = {geogpx.sum_elevation()[1]}m")
    print(f"distance = {round(geogpx.sum_distance() / 1000, 2)}km")
    # geogpx.wpt.plot(column = 'elevation')
