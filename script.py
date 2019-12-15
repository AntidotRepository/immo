from bs4 import BeautifulSoup
import json
import os
import re
import ssl
import urllib.request

from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor


class Immo24_Parser():
    def __init__(self):
        self.number_of_pages = 0
        self.my_json = None

        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context

        # page = urllib.request.urlopen('https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-kaufen?enteredFrom=one_step_search')
        page = urllib.request.urlopen('https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-kaufen?pagenumber=1')
        # os.chdir("/Users/ducept/Documents/Programmation/immobilier/")
        print("Parsing 1st page")
        self.my_json = self.get_json(page)
        print("Get number of pages")
        self.number_of_pages = self.get_number_of_pages()

        for i in range(self.number_of_pages):
            page = urllib.request.urlopen('https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-kaufen?pagenumber={}'.format(i))
            self.my_json = self.get_json(page)
            self.get_offers()

    def get_offers(self):
        elements = self.my_json['searchResponseModel']['resultlist.resultlist']['resultlistEntries']
        for elem in elements:
            offers = elem['resultlistEntry']
            for offer in offers:
                print("{}\n".format(offer['resultlist.realEstate']['address']))

    def get_number_of_pages(self):
        numberOfPages = self.my_json['searchResponseModel']['resultlist.resultlist']['paging']['numberOfPages']
        print(numberOfPages)
        return numberOfPages

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


Immo24_Parser()
