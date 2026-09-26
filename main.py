from agent.agent import BookingAgent


def main():

    agent = BookingAgent()

    print("===================================")
    print("   Kadambari Jetty Booking Agent")
    print("===================================")
    print()
    print("Type 'exit' to quit.")
    print()

    while True:

        message = input("Customer: ").strip()

        if message.lower() == "exit":
            break

        if not message:
            continue

        try:

            result = agent.process_message(message)

            print("\nAgent:")
            print(result["message"] if "message" in result else result)

            print()

        except Exception as e:

            print("\nError:")
            print(e)
            print()


if __name__ == "__main__":
    main()