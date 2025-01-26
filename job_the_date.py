import requests
import json
from datetime import datetime, timedelta

def load_config():
    try:
        with open("tokens.json", "r") as file:
            data = json.load(file)
            return data["access_token"]
    except FileNotFoundError:
        print("Error: tokens.json not found.")
        return None
    except KeyError:
        print("Error: Access token not found in access_token.json.")
        return None


access_token = load_config()
if not access_token:
    raise ValueError("Access token is missing. Ensure tokens.json is properly configured.")




# Function to execute the GraphQL query
def run_query(query, variables, headers):
    response = requests.post('https://your-graphql-endpoint.com/graphql', json={'query': query, 'variables': variables}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

# Function to fetch all jobs for a specific date
def fetch_all_jobs_for_date(date_str, headers):
    all_jobs = []
    query = """
    query GetJobsForDate($after: String, $start_date: ISO8601DateTime!, $end_date: ISO8601DateTime!) {
        jobs(filter: { startAt: { after: $start_date, before: $end_date } }, first: 20, after: $after) {
            edges {
                node {
                    id
                    title
                    client {
                        name
                    }
                    startAt
                    lineItems {
                        edges {
                            node {
                                description
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
    # Convert the input date to ISO format
    start_date = datetime.strptime(date_str, "%d/%m/%Y").isoformat() + "Z"
    end_date = (datetime.strptime(date_str, "%d/%m/%Y") + timedelta(days=1)).isoformat() + "Z"
    variables = {'after': None, 'start_date': start_date, 'end_date': end_date}

    while True:
        result = run_query(query, variables, headers)
        jobs = result['data']['jobs']['edges']
        all_jobs.extend([job['node'] for job in jobs])  # Collect job details
        page_info = result['data']['jobs']['pageInfo']
        if page_info['hasNextPage']:
            variables['after'] = page_info['endCursor']
        else:
            break

    return all_jobs

# Main script
if __name__ == "__main__":
    # Input date in DD/MM/YYYY format
    date_input = input("Enter the date (DD/MM/YYYY): ")
    # Replace with your actual API token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-JOBBER-GRAPHQL-VERSION": "2024-12-05"
    }

    try:
        jobs = fetch_all_jobs_for_date(date_input, headers)
        # Save the results to a JSON file
        with open('results.json', 'w') as f:
            json.dump(jobs, f, indent=2)
        print(f"Saved {len(jobs)} jobs to results.json")
    except Exception as e:
        print(f"An error occurred: {e}")
