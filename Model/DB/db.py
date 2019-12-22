import sqlite3


class DB():
    def __init__(self, **kwargs):
        # Create connection to database
        self.db = sqlite3.connect('Model/DB/immo.db')
        self.cursor = self.db.cursor()

    def insert_offer(self, offer):
        # try:
        # print("Insert {}".format(offer.title))
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

    def get_all_offers(self):
        self.cursor.execute('''SELECT offers.id, offers.modification,
                                      offers.creation, offers.title,
                                      offers.privateOffer, offers.price,
                                      offers.livingSpace,
                                      offers.sq_meter_price,
                                      offers.numberOfRooms,
                                      offers.energyPerfCert,
                                      offers.energyEfficiency,
                                      offers.builtInKitchen,
                                      offers.balcony, offers.garden,
                                      offers.lift, offers.guestToilet,
                                      offers.cellar, offers.isBarrierFree,
                                      offers.stillAvailable,
                                      offers.lastTimeView, addresses.street,
                                      addresses.houseNumber,
                                      addresses.latitude, addresses.longitude,
                                      addresses.preciseHouseNumber,
                                      addresses.postcode, addresses.city,
                                      addresses.quarter
                               FROM offers
                               INNER JOIN addresses
                               ON offers.id = addresses.appartment_id;
            ''')
        lines = self.cursor.fetchall()

        list_offers = list()
        for line in lines:
            dict_offer = dict()
            dict_offer['id'] = line[0]
            dict_offer['modification'] = line[1]
            dict_offer['creation'] = line[2]
            dict_offer['title'] = line[3]
            dict_offer['privateOffer'] = line[4]
            dict_offer['price'] = line[5]
            dict_offer['livingSpace'] = line[6]
            dict_offer['sq_meter_price'] = line[7]
            dict_offer['numberOfRooms'] = line[8]
            dict_offer['energyPerfCert'] = line[9]
            dict_offer['energyEfficiency'] = line[10]
            dict_offer['builtInKitchen'] = line[11]
            dict_offer['balcony'] = line[12]
            dict_offer['garden'] = line[13]
            dict_offer['lift'] = line[14]
            dict_offer['guestToilet'] = line[15]
            dict_offer['cellar'] = line[16]
            dict_offer['isBarrierFree'] = line[17]
            dict_offer['stillAvailable'] = line[18]
            dict_offer['lastTimeView'] = line[19]
            dict_offer['street'] = line[20]
            dict_offer['houseNumber'] = line[21]
            dict_offer['latitude'] = line[22]
            dict_offer['longitude'] = line[23]
            dict_offer['preciseHouseNumber'] = line[24]
            dict_offer['postcode'] = line[25]
            dict_offer['city'] = line[26]
            dict_offer['quarter'] = line[27]
            list_offers.append(dict_offer)

        return list_offers
