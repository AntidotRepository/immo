from geopy.geocoders import Nominatim
import os
import ssl
import sys


class Offer():
    def __init__(self, offer):
        self.id = offer['id']
        self.modification = offer['modification']
        self.creation = offer['creation']
        self.title = offer['title']
        self.privateOffer = offer['privateOffer']
        self.price = float(offer['price'])
        self.livingSpace = offer['livingSpace']
        self.sq_meter_price = self.calculate_sq_meter_price()
        self.numberOfRooms = offer['numberOfRooms']
        self.energyPerfCert = offer['energyPerfCert']
        self.energyEfficiency = offer['energyEfficiency']
        self.builtInKitchen = offer['builtInKitchen']
        self.balcony = offer['balcony']
        self.garden = offer['garden']
        self.lift = offer['lift']
        self.guestToilet = offer['guestToilet']
        self.cellar = offer['cellar']
        self.isBarrierFree = offer['isBarrierFree']
        self.stillAvailable = offer['stillAvailable']
        self.lastTimeView = offer['lastTimeView']

        self.street = offer['street']
        self.houseNumber = offer['houseNumber']
        self.preciseHouseNumber = offer['preciseHouseNumber']
        self.postcode = offer['postcode']
        self.city = offer['city']
        self.quarter = offer['quarter']
        if offer['latitude'] != 'None' and offer['longitude'] != 'None':
            self.latitude = offer['latitude']
            self.longitude = offer['longitude']
        self.filtered = offer['filtered']
        self.comments = offer['comments']

        self.area_average_price = 0

    def calculate_sq_meter_price(self):
        # Calculate price per square meter.
        # assert self.price != 0, "Appartment id: {}".format(self.id)
        # assert self.livingSpace != 0, "Appartment id: {}".format(self.id)
        if self.price != 0 and self.livingSpace != 0:
            return self.price / self.livingSpace
        else:
            return -1

    def calculate_coordinates(self):
        # Manage SSL certificate issue (not pretty clean)
        address = ""
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = \
                ssl._create_unverified_context
        gelocator = Nominatim(user_agent="my_locator")

        if self.street != 'None':
            address = address + " " + self.street
        if self.houseNumber != 'None':
            address = address + " " + str(self.houseNumber)
        if self.postcode != 'None':
            address = address + " " + str(self.postcode)
        if self.city != 'None':
            address = address + " " + self.city
        try:
            print("Get geocode")
            location = gelocator.geocode(address)
            if(type(location) != 'NoneType'):
                self.latitude = location.latitude
                self.longitude = location.longitude
                return True
            else:
                print("failed to get location for {}".format(self.id))
                return False
        except Exception:
            print(address)
            print("Calculate_coordinates failed: {}".format(sys.exc_info()))
            return False
