from database.database import Database
from utils.date_utils import normalize_date


class AvailabilityService:

    # Valid operating slots
    SLOTS = {
        "backwater": [
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00"
        ],
        "sunset": [
            "17:30"
        ],
        "dolphin": [
            "08:00",
            "10:00",
            "12:00"
        ],
        "scuba": [
            "08:30"
        ]
    }

    # Every ride has 30 seats
    CAPACITY = 30

    def __init__(self):
        self.database = Database()

    def create_slot_if_needed(
        self,
        ride,
        date,
        time_slot
    ):
        # Check whether ride exists
        if ride not in self.SLOTS:
            return False

        # Check whether requested time is valid
        if time_slot not in self.SLOTS[ride]:
            return False

        # Check if slot already exists
        slot = self.database.get_availability(
            ride,
            date,
            time_slot
        )

        # Create it if it doesn't exist
        if slot is None:
            self.database.add_availability(
                ride=ride,
                booking_date=date,
                booking_time=time_slot,
                capacity=self.CAPACITY
            )

        return True

    def check_availability(
        self,
        ride,
        date,
        people,
        time_slot
    ):
        # Convert "today" / "tomorrow" to YYYY-MM-DD
        date = normalize_date(date)

        # Normalize values
        ride = ride.lower().strip()
        time_slot = time_slot.strip()

        # Create the slot automatically
        slot_created = self.create_slot_if_needed(
            ride,
            date,
            time_slot
        )

        # Invalid ride or time
        if not slot_created:
            return {
                "available": False,
                "reason": (
                    f"{ride.capitalize()} is not available "
                    f"at {time_slot}."
                )
            }

        # Get the slot
        slot = self.database.get_availability(
            ride,
            date,
            time_slot
        )

        # Get existing bookings
        booked_people = self.database.get_booked_people(
            ride,
            date,
            time_slot
        )

        # Calculate remaining seats
        available_people = (
            slot["capacity"] - booked_people
        )

        # Not enough seats
        if available_people < people:
            return {
                "available": False,
                "ride": ride,
                "date": date,
                "time": time_slot,
                "capacity": slot["capacity"],
                "booked_people": booked_people,
                "available_people": available_people,
                "requested_people": people,
                "reason": "Not enough seats available."
            }

        # Available
        return {
            "available": True,
            "ride": ride,
            "date": date,
            "time": time_slot,
            "capacity": slot["capacity"],
            "booked_people": booked_people,
            "available_people": available_people,
            "requested_people": people
        }