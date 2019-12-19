from Model.DB.db import *
from Model.Parser.immo24_parser import Immo24_Parser

import os
import ssl
import urllib.request


class Controller:

    def __init__(self, fake=False):
        self.my_parser = Immo24_Parser()
        self.my_db = DB()
        if fake is True:
            # For test purpose only
            # Store the HTML file as a string
            page = open('toParse.html', 'r')
            offers = self.my_parser.get_offers(page)

            for offer in offers:
                self.my_db.insert_offer(offer)

        else:
            # Normal use!
            if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                    getattr(ssl, '_create_unverified_context', None)):
                ssl._create_default_https_context = \
                    ssl._create_unverified_context

            page = urllib.request.urlopen('https://www.immobilienscout24.de/' +
                                          'Suche/de/berlin/berlin/wohnung-' +
                                          'kaufen?pagenumber=1')
            print("Parsing 1st page")
            print("Get number of pages")
            self.number_of_pages = self.my_parser.get_number_of_pages(page)

            for i in range(self.number_of_pages):
                print("page {}/{}".format(i, self.number_of_pages))
                page = urllib.request.urlopen('https://www.immobilienscout24' +
                                              '.de/Suche/de/berlin/berlin/' +
                                              'wohnung-kaufen?pagenumber={}'.
                                              format(i))
                offers = self.my_parser.get_offers(page)

                for offer in offers:
                    self.my_db.insert_offer(offer)

