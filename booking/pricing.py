class PricingService:

    prices = {
        "backwater": 350,
        "sunset": 500,
        "dolphin": 400
    }

    def get_price(self, ride):
        return self.prices.get(ride)

    def calculate_total(self, ride, people):
        price = self.get_price(ride)

        if price is None:
            return None

        return price * people