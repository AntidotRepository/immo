import time
import sqlite3


class DB():
    def __init__(self, **kwargs):
        # Create connection to database
        self.db = sqlite3.connect('SQL/immo.db')
        self.cursor = self.db.cursor()

    def insert_offer(self, offer):
        try:
            self.cursor.execute('''INSERT INTO offers (id,
                                                       modification,
                                                       creation,
                                                       title,
                                                       privateOffer,
                                                       price,
                                                       livingSpace,
                                                       numberOfRooms,
                                                       energyPerfCert,
                                                       energyEfficiency,
                                                       builtInKitchen,
                                                       balcony,
                                                       garden,
                                                       lift,
                                                       guestToilet,
                                                       cellar,
                                                       isBarrierFree,
                                                       stillAvailable,
                                                       lastTimeView)
                                   VALUES (:id,
                                           :modification,
                                           :creation,
                                           :title,
                                           :privateOffer,
                                           :price,
                                           :livingSpace,
                                           :numberOfRooms,
                                           :energyPerfCert,
                                           :energyEfficiency,
                                           :builtInKitchen,
                                           :balcony,
                                           :garden,
                                           :lift,
                                           :guestToilet,
                                           :cellar,
                                           :isBarrierFree,
                                           :stillAvailable,
                                           :lastTimeView);''',
                                {
                                    'id': offer['resultlist.realEstate']['@id'],
                                    'modification': offer['@modification'],
                                    'creation': offer['@creation'],
                                    'title': offer['resultlist.realEstate']['title'],
                                    'privateOffer': offer['resultlist.realEstate']['privateOffer'],
                                    'price': float(offer['resultlist.realEstate']['price']['value']),
                                    'livingSpace': offer['resultlist.realEstate']['livingSpace'],
                                    'numberOfRooms': offer['resultlist.realEstate']['numberOfRooms'],
                                    'energyPerfCert': offer['resultlist.realEstate']['energyPerfCert'],
                                    'energyEfficiency': offer['resultlist.realEstate']['energyEfficiency'],
                                    'builtInKitchen': offer['resultlist.realEstate']['builtInKitchen'],
                                    'balcony': offer['resultlist.realEstate']['balcony'],
                                    'garden': offer['resultlist.realEstate']['garden'],
                                    'lift': offer['resultlist.realEstate']['lift'],
                                    'guestToilet': offer['resultlist.realEstate']['guestToilet'],
                                    'cellar': offer['resultlist.realEstate']['cellar'],
                                    'isBarrierFree': offer['resultlist.realEstate']['isBarrierFree'],
                                    'stillAvailable': True,
                                    'lastTimeView': time.strftime
                                    ('%Y-%m-%d %H:%M:%S')
                                })
        except Exception:
            print(Exception)

        try:
            self.cursor.execute('''INSERT INTO addresses(appartment_id,
                                                         street,
                                                         houseNumber,
                                                         latitude,
                                                         longitude,
                                                         preciseHouseNumber,
                                                         postCode,
                                                         city,
                                                         quarter)
                                   VALUES (:appartment_id,
                                           :street,
                                           :houseNumber,
                                           :latitude,
                                           :longitude,
                                           :preciseHouseNumber,
                                           :postCode,
                                           :city,
                                           :quarter);''',
                                {
                                    'appartment_id': offer['resultlist.realEstate']['@id'],
                                    'street': offer['resultlist.realEstate']['address']['street'],
                                    'houseNumber': offer['resultlist.realEstate']['address']['houseNumber'],
                                    'latitude': offer['resultlist.realEstate']['address']['latitude'],
                                    'longitude': offer['resultlist.realEstate']['address']['longitude'],
                                    'preciseHouseNumber': offer['resultlist.realEstate']['address']['preciseHouseNumber'],
                                    'postCode': offer['resultlist.realEstate']['address']['postcode'],
                                    'city': offer['resultlist.realEstate']['address']['city'],
                                    'quarter': offer['resultlist.realEstate']['address']['quarter']
                                })
            self.db.commit()
        except Exception:
            print(Exception)

    def close(self):
        self.db.close()
