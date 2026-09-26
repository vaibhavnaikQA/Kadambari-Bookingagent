import sqlite3


class Database:

    def __init__(self, database_name="kadambari.db"):

        self.database_name = database_name

        self.create_tables()

    def get_connection(self):

        connection = sqlite3.connect(
            self.database_name
        )

        connection.row_factory = sqlite3.Row

        return connection

    def create_tables(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                booking_id TEXT UNIQUE NOT NULL,

                ride TEXT NOT NULL,

                booking_date TEXT NOT NULL,

                booking_time TEXT,

                people INTEGER NOT NULL,

                price_per_person INTEGER NOT NULL,

                total_price INTEGER NOT NULL,

                status TEXT NOT NULL,

                customer_name TEXT,

                customer_phone TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS availability (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ride TEXT NOT NULL,
                booking_date TEXT NOT NULL,
                booking_time TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                UNIQUE(ride, booking_date, booking_time)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS availability (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ride TEXT NOT NULL,
                booking_date TEXT NOT NULL,
                booking_time TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                UNIQUE(ride, booking_date, booking_time)
            )
        """)

        connection.commit()

        connection.close()

    def insert_booking(
        self,
        booking_id,
        ride,
        booking_date,
        booking_time,
        people,
        price_per_person,
        total_price,
        status="CONFIRMED",
        customer_name=None,
        customer_phone=None
    ):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO bookings (
                booking_id,
                ride,
                booking_date,
                booking_time,
                people,
                price_per_person,
                total_price,
                status,
                customer_name,
                customer_phone
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            booking_id,
            ride,
            booking_date,
            booking_time,
            people,
            price_per_person,
            total_price,
            status,
            customer_name,
            customer_phone
        ))

        connection.commit()

        connection.close()

    def get_booking(self, booking_id):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM bookings
            WHERE booking_id = ?
        """, (booking_id,))

        booking = cursor.fetchone()

        connection.close()

        if booking is None:
            return None

        return dict(booking)

    def get_all_bookings(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM bookings
            ORDER BY created_at DESC
        """)

        bookings = cursor.fetchall()

        connection.close()

        return [dict(booking) for booking in bookings]

    def add_availability(
            self,
            ride,
            booking_date,
            booking_time,
            capacity
    ):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO availability (
                ride,
                booking_date,
                booking_time,
                capacity
            )
            VALUES (?, ?, ?, ?)
        """, (
            ride,
            booking_date,
            booking_time,
            capacity
        ))

        connection.commit()
        connection.close()

    def get_availability(
            self,
            ride,
            booking_date,
            booking_time
    ):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM availability
            WHERE ride = ?
            AND booking_date = ?
            AND booking_time = ?
        """, (
            ride,
            booking_date,
            booking_time
        ))

        result = cursor.fetchone()

        connection.close()

        if result is None:
            return None

        return dict(result)

    def get_booked_people(self, ride, booking_date, booking_time):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(people), 0) AS booked_people
            FROM bookings
            WHERE ride = ?
            AND booking_date = ?
            AND booking_time = ?
            AND status = 'CONFIRMED'
        """, (
            ride,
            booking_date,
            booking_time
        ))

        result = cursor.fetchone()

        connection.close()

        return result["booked_people"]

    def add_availability(
            self,
            ride,
            booking_date,
            booking_time,
            capacity=30
    ):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO availability (
                ride,
                booking_date,
                booking_time,
                capacity
            )
            VALUES (?, ?, ?, ?)
        """, (
            ride,
            booking_date,
            booking_time,
            capacity
        ))

        connection.commit()
        connection.close()

    def get_availability(
            self,
            ride,
            booking_date,
            booking_time
    ):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM availability
            WHERE ride = ?
            AND booking_date = ?
            AND booking_time = ?
        """, (
            ride,
            booking_date,
            booking_time
        ))

        result = cursor.fetchone()

        connection.close()

        if result is None:
            return None

        return dict(result)

    def get_booked_people(
            self,
            ride,
            booking_date,
            booking_time
    ):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(people), 0) AS booked_people
            FROM bookings
            WHERE ride = ?
            AND booking_date = ?
            AND booking_time = ?
            AND status = 'CONFIRMED'
        """, (
            ride,
            booking_date,
            booking_time
        ))

        result = cursor.fetchone()

        connection.close()

        return result["booked_people"]