from bs4 import BeautifulSoup
import json
import os
import re

from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor


os.chdir("/Users/ducept/Documents/Programmation/immobilier/")

# Store the HTML file as a string
html = open('toParse.html', 'r').read()
# print html

# Get the javascript from the HTML string
bs = BeautifulSoup(html, features="lxml")
js = bs.find('script', text=re.compile('resultListModel: '))
# print js.contents[0]

# Get a json string from js string
parser = Parser()
tree = parser.parse(js.contents[0])
# print tree
fields = next(node.right for node in nodevisitor.visit(tree)
              if (isinstance(node, ast.Assign) and node.left.to_ecma() == 'resultListModel'))

elements = json.loads(fields.to_ecma())['searchResponseModel']['resultlist.resultlist']['resultlistEntries']

for elem in elements:
    offers = elem['resultlistEntry']
    for offer in offers:
        print("{}\n".format(offer['resultlist.realEstate']['address']))
