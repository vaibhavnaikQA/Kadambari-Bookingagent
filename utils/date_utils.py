from datetime import datetime, timedelta


def normalize_date(date_text):
    if not date_text:
        return None

    date_text = date_text.strip().lower()

    today = datetime.now().date()

    if date_text == "today":
        return today.isoformat()

    if date_text == "tomorrow":
        return (today + timedelta(days=1)).isoformat()

    try:
        parsed_date = datetime.strptime(
            date_text,
            "%Y-%m-%d"
        ).date()

        return parsed_date.isoformat()

    except ValueError:
        return date_text