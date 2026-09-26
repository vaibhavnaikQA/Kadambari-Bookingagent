import uuid

from database.database import Database


class BookingService:

    def __init__(self):

        self.database = Database()

    def generate_booking_id(self):

        unique_number = uuid.uuid4().hex[:6].upper()

        return f"KJ-{unique_number}"

    def create_booking(
        self,
        booking,
        price_per_person,
        total_price
    ):

        booking_id = self.generate_booking_id()

        self.database.insert_booking(

            booking_id=booking_id,

            ride=booking["ride"],

            booking_date=booking["date"],

            booking_time=booking.get("time"),

            people=booking["people"],

            price_per_person=price_per_person,

            total_price=total_price,

            status="CONFIRMED"
        )

        return {
            "booking_id": booking_id,
            "status": "CONFIRMED",
            "booking": booking,
            "price_per_person": price_per_person,
            "total_price": total_price
        }

    def get_booking(self, booking_id):

        return self.database.get_booking(
            booking_id
        )