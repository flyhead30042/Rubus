# https://nominatim.openstreetmap.org/search?q=%E9%99%BD%E6%98%8E%E5%B1%B1&format=geojson&county=
import requests
import logging
import geopandas as gpd
from geopandas import GeoDataFrame
from tabulate import tabulate


class WebAPI(object):
    def __init__(self):
        self.resp = None

    def postAPI(self, url, headers=None, postdata=None):

        r = requests.post(url=url, headers=headers, data=postdata)
        logging.debug("Request %s ==> response (%s)[%s]" % (r.url, r.status_code, r.text))
        r.raise_for_status()
        self.resp = r

    def getAPI(self, url,  headers=None, params=None):
        r = requests.get(url=url, headers=headers, params=params)
        r.raise_for_status()
        self.resp = r

def nominatim(q:str) -> GeoDataFrame:
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q":q, "format":"geojson", "countrycodes":"TW", "type":"peak"}
    api = WebAPI()
    api.getAPI(url = url, headers=None, params=params)
    data = api.resp.text
    gdf = gpd.read_file(data, driver='GeoJSON')

    return gdf

if __name__ == "__main__":
    gdf = nominatim("多加屯")
    print(tabulate(gdf, headers='keys', tablefmt='psql'))



