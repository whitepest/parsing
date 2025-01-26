from datetime import datetime

def get_iso_date(input_date):
    """
    Convert a date in the format DD/MM to an ISO 8601 formatted date.
    """
    try:
        # Parse the input date in the format "DD/MM"
        parsed_date = datetime.strptime(input_date, "%d/%m")
        
        # Get the current year
        today = datetime.utcnow()
        parsed_date = parsed_date.replace(year=today.year)
        
        # If the parsed date is in the past for the current year, assume it's for the next year
        if parsed_date < today:
            parsed_date = parsed_date.replace(year=today.year + 1)
        
        # Return the date in ISO 8601 format
        return parsed_date.strftime("%Y-%m-%dT00:00:00Z")
    except ValueError:
        return "Invalid date format. Please enter the date in DD/MM format."

# Example usage
input_date = input("Enter a date (DD/MM): ")
iso_date = get_iso_date(input_date)
print(f"Formatted ISO 8601 date: {iso_date}")
