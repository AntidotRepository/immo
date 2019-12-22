class Offer():
    def __init__(self, offer):
        self.id = offer['id']
        self.modification = offer['modification']
        self.creation = offer['creation']
        self.title = offer['title']
        self.privateOffer = offer['privateOffer']
        self.price = float(offer['price'])
        self.livingSpace = offer['livingSpace']
        self.sq_meter_price = self.calculate_sq_meter_price()
        self.numberOfRooms = offer['numberOfRooms']
        self.energyPerfCert = offer['energyPerfCert']
        self.energyEfficiency = offer['energyEfficiency']
        self.builtInKitchen = offer['builtInKitchen']
        self.balcony = offer['balcony']
        self.garden = offer['garden']
        self.lift = offer['lift']
        self.guestToilet = offer['guestToilet']
        self.cellar = offer['cellar']
        self.isBarrierFree = offer['isBarrierFree']
        self.stillAvailable = offer['stillAvailable']
        self.lastTimeView = offer['lastTimeView']

        self.street = offer['street']
        self.houseNumber = offer['houseNumber']
        self.latitude = offer['latitude']
        self.longitude = offer['longitude']
        self.preciseHouseNumber = offer['preciseHouseNumber']
        self.postcode = offer['postcode']
        self.city = offer['city']
        self.quarter = offer['quarter']

    def calculate_sq_meter_price(self):
        # Calculate price per square meter.
        assert self.price != 0
        assert self.livingSpace != 0

        return self.price / self.livingSpace
