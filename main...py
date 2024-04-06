import streamlit as st
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from bokeh.plotting import figure, show
from bokeh.tile_providers import get_provider, Vendors

st.title("Phone Number Location Finder")

# Get phone number from user input
number = st.text_input("Enter phone number (with country code):")

if number:
    pepnumber = phonenumbers.parse(number)
    location = geocoder.description_for_number(pepnumber, "en")
    service_pro = phonenumbers.parse(number)
    provider = carrier.name_for_number(service_pro, "en")

    st.write("Location:", location)
    st.write("Service Provider:", provider)

    key = '3229ea51ebed4311924d0dc704876aca'
    geocoder = OpenCageGeocode(key)
    query = str(location)
    results = geocoder.geocode(query)

    if results:
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']

        st.write("Latitude:", lat)
        st.write("Longitude:", lng)

        # Create Bokeh plot
        p = figure(x_range=(lng - 1, lng + 1), y_range=(lat - 1, lat + 1),
                   x_axis_type="mercator", y_axis_type="mercator")
        tile_provider = get_provider(Vendors.CARTODBPOSITRON)
        p.add_tile(tile_provider)

        # Plot marker at the location
        p.circle(x=lng, y=lat, size=10, fill_color="blue", fill_alpha=0.6)

        # Display the plot
        st.bokeh_chart(p, use_container_width=True)
    else:
        st.error("No results found for the location.")