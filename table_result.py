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
    rows.append(["", "", "", "", "", f"Total Glasses: {glass_count}"])

    # Write the table to a CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)   # Write rows

    print(f"Table created and saved to {output_file}")

# Run the function
create_table_with_glass_count('results.json', 'glass_table.csv')
