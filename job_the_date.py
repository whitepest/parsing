import requests
import json
import csv
from datetime import datetime, timedelta
from this_date import get_iso_date  # Import the function from this_date.py

def load_config():
    try:
        with open("tokens.json", "r") as file:
            data = json.load(file)
            return data["access_token"]
    except FileNotFoundError:
        print("Error: tokens.json not found.")
        return None
    except KeyError:
        print("Error: Access token not found in tokens.json.")
        return None

access_token = load_config()
if not access_token:
    raise ValueError("Access token is missing. Ensure tokens.json is properly configured.")

# Function to execute the GraphQL query
def run_query(query, variables, headers):
    response = requests.post('https://api.getjobber.com/api/graphql', json={'query': query, 'variables': variables}, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

#clean line break
def clean_multiline(value):
    return value.replace('\n', ' ').strip()

# Function to fetch all jobs for a specific date
def fetch_all_jobs_for_date(iso_date, headers, sort_type, sort_line):
    sort_line = sort_line.lower()
    all_jobs = []
    query = """
    query GetJobsForDate($after: String, $start_date: ISO8601DateTime!, $end_date: ISO8601DateTime!) {
        jobs(filter: { startAt: { after: $start_date, before: $end_date } }, first: 20, after: $after) {
            edges {
                node {
                    title
                    client {
                        name
                    }
                    startAt
                    lineItems {
                        edges {
                            node {
                                name
                                description
                                quantity
                            }
                        }
                    }
                }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
    """
    # Extract the start and end of the day from the ISO date
    start_date = iso_date
    end_date = (datetime.strptime(iso_date, "%Y-%m-%dT00:00:00Z") + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
    #print("end_date: ", end_date)
    variables = {'after': None, 'start_date': start_date, 'end_date': end_date}
    while True:
        result = run_query(query, variables, headers)
        jobs = result['data']['jobs']['edges']
        for job in jobs:
            job_node = job['node']
            filtered_line_items = []
            for item in job_node.get('lineItems', {}).get('edges', []):
                node_data = item.get('node', {})
                name = node_data.get('name', '')
                description = node_data.get('description', '')
                if sort_type == "description":
                    if sort_line in description.lower():
                        filtered_line_items.append({'node': node_data})
                elif sort_type == "name":
                    if sort_line in name.lower():
                        filtered_line_items.append({'node': node_data})
                else :
                    print("sort_type inccorect")
                    break
            if filtered_line_items:
                job_node['lineItems']['edges'] = filtered_line_items
                all_jobs.append(job_node)
        page_info = result['data']['jobs']['pageInfo']
        print("Jobs received:", len(jobs))
        if page_info['hasNextPage']:
            variables['after'] = page_info['endCursor']
        else:
            break
    return all_jobs

# Function to create the table of glass with a total count
def create_table_with_total_glass(jobs, output_file, iso_date):
    if not jobs:
        print("No jobs found for the specified date.")
        return

    total_glass_panes = 0

    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(['Item Name', 'Title', 'Name', 'Glass Type', 'QNT', 'Glass Size', 'OA', 'Muntin Bars', 'Unsorted'])

            for job in jobs:
                title = job.get('title', 'N/A')
                client_name = job.get('client', {}).get('name', 'N/A')
                line_items = job.get('lineItems', {}).get('edges', [])

                for item in line_items:
                    node = item.get('node', {})
                    item_name = node.get('name', 'N/A')
                    description = node.get('description', 'N/A')
                    quantity = node.get('quantity', 0)
                    total_glass_panes += quantity  # Accumulate total glass panes
                    
                    # Extract glass details from the description
                    glass_type_lines = []
                    oa_lines = []
                    muntin_bars_lines = []
                    size_lines = []
                    unsorted_lines = []
                    
                    collecting_size = False
                    
                    # Parsing the description (assumes consistent format)
                    for line in description.splitlines():
                        line = line.lower().strip()

                        if "glass type" in line:
                            glass_type_lines.append(line.split(":", 1)[1].strip())
                        elif "oa" in line:
                            oa_lines.append(line.split(":", 1)[1].strip())
                        elif "muntin bars" in line:
                            muntin_bars_lines.append(line.split(":", 1)[1].strip())
                        elif "size" in line:
                            collecting_size = True
                            size_lines.append(line.split(":", 1)[1].strip())
                        elif collecting_size:
                            if line == "" or any(x in line for x in ["glass type", "oa", "muntin bars", "size"]):
                                collecting_size = False
                            else:
                                size_lines.append(line)
                        else:
                            unsorted_lines.append(line)
                    
                    glass_type = clean_multiline(" | ".join(glass_type_lines)) if glass_type_lines else "N/A"
                    oa = clean_multiline(" | ".join(oa_lines)) if oa_lines else "N/A"
                    muntin_bars = clean_multiline(" | ".join(muntin_bars_lines)) if muntin_bars_lines else "N/A"
                    glass_size = clean_multiline(" | ".join(size_lines)) if size_lines else "N/A"
                    unsorted = clean_multiline(" | ".join(unsorted_lines)) if unsorted_lines else "N/A"
                    # Write the row
                    writer.writerow([item_name, title, client_name, glass_type, quantity, glass_size, oa, muntin_bars, unsorted])

            # Write the total row at the end
            writer.writerow([])
            writer.writerow(['Total Glass', total_glass_panes, 'Date', iso_date, '', '', '', ''])

        print(f"CSV table with total glass panes created successfully at {output_file}")
    except Exception as e:
        print(f"An error occurred while creating the glass table: {e}")

# Function to create the table of screen with a total count
def create_table_with_total_screen(jobs, output_file, iso_date):
    if not jobs:
        print("No jobs found for the specified date.")
        return

    total_screen_panes = 0

    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(['Item Name','Title', 'Name', 'Size', 'QNT', 'Color', 'Springs', 'Pins', 'Middle bar', 'Puls', 'Unsorted'])

            for job in jobs:
                title = job.get('title', 'N/A')
                client_name = job.get('client', {}).get('name', 'N/A')
                line_items = job.get('lineItems', {}).get('edges', [])

                for item in line_items:
                    node = item.get('node', {})
                    item_name = node.get('name', 'N/A')
                    description = node.get('description', 'N/A')
                    quantity = node.get('quantity', 0)
                    total_screen_panes += quantity  # Accumulate total screen panes
                    
                    # Extract screen details from the description
                    color_lines = []
                    spring_lines = []
                    pins_lines = []
                    middle_bar_lines = []
                    puls_lines = []
                    size_lines = []
                    unsorted_lines = []

                    collecting_size = False

                    # Parsing the description (assumes consistent format)
                    for line in description.splitlines():
                        line = line.lower().strip()

                        if "color" in line and ":" in line:
                            color_lines.append(line.split(":", 1)[1].strip())
                        elif "springs" in line:
                            spring_lines.append(line.strip())
                        elif "pins" in line:
                            pins_lines.append(line.split(":", 1)[1].strip())
                        elif "middle bar" in line:
                            middle_bar_lines.append(line.split(":", 1)[1].strip())
                        elif "puls" in line:
                            puls_lines.append(line.split(":", 1)[1].strip())
                        elif "size" in line:
                            collecting_size = True
                            size_lines.append(line.split(":", 1)[1].strip())
                        elif collecting_size:
                            if line == "" or any(x in line for x in ["color", "springs", "pins", "middle bar", "puls"]):
                                collecting_size = False
                            else:
                                size_lines.append(line)
                        else:
                            unsorted_lines.append(line)
                    
                    screen_color = clean_multiline(" | ".join(color_lines)) if color_lines else "N/A"
                    spring = clean_multiline(" | ".join(spring_lines)) if spring_lines else "N/A"
                    pins = clean_multiline(" | ".join(pins_lines)) if pins_lines else "N/A"
                    middle_bar = clean_multiline(" | ".join(middle_bar_lines)) if middle_bar_lines else "N/A"
                    puls = clean_multiline(" | ".join(puls_lines)) if puls_lines else "N/A"
                    screen_size = clean_multiline(" | ".join(size_lines)) if size_lines else "N/A"
                    unsorted = clean_multiline(" | ".join(unsorted_lines)) if unsorted_lines else "N/A"

                    # Write the row
                    writer.writerow([item_name, title, client_name, screen_size, quantity, screen_color, spring, pins, middle_bar, puls, unsorted])

            # Write the total row at the end
            writer.writerow([])
            writer.writerow(['Total Screen', total_screen_panes, 'Date', iso_date, '', '', '', '', '', ''])

        print(f"CSV table with total screen panes created successfully at {output_file}")
    except Exception as e:
        print(f"An error occurred while creating the screen table: {e}")


# Main script
if __name__ == "__main__":
    # Input date in DD/MM format
    date_input = input("Enter the date (DD/MM): ")
    iso_date = get_iso_date(date_input)

    if iso_date.startswith("Invalid"):
        print(iso_date)
    else:
        # Replace with your actual API token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-JOBBER-GRAPHQL-VERSION": "2024-12-05"
        }

        try:
            sort_type_name = 'name'
            sort_type_description = 'description'
            sort_line_glass = 'Glass type:'
            sort_line_screen = 'screen'

            glass_jobs = fetch_all_jobs_for_date(iso_date, headers, sort_type_description, sort_line_glass)
            screen_jobs = fetch_all_jobs_for_date(iso_date, headers, sort_type_name, sort_line_screen)
            # Define json file
            results_glass_file = 'results_glass.json'
            results_screen_file = 'result_screen.json'
            # Save the results to a JSON file
            with open(results_glass_file, 'w') as f:
                json.dump(glass_jobs, f, indent=2)
            print(f"Saved {len(glass_jobs)} jobs to {results_glass_file}")
            
            with open(results_screen_file, 'w') as f:
                json.dump(screen_jobs, f, indent=2)
            print(f"Saved {len(screen_jobs)} jobs to {results_screen_file}")
            
            # Generate the table
            table_file = 'glass_table.csv'
            screen_file = 'screen_table.csv'
            create_table_with_total_glass(glass_jobs, table_file, iso_date)
            create_table_with_total_screen(screen_jobs, screen_file, iso_date)
            print(f"Table generated and saved to {table_file}")
        except Exception as e:
            print(f"An error occurred: {e}")
