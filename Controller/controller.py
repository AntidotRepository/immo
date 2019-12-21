from Model.DB.db import *
from Model.Parser.immo24_parser import Immo24_Parser

import os
import ssl
import urllib.request

import gmplot
import os
from geopy.geocoders import Nominatim

class Controller:

    def __init__(self, fake=False, show_only=False):
        self.my_parser = Immo24_Parser()
        self.my_db = DB()

        # Manage SSL certificate issue (not pretty clean)
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = \
                ssl._create_unverified_context

        if show_only is False:
            if fake is True:
                # For test purpose only
                # Store the HTML file as a string
                page = open('toParse.html', 'r')
                offers = self.my_parser.get_offers(page)

                for offer in offers:
                    self.my_db.insert_offer(offer)

            else:
                # Normal use!
                # First, check how many page we have to retrieve.
                page = urllib.request.urlopen('https://www.immobilienscout24.de/' +
                                              'Suche/de/berlin/berlin/wohnung-' +
                                              'kaufen?pagenumber=1')
                print("Get number of pages")
                self.number_of_pages = self.my_parser.get_number_of_pages(page)

                # For each page, get the offers
                for i in range(self.number_of_pages):
                    print("page {}/{}".format(i, self.number_of_pages))
                    page = urllib.request.urlopen('https://www.immobilienscout24' +
                                                  '.de/Suche/de/berlin/berlin/' +
                                                  'wohnung-kaufen?pagenumber={}'.
                                                  format(i))
                    offers = self.my_parser.get_offers(page)

                    # Store each offer in the DB
                    for offer in offers:
                        self.my_db.insert_offer(offer)

        # Map stuffs
        gelocator = Nominatim(user_agent="lol")
        location = gelocator.geocode(12059)
        gmap4 = gmplot.GoogleMapPlotter(location.latitude, location.longitude, 13)

        gmap4.heatmap([location.latitude], [location.longitude])

        gmap4.draw(os.getcwd() + "/maps.html")
