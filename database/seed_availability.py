from database import Database


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


CAPACITY = {
    "backwater": 20,
    "sunset": 20,
    "dolphin": 15,
    "scuba": 15
}


def seed_availability():
    database = Database()

    for ride, times in SLOTS.items():

        for time_slot in times:

            database.add_availability(
                ride=ride,
                booking_date="2026-09-27",
                booking_time=time_slot,
                capacity=CAPACITY[ride]
            )

    print("Availability seeded successfully.")


if __name__ == "__main__":
    seed_availability()