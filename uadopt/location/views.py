from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo, get_center_coordinates, getZoom,get_client_ip
import folium


# Create your views here.


def calculate_distance_view(request):
    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='location')
    ip = '63.22.192.34'
    country, city, lat, long = get_geo(ip)
    location = geolocator.geocode(city)

    # location coordinates
    l_lat = lat
    l_long = long
    pointA = (l_lat, l_long)
    print(l_lat, l_long, "\n")

    # initial folium map
    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_long), zoom_start=1)

    # location Marker
    folium.Marker([l_lat, l_long], tooltip='Click here for more', popup=city['city'],
                  icon=folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)

        # destination coordinates
        d_lat = destination.latitude
        d_long = destination.longitude
        pointB = (d_lat, d_long)

        # distance calculated
        distance = round(geodesic(pointA, pointB).km, 2)

        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_long, d_lat, d_long),
                       zoom_start=getZoom(distance))

        # location Marker
        folium.Marker([l_lat, l_long], tooltip='Click here for more', popup=city['city'],
                      icon=folium.Icon(color='red')).add_to(m)

        # Destination Marker
        folium.Marker([d_lat, d_long], tooltip='Click here for more', popup=destination,
                      icon=folium.Icon(color='blue', icon='cloud')).add_to(m)

        # Draw line between locations
        line = folium.PolyLine(locations=[pointA, pointB], weight=2, color='green')
        m.add_child(line)

        instance.location = location
        instance.distance = distance
        instance.save()

    m = m._repr_html_()
    context = {
        'distance': obj,
        'form': form,
        'map': m
    }

    return render(request, 'main.html', context)
