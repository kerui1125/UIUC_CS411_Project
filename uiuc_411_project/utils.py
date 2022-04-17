import certifi
import geopy
import ssl
from typing import Tuple


def get_college_geo_coordinates(name: str) -> Tuple[float, float]:
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    locator = geopy.geocoders.ArcGIS(user_agent="UIUC_CS411_kerui_juntao")
    location = locator.geocode(name, timeout=10)
    return location.latitude, location.longitude
