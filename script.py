from bs4 import BeautifulSoup
import json
import os
import re
import ssl
import urllib.request

from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor


def get_offers(my_json):
    elements = my_json['searchResponseModel']['resultlist.resultlist']['resultlistEntries']
    for elem in elements:
        offers = elem['resultlistEntry']
        for offer in offers:
            print("{}\n".format(offer['resultlist.realEstate']['address']))


def get_number_of_pages(my_json):
    numberOfPages = my_json['searchResponseModel']['resultlist.resultlist']['paging']['numberOfPages']
    print(numberOfPages)
    return numberOfPages


def parse_page(page):
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

    my_json = json.loads(fields.to_ecma())
    get_offers(my_json)
    get_number_of_pages(my_json)


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

page = urllib.request.urlopen('https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-kaufen?enteredFrom=one_step_search')
os.chdir("/Users/ducept/Documents/Programmation/immobilier/")
parse_page(page)

