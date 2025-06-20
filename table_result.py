import json
import csv

def create_table_with_glass_count(input_file, output_file):
    # Load the JSON data
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Prepare the table headers
    headers = ["Title", "Name", "Glass Type", "Glass Size", "OA", "Muntin Bars"]

    # Prepare the rows for the table
    rows = []
    glass_count = 0  # Initialize the glass counter

    for job in data:
        for line_item in job["lineItems"]["edges"]:
            description = line_item["node"]["description"]
            if "Glass Type:" in description:
                # Extract details
                glass_type = description.split("Glass Type:")[1].split("\n")[0].strip()
                size = description.split("Size:")[1].split("\n")[0].strip() if "Size:" in description else "N/A"
                oa = description.split("OA:")[1].split("\n")[0].strip() if "OA:" in description else "N/A"
                muntin_bars = description.split("Muntin Bars:")[1].split("\n")[0].strip() if "Muntin Bars:" in description else "N/A"

                # Add a row for the table
                rows.append([job["title"], job["client"]["name"], glass_type, size, oa, muntin_bars])
                glass_count += 1  # Increment the glass counter

    # Add a final row for the total count of glasses
    rows.append([f"Date: {date}", "", "", "", "", f"Total Glasses: {glass_count}"])

    # Write the table to a CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)   # Write rows

    print(f"Table created and saved to {output_file}")

#same as above but for screen
def create_table_with_screen_count(input_file, output_file):
    # Load the JSON data
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Prepare the table headers
    headers = ["Title", "Name", "Size", "Color", "Spring", "Pins", "Middle bar", "Puls"]

    # Prepare the rows for the table
    rows = []
    screen_count = 0  # Initialize the screen counter

    for job in data:
        for line_item in job["lineItems"]["edges"]:
            description = line_item["node"]["description"]
            # Extract screen details
            size = color = spring = pins = middle_bar = puls = "N/A"
            for line in description.splitlines():
                if "Size:" in line:
                    size = line.split("Size:")[1].strip()
                elif "Color:" in line:
                    color = line.split("Color:")[1].strip()
                elif "Spring:" in line:
                    spring = line.split("Spring:")[1].strip()
                elif "Pins:" in line:
                    pins = line.split("Pins:")[1].strip()
                elif "Middle bar:" in line:
                    middle_bar = line.split("Middle bar:")[1].strip()
                elif "Puls:" in line:
                    puls = line.split("Puls:")[1].strip()

            # Add a consistent 8-column row
            rows.append([title, client_name, size, color, spring, pins, middle_bar, puls])
            screen_count += 1

    # Add a final row for the total count of screens
    total_row = [""] * 7 + [f"Total Screen: {screen_count}"]
    #if date:
    #    total_row[0] = f"Date: {date}"
    rows.append(total_row)

    # Write the table to a CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)   # Write rows

    print(f"Table created and saved to {output_file}")

# Run the function
create_table_with_glass_count('results.json', 'glass_table.csv')
create_table_with_screen_count('result_screen.json', 'screen_table.csv')
