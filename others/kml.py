import pygeoip
import sys
import textwrap


gi = pygeoip.GeoIP('../resources/GeoLiteCity.dat')

def get_kml_body(ip):
    rec = gi.record_by_name(ip)
    try:
        longitude = rec['longitude']
        latitude = rec['latitude']
        kml = (
                '<Placemark>\n'
                '<name>%s</name>\n'
                '<Point>\n'
                '<coordinates>%6f,%6f</coordinates>\n'
                '</Point>\n'
                '</Placemark>\n'
                ) % (ip, longitude, latitude)
        return kml

    except Exception as e:
        return None

def get_kml_doc(src, dst):
    kmlheader = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
            '<Document>\n')
    kmlbody_src = get_kml_body(src)
    kmlbody_dst = get_kml_body(dst)
    kmlfooter = '</Document>\n</kml>'
    if kmlbody_src and kmlbody_dst is not None:
        kmldoc = kmlheader + kmlbody_src + kmlbody_dst + kmlfooter
        with open("xxx.kml", 'w') as t:
            t.write(kmldoc)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python kml.py [src_ip] [dst_ip]')
        sys.exit()
    src = sys.argv[1]
    dst = sys.argv[2]
    get_kml_doc(src, dst)
