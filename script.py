from bs4 import BeautifulSoup
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
# fields = {getattr(node.left, 'value', ''): getattr(node.right, 'value', '')
#           for node in nodevisitor.visit(tree)
#           if isinstance(node, ast.Assign)}
fields = next(node.right for node in nodevisitor.visit(tree)
              if (isinstance(node, ast.Assign) and node.left.to_ecma() == 'resultListModel'))
# keylist = fields.keys()
# keylist.sort()
# for key in keylist:
#     print key

print(fields.to_ecma())

#look for queryModel

# print(type(fields['"resultlist.resultlist"']))

# print("fields keys: {}".format(fields.keys()))
# for child in fields["searchResponseModel"]:
#     if not isinstance(child, ast.VarStatement):
#         raise ValueError("All statements should be var statements")
#     print("child: {}".format(child))
