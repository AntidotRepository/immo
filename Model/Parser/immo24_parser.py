from bs4 import BeautifulSoup
import json
import re

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
        # self.my_db = DB()

        # if fake is True:
        #     # Used for tests only!
        #     os.chdir("/Users/ducept/Documents/Programmation/immobilier/")
        #     # Store the HTML file as a string
        #     page = open('toParse.html', 'r')
        #     self.my_json = self.get_json(page)
        #     self.get_offers()
        # else:
        #     # Normal use!
        #     if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        #             getattr(ssl, '_create_unverified_context', None)):
        #         ssl._create_default_https_context = \
        #             ssl._create_unverified_context

        #     page = urllib.request.urlopen('https://www.immobilienscout24.de/\
        #         Suche/de/berlin/berlin/wohnung-kaufen?pagenumber=1')
        #     print("Parsing 1st page")
        #     self.my_json = self.get_json(page)
        #     print("Get number of pages")
        #     self.number_of_pages = self.get_number_of_pages()

        #     for i in range(self.number_of_pages):
        #         print("page {}/{}".format(i, self.number_of_pages))
        #         page = urllib.request.urlopen('https://www.immobilienscout24.\
        #             de/Suche/de/berlin/berlin/wohnung-kaufen?pagenumber={}'.
        #                                       format(i))
        #         self.my_json = self.get_json(page)
        #         self.get_offers()

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    def get_offers(self, page):
        self.my_json = self.get_json(page)
        offers_list = list()
        elements = self.my_json['searchResponseModel']\
            ['resultlist.resultlist']['resultlistEntries']
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

Immo24_Parser(fake=True)
