import time
import sqlite3


class DB():
    def __init__(self, **kwargs):
        # Create connection to database
        self.db = sqlite3.connect('SQL/immo.db')
        self.cursor = self.db.cursor()

    def insert_offer(self, offer):
        try:
            realEstate = offer['resultlist.realEstate']
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
                                    'id': realEstate['@id'],
                                    'modification': offer['@modification'],
                                    'creation': offer['@creation'],
                                    'title': realEstate['title'],
                                    'privateOffer': realEstate['privateOffer'],
                                    'price': float(realEstate['price']['value']),
                                    'livingSpace': realEstate['livingSpace'],
                                    'numberOfRooms': realEstate['numberOfRooms'],
                                    'energyPerfCert': realEstate['energyPerfCert'],
                                    'energyEfficiency': realEstate['energyEfficiency'],
                                    'builtInKitchen': realEstate['builtInKitchen'],
                                    'balcony': realEstate['balcony'],
                                    'garden': realEstate['garden'],
                                    'lift': realEstate['lift'],
                                    'guestToilet': realEstate['guestToilet'],
                                    'cellar': realEstate['cellar'],
                                    'isBarrierFree': realEstate['isBarrierFree'],
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
                                    'appartment_id': realEstate['@id'],
                                    'street': realEstate['address']['street'],
                                    'houseNumber': realEstate['address']['houseNumber'],
                                    'latitude': realEstate['address']['latitude'],
                                    'longitude': realEstate['address']['longitude'],
                                    'preciseHouseNumber': realEstate['address']['preciseHouseNumber'],
                                    'postCode': realEstate['address']['postcode'],
                                    'city': realEstate['address']['city'],
                                    'quarter': realEstate['address']['quarter']
                                })
            self.db.commit()
        except Exception:
            print(Exception)

    def close(self):
        self.db.close()
