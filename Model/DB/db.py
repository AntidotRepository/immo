import time
import sqlite3
import sys


class DB():
    def __init__(self, **kwargs):
        # Create connection to database
        self.db = sqlite3.connect('Model/DB/immo.db')
        self.cursor = self.db.cursor()

    def insert_offer(self, offer):
        # try:
        print("Insert {}".format(offer.title))
        self.cursor.execute('''INSERT INTO offers (id,
                                                modification,
                                                creation,
                                                title,
                                                privateOffer,
                                                price,
                                                sq_meter_price,
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
                                    :sq_meter_price,
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
                             'id': offer.id,
                             'modification': offer.modification,
                             'creation': offer.creation,
                             'title': offer.title,
                             'privateOffer': offer.privateOffer,
                             'price': offer.price,
                             'sq_meter_price': float(offer.sq_meter_price),
                             'livingSpace': float(offer.livingSpace),
                             'numberOfRooms': offer.numberOfRooms,
                             'energyPerfCert': offer.energyPerfCert,
                             'energyEfficiency': offer.energyEfficiency,
                             'builtInKitchen': offer.builtInKitchen,
                             'balcony': offer.balcony,
                             'garden': offer.garden,
                             'lift': offer.lift,
                             'guestToilet': offer.guestToilet,
                             'cellar': offer.cellar,
                             'isBarrierFree': offer.isBarrierFree,
                             'stillAvailable': offer.stillAvailable,
                             'lastTimeView': offer.lastTimeView
                         })
        # except Exception:
        #     print("Insert offer exception: {}".format(sys.exc_info()[0]))

        # try:
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
                             'appartment_id': offer.id,
                             'street': offer.street,
                             'houseNumber': offer.houseNumber,
                             'latitude': offer.latitude,
                             'longitude': offer.longitude,
                             'preciseHouseNumber': offer.preciseHouseNumber,
                             'postCode': offer.postcode,
                             'city': offer.city,
                             'quarter': offer.quarter
                         })
        self.db.commit()
        # except Exception:
        #     print("Insert address: {}".format(sys.exc_info()[0]))

    def close(self):
        self.db.close()
