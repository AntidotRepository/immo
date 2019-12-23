from Model.DB.db import *
from Model.offer import *
from Model.area import *
from Model.Parser.immo24_parser import Immo24_Parser

import numpy
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

        grid_step = 0.05  # Step for latitudes and longitudes
        min_latitude = self.my_db.get_min_latitude()
        max_latitude = self.my_db.get_max_latitude()
        min_longitude = self.my_db.get_min_longitude()
        max_longitude = self.my_db.get_max_longitude()

        # Creation of the grid
        areas_grid = list()
        for latitude in numpy.arange(min_latitude, max_latitude, grid_step):
            lines = list()
            areas_grid.append(lines)
            for longitude in numpy.arange(min_longitude, max_longitude, grid_step):
                area = Area(latitude, longitude, grid_step, grid_step)
                lines.append(area)

        # Populate the grid
        for an_offer in self.offers:
            if an_offer.latitude != 'None':
                for line in areas_grid:
                    for area in line:
                        if (an_offer.latitude > area.posX) and (an_offer.latitude < (area.posX + area.width)) and (an_offer.longitude > area.posY) and (an_offer.longitude < (area.posY + area.height)):
                            area.add_offer(an_offer)

        # Calculation of the average price in the grid
        i = 0
        j = 0
        for line in areas_grid:
            i += 1
            j = 0
            for area in line:
                j += 1
                if len(area.offers) != 0:
                    area.calc_average()

        # Map stuffs
        latitudes = list()
        longitudes = list()

        for an_offer in self.offers:
            if an_offer.latitude != 'None':
                latitudes.append(an_offer.latitude)
                longitudes.append(an_offer.longitude)
        gelocator = Nominatim(user_agent="lol")
        location = gelocator.geocode(12059)

        gmap4 = gmplot.GoogleMapPlotter(location.latitude, location.longitude, 13)

        # Change the color of the dot according to the price.
        for an_offer in self.offers:
            if an_offer.sq_meter_price < an_offer.area_average_price:
                color = 'blue'
            else:
                color = 'red'
            gmap4.scatter([an_offer.latitude], [an_offer.longitude], color, size=40, marker=False)

        gmap4.draw(os.getcwd() + "/maps.html")
