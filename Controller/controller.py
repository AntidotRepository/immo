from Model.DB.db import *
from Model.offer import *
from Model.Parser.immo24_parser import Immo24_Parser

import os
import ssl
import time
import urllib.request

import gmplot
from geopy.geocoders import Nominatim


class Controller:

    def __init__(self, fake=False, skip_parse=False):
        self.my_parser = Immo24_Parser()
        self.my_db = DB()
        self.offers = list()

        # Manage SSL certificate issue (not pretty clean)
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = \
                ssl._create_unverified_context

        if skip_parse is False:
            # Fill DB
            if fake is True:
                # For test purpose only
                # Store the HTML file as a string
                page = open('toParse.html', 'r')
                dict_offers = self.my_parser.get_offers(page)

                for dict_offer in dict_offers:
                    dict_offer['stillAvailable'] = True
                    dict_offer['lastTimeView'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    offer = Offer(dict_offer)
                    self.my_db.insert_offer(offer)
                dict_offers.clear()

            else:
                # Normal use!
                # First, check how many page we have to retrieve.
                page = urllib.request.urlopen('https://www.immobilienscout24.de/' +
                                              'Suche/de/berlin/berlin/wohnung-' +
                                              'kaufen?pagenumber=1')
                print("Get number of pages")
                self.number_of_pages = self.my_parser.get_number_of_pages(page)

                # For each page, get the offers
                for i in range(1, self.number_of_pages):
                    print("page {}/{}".format(i, self.number_of_pages))
                    page = urllib.request.urlopen('https://www.immobilienscout24' +
                                                  '.de/Suche/de/berlin/berlin/' +
                                                  'wohnung-kaufen?pagenumber={}'.
                                                  format(i))
                    dict_offers = self.my_parser.get_offers(page)

                    # Store each offer in the DB
                    for dict_offer in dict_offers:
                        dict_offer['stillAvailable'] = True
                        dict_offer['lastTimeView'] = time.strftime('%Y-%m-%d %H:%M:%S')
                        offer = Offer(dict_offer)
                        self.my_db.insert_offer(offer)
                    dict_offers.clear()

        # Get offers from DB
        list_dict_offers = self.my_db.get_all_offers()

        for dict_offer in list_dict_offers:
            offer = Offer(dict_offer)
            self.offers.append(offer)

        # Map stuffs
        latitudes = list()
        longitudes = list()

        for an_offer in self.offers:
            print(type(an_offer.longitude))
            if an_offer.latitude != 'None':
                latitudes.append(an_offer.latitude)
                longitudes.append(an_offer.longitude)
        gelocator = Nominatim(user_agent="lol")
        location = gelocator.geocode(12059)
        gmap4 = gmplot.GoogleMapPlotter(location.latitude, location.longitude, 13)

        gmap4.heatmap(latitudes, longitudes)

        gmap4.draw(os.getcwd() + "/maps.html")
