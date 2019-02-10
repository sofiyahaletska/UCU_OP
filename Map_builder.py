import folium
import pandas


year = int(input())

def file_reader(year):
    '''

    (int) -> generator
    Finds films with given year and return result of get_films_location()

    '''
    f = open("locations.csv", encoding='utf-8', errors='ignore')
    data = (line for line in f)
    for line in data:
        if line.split(',')[1] == str(year):
            yield get_films_location(line)

def get_films_location(line):
    '''

    (str) -> tuple(str,str)
    From the given line takes film name and film`s place, where it has been taken and return this info in tuple

    '''
    film_name = line.split(',')[0]
    film_place = line.split(',')[3]
    return (film_name,film_place)


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='MovieMapApp', timeout = None)

from geopy.extra.rate_limiter import RateLimiter

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

map = folium.Map(location=[48.314775, 25.082925],
zoom_start=5)
lst = list(file_reader(year))
fg_fm = folium.FeatureGroup(name="Film_Layer")
for movie in lst:
    film = movie[0]
    point = movie[1]
    while len(point) > 0:
        if geolocator.geocode(point):
            location = geolocator.geocode(point)
            break
        else:
            point = " ".join(point.split(" ")[1:])
    else:
        location = geolocator.geocode('Bermuda triangle')
    fg_fm.add_child(folium.Marker(location=[location.latitude, location.longitude],
                                    popup = film + " " + str(year) + " рік",
                                    icon=folium.Icon()))

fg_pp = folium.FeatureGroup(name="Population")
fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
    encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor':'green'
    if x['properties']['POP2005'] < 10000000
    else 'yellow' if 10000000 <= x['properties']['POP2005'] < 50000000
    else 'red'}))

def color_creator(population):
    if population < 2000:
        return "green"
    elif 2000 <= population <= 3500:
        return "yellow"
    else:
        return "red"
data = pandas.read_csv("Stan_1900.csv")
lat = data['lat']
lon = data['lon']
churches = data['церкви']
hc = data['гр-кат.']
map = folium.Map(location=[48.314775, 25.082925],
zoom_start=5)
fg_stan1 = folium.FeatureGroup(name="Stan_1900")
for lt, ln, ch, hc in zip(lat, lon, churches, hc):
    fg_stan1.add_child(folium.CircleMarker(location=[lt, ln],
    radius=10,
    popup="1900 рік"+"\n" + ch,
    fill_color=color_creator(hc),
    color='purple',
    fill_opacity=0.5))

data = pandas.read_csv("Stan_1914.csv")
lat = data['lat']
lon = data['lon']
churches = data['церкви']
hc = data['гр-кат.']
map = folium.Map(location=[48.314775, 25.082925],
zoom_start=5)
fg_stan2 = folium.FeatureGroup(name="Stan_1914")
for lt, ln, ch, hc in zip(lat, lon, churches, hc):
    fg_stan2.add_child(folium.CircleMarker(location=[lt, ln],
    radius=10,
    popup="1914 рік"+"\n" + ch,
    fill_color=color_creator(hc),
    color='white',
    fill_opacity=0.5))

data = pandas.read_csv("Stan_1938.csv")
lat = data['lat']
lon = data['lon']
churches = data['церкви']
hc = data['гр-кат.']
map = folium.Map(location=[48.314775, 25.082925],
zoom_start=5)
fg_stan3 = folium.FeatureGroup(name="Stan_1938")
for lt, ln, ch, hc in zip(lat, lon, churches, hc):
    fg_stan3.add_child(folium.CircleMarker(location=[lt, ln],
    radius=10,
    popup="1938 рік"+"\n" + ch,
    fill_color=color_creator(hc),
    color='black',
    fill_opacity=0.5))

map.add_child(fg_fm)
map.add_child(fg_pp)
map.add_child(fg_stan1)
map.add_child(fg_stan2)
map.add_child(fg_stan3)
map.add_child(folium.LayerControl())
map.save('5_Layered_Map.html')

