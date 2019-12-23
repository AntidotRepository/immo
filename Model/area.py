class Area:
    def __init__(self, posX, posY, width, height):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.average_price = 0
        self.offers = list()

    def add_offer(self, offer):
        self.offers.append(offer)

    def calc_average(self):
        total_price = 0
        for an_offer in self.offers:
            total_price += an_offer.sq_meter_price

        self.average_price = total_price / len(self.offers)

        for offer in self.offers:
            print("Here")
            offer.area_average_price = self.average_price
