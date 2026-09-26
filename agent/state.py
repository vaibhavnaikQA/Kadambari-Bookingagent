class ConversationState:

    def __init__(self):
        self.ride = None
        self.date = None
        self.people = None
        self.time = None
        self.confirmation_pending = False

    def update(self, booking_data):

        if booking_data.get("ride") is not None:
            self.ride = booking_data["ride"]

        if booking_data.get("date") is not None:
            self.date = booking_data["date"]

        if booking_data.get("people") is not None:
            self.people = booking_data["people"]

        if booking_data.get("time") is not None:
            self.time = booking_data["time"]

    def get_booking(self):

        return {
            "ride": self.ride,
            "date": self.date,
            "people": self.people,
            "time": self.time
        }

    def missing_information(self):

        missing = []

        if self.ride is None:
            missing.append("ride")

        if self.date is None:
            missing.append("date")

        if self.people is None:
            missing.append("people")

        if self.time is None:
            missing.append("time")

        return missing

    def clear(self):
        self.ride = None
        self.date = None
        self.people = None
        self.time = None

    def reset(self):
        self.ride = None
        self.date = None
        self.people = None
        self.time = None
        self.confirmation_pending = False