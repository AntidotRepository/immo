from bs4 import BeautifulSoup
import json
import os
import re
import ssl
import time
import urllib.request
from db import DB

from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor


class Immo24_Parser():
    def __init__(self, fake=False):
        """
        Initialize Immo24_Parser.

        Fetch every web pages matching:
        https://www.immobilienscout24.de/Suche/de/berlin/berlin/
        wohnung-kaufen?pagenumber=1
        and get the offers from these pages.

        Param:
        @type fake: Boolean (default: False)
        @param fake: False: Use immoScout24 to fill the database
                            (normal usecase)
                     True: Use toParse.html to fill the database
                           (for tests purpose)
        """
        self.number_of_pages = 0
        self.my_json = None
        self.my_db = DB()

        if fake is True:
            # Used for tests only!
            os.chdir("/Users/ducept/Documents/Programmation/immobilier/")
            # Store the HTML file as a string
            page = open('toParse.html', 'r')
            self.my_json = self.get_json(page)
            self.get_offers()
        else:
            # Normal use!
            if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                    getattr(ssl, '_create_unverified_context', None)):
                ssl._create_default_https_context = \
                    ssl._create_unverified_context

            page = urllib.request.urlopen('https://www.immobilienscout24.de/\
                Suche/de/berlin/berlin/wohnung-kaufen?pagenumber=1')
            print("Parsing 1st page")
            self.my_json = self.get_json(page)
            print("Get number of pages")
            self.number_of_pages = self.get_number_of_pages()

            for i in range(self.number_of_pages):
                print("page {}/{}".format(i, self.number_of_pages))
                page = urllib.request.urlopen('https://www.immobilienscout24.\
                    de/Suche/de/berlin/berlin/wohnung-kaufen?pagenumber={}'.
                                              format(i))
                self.my_json = self.get_json(page)
                self.get_offers()

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    def get_offers(self):
        elements = self.my_json['searchResponseModel']\
            ['resultlist.resultlist']['resultlistEntries']
        for elem in elements:
            offers = elem['resultlistEntry']
            for offer in offers:
                print("Creation date: {}".format(offer['@creation']))
                #offer = offer
                if '@id' not in offer['resultlist.realEstate'].keys():
                    assert False, "Missing id!"
                if '@creation' not in offer.keys():
                    assert False, "No creation date!"
                if '@modification' not in offer.keys():
                    assert False, "No modification date!"
                if 'title' not in offer['resultlist.realEstate'].keys():
                    assert False, "Missing title!"
                if 'privateOffer' not in offer['resultlist.realEstate'].keys():
                    offer['resultlist.realEstate']['privateOffer'] = False
                if 'price' not in offer['resultlist.realEstate'].keys():
                    assert False, "Missing price!"
                if 'value' not in offer['resultlist.realEstate']['price'].keys():
                    assert False, "Missing value!"
                if 'livingSpace' not in offer['resultlist.realEstate'].keys():
                    assert False, "Missing living space!"
                if 'numberOfRooms' not in offer['resultlist.realEstate'].keys():
                    assert False, "Missing number of rooms!"
                if 'energyPerfCert' not in offer['resultlist.realEstate'].keys():
                    offer['resultlist.realEstate']['energyPerfCert'] = False
                if 'energyEfficiency' not in offer['resultlist.realEstate'].keys():
                    offer['resultlist.realEstate']['energyEfficiency'] = 'NULL'
                if 'builtInKitchen' not in offer['resultlist.realEstate'].keys():
                    offer['builtInKitchen'] = 'NULL'
                if 'balcony' not in offer['resultlist.realEstate'].keys():
                    offer['resultlist.realEstate']['balcony'] = 'NULL'
                if 'garden' not in offer['resultlist.realEstate'].keys():
                    offer['resultlist.realEstate']['garden'] = 'NULL'
                if 'lift' not in offer['resultlist.realEstate'].keys():
                    offer['resultlist.realEstate']['lift'] = 'NULL'
                if 'guestToilet' not in offer['resultlist.realEstate'].keys():
                    offer['resultlist.realEstate']['guestToilet'] = 'NULL'
                if 'cellar' not in offer['resultlist.realEstate'].keys():
                    offer['resultlist.realEstate']['cellar'] = 'NULL'
                if 'isBarrierFree' not in offer['resultlist.realEstate'].keys():
                    offer['resultlist.realEstate']['isBarrierFree'] = 'NULL'
                if 'address' not in offer['resultlist.realEstate'].keys():
                    assert False, "Missing address"
                if 'street' not in offer['resultlist.realEstate']['address'].keys():
                    offer['resultlist.realEstate']['address']['street'] = 'None'
                if 'houseNumber' not in offer['resultlist.realEstate']['address'].keys():
                    offer['resultlist.realEstate']['address']['houseNumber'] = 'None'
                if 'latitude' not in offer['resultlist.realEstate']['address'].keys():
                    offer['resultlist.realEstate']['address']['latitude'] = 'None'
                if 'longitude' not in offer['resultlist.realEstate']['address'].keys():
                    offer['resultlist.realEstate']['address']['longitude'] = 'None'
                if 'preciseHouseNumber' not in offer['resultlist.realEstate']['address'].keys():
                    if offer['resultlist.realEstate']['address']['street'] != 'None':
                        offer['resultlist.realEstate']['address']['preciseHouseNumber'] = True
                    else:
                        offer['resultlist.realEstate']['address']['preciseHouseNumber'] = False
                if 'postcode' not in offer['resultlist.realEstate']['address'].keys():
                    assert False, "No postcode!"
                if 'city' not in offer['resultlist.realEstate']['address'].keys():
                    assert False, "No city!"
                if 'quarter' not in offer['resultlist.realEstate']['address'].keys():
                    assert False, "No quarter!"

                self.my_db.insert_offer(offer)

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    def get_number_of_pages(self):
        numberOfPages = self.my_json['searchResponseModel']\
            ['resultlist.resultlist']['paging']['numberOfPages']
        print(numberOfPages)
        return numberOfPages

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    def get_json(self, page):
        # Store the HTML file as a string
        html = page.read()
        # print html

        # Get the javascript from the HTML string
        bs = BeautifulSoup(html, features="html.parser")
        js = bs.find('script', text=re.compile('resultListModel: '))
        # print js.contents[0]

        # Get a json string from js string
        parser = Parser()
        tree = parser.parse(js.contents[0])
        # print tree
        fields = next(node.right for node in nodevisitor.visit(tree)
                      if (isinstance(node, ast.Assign) and
                          node.left.to_ecma() == 'resultListModel'))

        return json.loads(fields.to_ecma())

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------

Immo24_Parser(fake=True)
