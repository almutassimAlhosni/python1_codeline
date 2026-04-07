import requests

# Simple country code → country name mapping
country_map = {
    "US": "United States",
    "NG": "Nigeria",
    "GB": "United Kingdom",
    "IN": "India",
    "CA": "Canada",
    "AU": "Australia",
    "FR": "France",
    "DE": "Germany",
    "BR": "Brazil",
    "IT": "Italy",
    "ES": "Spain",
    "MX": "Mexico"
}

def main():
    name = input("Enter a name: ").strip()
    
    if not name:
        print("Please enter a valid name.")
        return

    url = f"https://api.nationalize.io?name={name}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return

    countries = data.get("country", [])

    if not countries:
        print("No country data found.")
        return

    print(f"\nPossible countries for '{name}':\n")

    for c in countries:
        code = c.get("country_id")
        probability = c.get("probability", 0)

        country_name = country_map.get(code, code)
        percentage = probability * 100

        print(f"{country_name}: {percentage:.2f}%")

if __name__ == "__main__":
    main()