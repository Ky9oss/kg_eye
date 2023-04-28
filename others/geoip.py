import pygeoip
gi = pygeoip.GeoIP('../resources/GeoLiteCity.dat')

def printRecord(tgt):
    rec = gi.record_by_name(tgt)
    city = rec['city']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    print(str(city) +"  "+  str(country))
    print(str(lat)+"  "+str(long))

printRecord('101.200.44.45')
printRecord('64.233.161.99')
