import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl
import geopy
import folium
from flask import Flask, render_template, request


def get_account_api(acct):
    """
    str -> str
    Function takes twitter acoount and returns json file with information
    about this account.
    """
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = twurl.augment(TWITTER_URL, {'screen_name': acct, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    return js


def find_friends_locations(dictn):
    """
    dict -> list
    Function takes API's dictionary and returns list of friends and
    their locations.
    """
    answer = []
    for user in dictn['users']:
        if user['location'] != '':
            answer.append((user['screen_name'], user['location']))
    return answer


def locations_to_coords(locations):
    """
    list -> list
    Function takes list of locations and returns list of coordinates.
    """
    coords_final = []
    geoloc = geopy.geocoders.Nominatim(user_agent="specify_your_app_name_here")
    coords_range = 9 if len(locations) >= 10 else len(locations)

    for point in range(coords_range):
        coordinates = geoloc.geocode(locations[point][1])
        if coordinates is not None:
            coords_final.append([locations[point][0], [coordinates.latitude,
                                coordinates.longitude]])
    lst_names = [el[0] for el in coords_final]
    lst_loc = [el[1] for el in coords_final]

    for var in range(0, len(lst_loc)):
        if lst_loc.count(lst_loc[var]) != 1:
            temp = lst_loc.pop(var)
            temp[0] = temp[0] + 0.3
            lst_loc.append(temp)

    return [el for el in zip(lst_names, lst_loc)]


def map_generator(coords):
    """
    (list) -> None
    Function takes lattitude and longitude of the user and returns map
    with the nearest location of films making.
    """
    m = folium.Map(location=[coords[0][1][0], coords[0][1][1]], zoom_start=7)

    tooltip = 'Click me'
    layer_2 = folium.FeatureGroup(name='Main')
    for point in coords:
        folium.Marker([point[1][0], point[1][1]], popup=point[0],
                      tooltip=tooltip, icon=folium.Icon()).add_to(layer_2)

    layer_3 = folium.FeatureGroup(name="Population")
    layer_3.add_child(folium.GeoJson(data=open('world.json', 'r',
        encoding='utf-8-sig').read(),
        style_function=lambda x: {'fillColor': 'green'
        if x['properties']['POP2005'] < 10000000 else 'orange'
            if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

    m.add_child(layer_2)
    m.add_child(layer_3)
    m.add_child(folium.LayerControl())
    return m


app = Flask(__name__)


@app.route("/", methods=['GET', "POST"])
def account():
    if request.method == 'POST':
        acc_ips = get_account_api(list(request.form.items())[0][1])
        friend_loc = find_friends_locations(acc_ips)
        return map_generator(locations_to_coords(friend_loc))._repr_html_()
    return render_template('account.html', res=6)

if __name__ == "__main__":
    app.run(debug=True)