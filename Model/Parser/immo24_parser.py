from bs4 import BeautifulSoup
import json
import re

from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor


class Immo24_Parser():
    def __init__(self):
        """
        Initialize Immo24_Parser.
        """
        self.number_of_pages = 0
        self.my_json = None
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    def get_offers(self, page):
        # First, get the json content of the page.
        self.my_json = self.get_json(page)
        offers_list = list()

        # From that json, extract the offers
        elements = self.my_json['searchResponseModel']\
            ['resultlist.resultlist']['resultlistEntries']

        # Check that every offer has all information.
        # If not, complete it with default values or assert
        # if the value are really important.
        for elem in elements:
            offers = elem['resultlistEntry']
            for offer in offers:
                realEstate = offer['resultlist.realEstate']
                if '@id' not in realEstate.keys():
                    assert False, "Missing id!"
                if '@creation' not in offer.keys():
                    assert False, "No creation date!"
                if '@modification' not in offer.keys():
                    assert False, "No modification date!"
                if 'title' not in realEstate.keys():
                    assert False, "Missing title!"
                if 'privateOffer' not in realEstate.keys():
                    realEstate['privateOffer'] = False
                if 'price' not in realEstate.keys():
                    assert False, "Missing price!"
                if 'value' not in realEstate['price'].keys():
                    assert False, "Missing value!"
                if 'livingSpace' not in realEstate.keys():
                    assert False, "Missing living space!"
                if 'numberOfRooms' not in realEstate.keys():
                    assert False, "Missing number of rooms!"
                if 'energyPerfCert' not in realEstate.keys():
                    realEstate['energyPerfCert'] = False
                if 'energyEfficiency' not in realEstate.keys():
                    realEstate['energyEfficiency'] = 'NULL'
                if 'builtInKitchen' not in realEstate.keys():
                    offer['builtInKitchen'] = 'NULL'
                if 'balcony' not in realEstate.keys():
                    realEstate['balcony'] = 'NULL'
                if 'garden' not in realEstate.keys():
                    realEstate['garden'] = 'NULL'
                if 'lift' not in realEstate.keys():
                    realEstate['lift'] = 'NULL'
                if 'guestToilet' not in realEstate.keys():
                    realEstate['guestToilet'] = 'NULL'
                if 'cellar' not in realEstate.keys():
                    realEstate['cellar'] = 'NULL'
                if 'isBarrierFree' not in realEstate.keys():
                    realEstate['isBarrierFree'] = 'NULL'
                if 'address' not in realEstate.keys():
                    assert False, "Missing address"
                if 'street' not in realEstate['address'].keys():
                    realEstate['address']['street'] = 'None'
                if 'houseNumber' not in realEstate['address'].keys():
                    realEstate['address']['houseNumber'] = 'None'
                if 'latitude' not in realEstate['address'].keys():
                    realEstate['address']['latitude'] = 'None'
                if 'longitude' not in realEstate['address'].keys():
                    realEstate['address']['longitude'] = 'None'
                if 'preciseHouseNumber' not in realEstate['address'].keys():
                    if realEstate['address']['street'] != 'None':
                        realEstate['address']['preciseHouseNumber'] = True
                    else:
                        realEstate['address']['preciseHouseNumber'] = False
                if 'postcode' not in realEstate['address'].keys():
                    assert False, "No postcode!"
                if 'city' not in realEstate['address'].keys():
                    assert False, "No city!"
                if 'quarter' not in realEstate['address'].keys():
                    assert False, "No quarter!"

                # Calculate price per square meter.
                realEstate['sq_meter_price'] = realEstate['price']['value'] / realEstate['livingSpace']

                offers_list.append(offer)

        return offers_list

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    def get_number_of_pages(self, page):
        self.my_json = self.get_json(page)
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
