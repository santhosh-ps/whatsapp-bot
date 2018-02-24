import json
from os.path import expanduser
class Bevco(object):
    dir = str(expanduser("~"))+"/bevco.json"
    bottles = []
    searchIndex = {}
    def __init__(self):
        with open(self.dir) as jsonfh:
            self.bottles = json.load(jsonfh)


    def getBottlesByName(self,name):
        searchBottles = []
        indexB = self.searchIndex.get(name)
        if indexB is not None:
            return indexB
        for bottle in self.bottles:
            brand = bottle.get('brand')
            # print(brand)
            if name in brand:
                searchBottles.append(bottle)
        self.searchIndex[name] = searchBottles
        return searchBottles



    #  print(jstr)
