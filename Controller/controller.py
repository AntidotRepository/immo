# coding: utf-8

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

        self.my_db.set_all_offers_to_unavailable()

        if skip_parse is False:
            # Fill DB
            if fake is True:
                print("Fill DB...")
                # For test purpose only
                # Store the HTML file as a string
                page = open('toParse.html', 'r')
                dict_offers = self.my_parser.get_offers(page)

                for dict_offer in dict_offers:
                    dict_offer['stillAvailable'] = True
                    offer = Offer(dict_offer)
                    if offer.latitude != 'None' and offer.longitude != 'None':
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
                        if offer.latitude != 'None' and offer.longitude != 'None':
                            self.my_db.insert_offer(offer)
                    dict_offers.clear()

        # Get offers from DB
        print("Get offers from DB...")
        list_dict_offers = self.my_db.get_all_offers()

        for dict_offer in list_dict_offers:
            offer = Offer(dict_offer)
            self.offers.append(offer)

        print("Create grid...")
        grid_step_width = 0.04  # Step for latitudes
        grid_step_height = 0.02  # Step for longitudes
        min_latitude = self.my_db.get_min_latitude()
        max_latitude = self.my_db.get_max_latitude()
        min_longitude = self.my_db.get_min_longitude()
        max_longitude = self.my_db.get_max_longitude()

        # Creation of the grid
        areas_grid = list()
        for latitude in numpy.arange(min_latitude, max_latitude, grid_step_height):
            lines = list()
            areas_grid.append(lines)
            for longitude in numpy.arange(min_longitude, max_longitude, grid_step_width):
                area = Area(latitude, longitude, grid_step_height, grid_step_width)
                lines.append(area)

        # Populate the grid
        print("Populate grid...")
        for an_offer in self.offers:
            if an_offer.latitude != 'None':
                lat_case = int((an_offer.latitude - min_latitude) / grid_step_height)
                long_case = int((an_offer.longitude - min_longitude) / grid_step_width)
                areas_grid[lat_case][long_case].add_offer(an_offer)

        print("Calculate average prices in the grid...")
        # Calculation of the average price in the grid
        for line in areas_grid:
            for area in line:
                if len(area.offers) != 0:
                    area.calc_average()

        # # Map stuffs
        gelocator = Nominatim(user_agent="lol")
        location = gelocator.geocode(10115)

        gmap = gmplot.GoogleMapPlotter(location.latitude, location.longitude, 11)

        most_expensive = 0
        cheapest = 999999
        # Look for more expensive and cheapest area values
        print("Get extrem price values...")
        for line in areas_grid:
            for area in line:
                if area.average_price > most_expensive:
                    most_expensive = area.average_price
                if area.average_price != 0 and area.average_price < cheapest:
                    cheapest = area.average_price

        # Draw the grid
        print("Populate the grid...")
        for line in areas_grid:
            for area in line:
                if area.average_price != 0:
                    latitude_list = [area.posX, area.posX + area.width, area.posX + area.width, area.posX]
                    longitude_list = [area.posY, area.posY, area.posY + area.height, area.posY + area.height]
                    red = ((area.average_price - cheapest)/ (most_expensive - cheapest)) * 255
                    green = 255 - ((area.average_price - cheapest)/ (most_expensive - cheapest)) * 255
                    gmap.polygon(latitude_list, longitude_list, color='#{:02x}{:02x}00'.format(int(red), int(green)))

        # Change the color of the dot according to the price.
        for an_offer in self.offers:
            if an_offer.price < 170000 and an_offer.livingSpace > 10:
	            if an_offer.sq_meter_price < an_offer.area_average_price:
	                color = 'blue'
	            else:
	                color = 'red'
	            title = an_offer.title.replace('"', '\'').replace('\n', ' ').replace('\r', ' ') +' \\n'
	            title += "Price: {}€\\n".format(str(an_offer.price))
	            title += "Size: {}\\n".format(str(an_offer.livingSpace))
	            title += "Sq meter price: {:.2f}€/m2\\n".format(an_offer.sq_meter_price)
	            title += "dev from average: {:.2f}€/m2\\n".format(an_offer.sq_meter_price - an_offer.area_average_price)
	            title += "ID: {}\\n".format(str(an_offer.id))
	            gmap.marker(an_offer.latitude, an_offer.longitude, color, title=title)

        gmap.draw(os.getcwd() + "/maps.html")
