import cartopy
import geoip2
from scapy.all import *

conf.geoip_city = "/home/kadrex/Application/GeoLite/GeoLite2-Country_20230310/GeoLite2-Country.mmdb"
traceroute_map(["www.google.com", "www.secdev.org"])
