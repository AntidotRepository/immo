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
                                    'id': offer['@id'],
                                    'modification': offer['@modification'],
                                    'creation': offer['@creation'],
                                    'title': offer['title'],
                                    'privateOffer': offer['privateOffer'],
                                    'price': float(offer['price']['value']),
                                    'livingSpace': offer['livingSpace'],
                                    'numberOfRooms': offer['numberOfRooms'],
                                    'energyPerfCert': offer['energyPerfCert'],
                                    'energyEfficiency': offer['energyEfficiency'],
                                    'builtInKitchen': offer['builtInKitchen'],
                                    'balcony': offer['balcony'],
                                    'garden': offer['garden'],
                                    'lift': offer['lift'],
                                    'guestToilet': offer['guestToilet'],
                                    'cellar': offer['cellar'],
                                    'isBarrierFree': offer['isBarrierFree'],
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
                                    'appartment_id': offer['@id'],
                                    'street': offer['address']['street'],
                                    'houseNumber': offer['address']['houseNumber'],
                                    'latitude': offer['address']['latitude'],
                                    'longitude': offer['address']['longitude'],
                                    'preciseHouseNumber': offer['address']['preciseHouseNumber'],
                                    'postCode': offer['address']['postcode'],
                                    'city': offer['address']['city'],
                                    'quarter': offer['address']['quarter']
                                })
            self.db.commit()
        except Exception:
            print(Exception)

    def close(self):
        self.db.close()
