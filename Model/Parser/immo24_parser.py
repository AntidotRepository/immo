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
        ignore = False
        for elem in elements:
            offers = elem['resultlistEntry']
            for offer_json in offers:
                realEstate = offer_json['resultlist.realEstate']
                if '@id' not in realEstate.keys():
                    print("Missing id!")
                    ignore = True
                if '@creation' not in offer_json.keys():
                    print("No creation date!")
                    ignore = True
                if '@modification' not in offer_json.keys():
                    print("No modification date!")
                    ignore = True
                if 'title' not in realEstate.keys():
                    print("Missing title!")
                    ignore = True
                if 'privateOffer' not in realEstate.keys():
                    realEstate['privateOffer'] = False
                if 'price' not in realEstate.keys():
                    print("Missing price!")
                    ignore = True
                if 'value' not in realEstate['price'].keys():
                    print("Missing value!")
                    ignore = True
                if 'livingSpace' not in realEstate.keys():
                    print("Missing living space!")
                    ignore = True
                if realEstate['livingSpace'] == 0:
                    print("living space = 0")
                    ignore = True
                if 'numberOfRooms' not in realEstate.keys():
                    print("Missing number of rooms!")
                if 'energyPerfCert' not in realEstate.keys():
                    realEstate['energyPerfCert'] = False
                if 'energyEfficiency' not in realEstate.keys():
                    realEstate['energyEfficiency'] = 'NULL'
                if 'builtInKitchen' not in realEstate.keys():
                    offer_json['builtInKitchen'] = 'NULL'
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
                    print("Missing address")
                    ignore = True
                if 'street' not in realEstate['address'].keys():
                    realEstate['address']['street'] = 'None'
                if 'houseNumber' not in realEstate['address'].keys():
                    realEstate['address']['houseNumber'] = 'None'
                if 'wgs84Coordinate' not in realEstate['address']:
                    realEstate['address']['wgs84Coordinate'] = dict()
                if 'latitude' not in realEstate['address']['wgs84Coordinate'].keys():
                    realEstate['address']['wgs84Coordinate']['latitude'] = 'None'
                if 'longitude' not in realEstate['address']['wgs84Coordinate'].keys():
                    realEstate['address']['wgs84Coordinate']['longitude'] = 'None'
                if 'preciseHouseNumber' not in realEstate['address'].keys():
                    if realEstate['address']['street'] != 'None':
                        realEstate['address']['preciseHouseNumber'] = True
                    else:
                        realEstate['address']['preciseHouseNumber'] = False
                if 'postcode' not in realEstate['address'].keys():
                    print("No postcode!")
                    ignore = True
                if 'city' not in realEstate['address'].keys():
                    print("No city!")
                    ignore = True
                if 'quarter' not in realEstate['address'].keys():
                    print("No quarter!")
                    ignore = True

                if ignore is False:
                    offer = dict()
                    offer['id'] = realEstate['@id']
                    offer['creation'] = offer_json['@creation']
                    offer['modification'] = offer_json['@modification']
                    offer['title'] = realEstate['title']
                    offer['privateOffer'] = realEstate['privateOffer']
                    offer['price'] = realEstate['price']['value']
                    offer['livingSpace'] = realEstate['livingSpace']
                    offer['numberOfRooms'] = realEstate['numberOfRooms']
                    offer['energyPerfCert'] = realEstate['energyPerfCert']
                    offer['energyEfficiency'] = realEstate['energyEfficiency']
                    offer['builtInKitchen'] = realEstate['builtInKitchen']
                    offer['balcony'] = realEstate['balcony']
                    offer['garden'] = realEstate['garden']
                    offer['lift'] = realEstate['lift']
                    offer['guestToilet'] = realEstate['guestToilet']
                    offer['cellar'] = realEstate['cellar']
                    offer['isBarrierFree'] = realEstate['isBarrierFree']
                    offer['street'] = realEstate['address']['street']
                    offer['houseNumber'] = realEstate['address']['houseNumber']
                    offer['latitude'] = realEstate['address']['wgs84Coordinate']['latitude']
                    offer['longitude'] = realEstate['address']['wgs84Coordinate']['longitude']
                    offer['preciseHouseNumber'] = realEstate['address']['preciseHouseNumber']
                    offer['postcode'] = realEstate['address']['postcode']
                    offer['city'] = realEstate['address']['city']
                    offer['quarter'] = realEstate['address']['quarter']
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
