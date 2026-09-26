import json

from llm.gemini_client import GeminiClient
from booking.availability import AvailabilityService
from booking.pricing import PricingService
from agent.state import ConversationState
from booking.booking import BookingService

class BookingAgent:

    def __init__(self):

        self.name = "Kadambari Booking Agent"

        self.llm = GeminiClient()

        self.availability_service = AvailabilityService()

        self.pricing_service = PricingService()

        self.booking_service = BookingService()

        self.state = ConversationState()

    def process_message(self, message):

        # -----------------------------------
        # CONFIRMATION
        # -----------------------------------

        if self.state.confirmation_pending:

            answer = message.lower().strip()

            if answer in [
                "yes",
                "y",
                "confirm",
                "confirmed",
                "yes confirm"
            ]:
                booking = self.state.get_booking()

                price_per_person = self.pricing_service.get_price(
                    booking["ride"]
                )

                total_price = self.pricing_service.calculate_total(
                    booking["ride"],
                    booking["people"]
                )

                result = self.booking_service.create_booking(
                    booking=booking,
                    price_per_person=price_per_person,
                    total_price=total_price
                )

                self.state.reset()

                return {
                    "status": "confirmed",
                    "message": (
                        f"Booking confirmed!\n"
                        f"Booking ID: {result['booking_id']}\n"
                        f"Ride: {booking['ride']}\n"
                        f"Date: {booking['date']}\n"
                        f"Time: {booking['time']}\n"
                        f"People: {booking['people']}\n"
                        f"Total: ₹{total_price}"
                    ),
                    "booking": result
                }

            if answer in [
                "no",
                "n",
                "cancel",
                "cancelled"
            ]:
                self.state.reset()

                return {
                    "status": "cancelled",
                    "message": "No problem. The booking has been cancelled."
                }

            return {
                "status": "confirmation_required",
                "message": (
                    "Please reply Yes to confirm "
                    "or No to cancel."
                )
            }

        # -----------------------------------
        # NORMAL MESSAGE
        # -----------------------------------

        booking_data = self.extract_booking_data(message)

        if "error" in booking_data:
            return booking_data

        print("\nGemini extracted:")
        print(booking_data)

        # Save information
        self.state.update(booking_data)

        booking = self.state.get_booking()

        print("\nCurrent booking:")
        print(booking)

        # -----------------------------------
        # CHECK MISSING INFORMATION
        # -----------------------------------

        missing = self.state.missing_information()

        if missing:

            if "ride" in missing:
                return {
                    "status": "missing_information",
                    "message": "Which ride would you like to book?"
                }

            if "date" in missing:
                return {
                    "status": "missing_information",
                    "message": "What date would you like to book?"
                }

            if "people" in missing:
                return {
                    "status": "missing_information",
                    "message": "How many people will be joining?"
                }

            if "time" in missing:
                return {
                    "status": "missing_information",
                    "message": "What time would you prefer?"
                }

        # -----------------------------------
        # CHECK AVAILABILITY
        # -----------------------------------

        availability = self.availability_service.check_availability(
            ride=booking["ride"],
            date=booking["date"],
            people=booking["people"],
            time_slot=booking["time"]
        )

        if not availability["available"]:
            return {
                "status": "unavailable",
                "message": (
                    "Sorry, the requested ride is not available "
                    "for that time."
                ),
                "booking": booking,
                "availability": availability
            }

        # -----------------------------------
        # PRICE
        # -----------------------------------

        price_per_person = self.pricing_service.get_price(
            booking["ride"]
        )

        total_price = self.pricing_service.calculate_total(
            booking["ride"],
            booking["people"]
        )

        # -----------------------------------
        # ASK FOR CONFIRMATION
        # -----------------------------------

        self.state.confirmation_pending = True

        return {
            "status": "confirmation_required",

            "message": (
                f"I have the following booking details:\n\n"
                f"Ride: {booking['ride']}\n"
                f"Date: {booking['date']}\n"
                f"Time: {booking['time']}\n"
                f"People: {booking['people']}\n\n"
                f"Price per person: ₹{price_per_person}\n"
                f"Total: ₹{total_price}\n\n"
                f"Would you like to confirm?"
            ),

            "booking": booking,

            "price_per_person": price_per_person,

            "total_price": total_price
        }

    def extract_booking_data(self, message):

        prompt = f"""
You are an AI booking assistant ONLY for Kadambari Jetty in Goa, India.

IMPORTANT:
You are NOT a Kerala backwater booking assistant.

Do NOT mention:
- Alleppey
- Kumarakom
- Munnar
- houseboats
- shikaras
- traditional houseboats
- Kerala
- any other destination

You are specifically helping customers book boat rides
with Kadambari Jetty in Goa.

Kadambari Jetty currently offers:

1. BACKWATER
   - Nerul River backwaters
   - Mangroves
   - Approximately 45 minutes

2. SUNSET
   - Sunset boat ride
   - Approximately 1 hour

3. DOLPHIN
   - Dolphin boat ride

Your task is ONLY to extract booking information
from the customer's message.

Customer message:

{message}

Return ONLY valid JSON.

The JSON MUST contain exactly these fields:

{{
    "ride": null,
    "date": null,
    "people": null,
    "time": null
}}

Rules:

1. ride can ONLY be:

   "backwater"
   "sunset"
   "dolphin"
   null

2. people must be an integer or null.

3. If the customer says "tomorrow",
   return:

   "tomorrow"

4. If the customer says "today",
   return:

   "today"

5. If the customer gives a specific date,
   preserve it as text.

6. If the customer says "evening",
   return:

   "evening"

7. If the customer says "morning",
   return:

   "morning"

8. If the customer says "afternoon",
   return:

   "afternoon"

9. If the customer gives a specific time,
   preserve it as text.

10. Do NOT guess missing information.

11. Do NOT ask questions.

12. Do NOT provide a customer response.

13. Do NOT provide prices.

14. Do NOT check availability.

15. Do NOT mention any destination other than Goa
    or Kadambari Jetty.

16. Do NOT return Markdown.

Return ONLY the JSON object.
"""

        response = self.llm.generate(prompt)

        cleaned = response.strip()

        # Gemini sometimes returns JSON inside ```json ... ```
        if cleaned.startswith("```"):

            cleaned = cleaned.replace(
                "```json",
                "",
                1
            )

            cleaned = cleaned.replace(
                "```",
                "",
                1
            )

            cleaned = cleaned.strip()

        try:

            return json.loads(cleaned)

        except json.JSONDecodeError:

            return {
                "error": "Gemini returned invalid JSON",
                "raw_response": response
            }