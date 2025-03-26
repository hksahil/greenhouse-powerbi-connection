import requests
import pandas as pd
import base64

def get_greenhouse_data(api_token, endpoint):
    credential = base64.b64encode(f"{api_token}:".encode()).decode()
    headers = {"Authorization": f"Basic {credential}"}

    all_data = []
    page = 1
    while True:
        params = {"page": page, "per_page": 100}
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()  # API returns data as a list
            if not data:
                break
            all_data.extend(data)
            print(f"Fetched {len(data)} records from page {page}")
            page += 1
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    return all_data

def main():
    api_token = '' # Note: This needs to be b64 encoded key not plain key, so convert the key to b64 using b64 library
    endpoint = 'https://harvest.greenhouse.io/v1/jobs'

    try:
        data = get_greenhouse_data(api_token, endpoint)
        df = pd.DataFrame(data)

        # Save the data to a CSV file
        csv_file = "greenhouse_jobs_data.csv"
        df.to_csv(csv_file, index=False)

        print(f"Data successfully saved to {csv_file}")
        return df
    except Exception as e:
        print(e)
        return pd.DataFrame()

if __name__ == "__main__":
    df = main()
