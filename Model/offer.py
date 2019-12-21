class Offer():
    def __init__(self, offer):
        realEstate = offer['resultlist.realEstate']
        self.id = realEstate['@id']
        self.modification = offer['@modification']
        self.creation = offer['@creation']
        self.title = realEstate['title']
        self.privateOffer = realEstate['privateOffer']
        self.price = float(realEstate['price']['value'])
        self.livingSpace = realEstate['livingSpace']
        self.sq_meter_price = self.calculate_sq_meter_price()
        self.numberOfRooms = realEstate['numberOfRooms']
        self.energyPerfCert = realEstate['energyPerfCert']
        self.energyEfficiency = realEstate['energyEfficiency']
        self.builtInKitchen = realEstate['builtInKitchen']
        self.balcony = realEstate['balcony']
        self.garden = realEstate['garden']
        self.lift = realEstate['lift']
        self.guestToilet = realEstate['guestToilet']
        self.cellar = realEstate['cellar']
        self.isBarrierFree = realEstate['isBarrierFree']
        self.stillAvailable = offer['stillAvailable']
        self.lastTimeView = offer['lastTimeView']

        address = realEstate['address']
        self.street = address['street']
        self.houseNumber = address['houseNumber']
        self.latitude = address['latitude']
        self.longitude = address['longitude']
        self.preciseHouseNumber = address['preciseHouseNumber']
        self.postcode = address['postcode']
        self.city = address['city']
        self.quarter = address['quarter']

    def calculate_sq_meter_price(self):
        # Calculate price per square meter.
        assert self.price != 0
        assert self.livingSpace != 0

        return self.price / self.livingSpace
