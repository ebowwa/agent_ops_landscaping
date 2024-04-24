import csv
import json

def load_data():
    with open('Bay_Area.csv', 'r') as f:
        bay_area_data = list(csv.DictReader(f))

    with open('gallery.csv', 'r') as f:
        services_data = list(csv.DictReader(f))

    company_name = "Goldson Landscaping"
    company_services = [row['Item'] for row in services_data]

    output_data = {
        "company_name": company_name,
        "services": company_services,
        "service_coverage": {}
    }

    for row in bay_area_data:
        city = row['City/Town']
        neighborhoods = [n.strip() for n in row['Neighborhoods'].split('\n')]

        for service in company_services:
            service_coverage = output_data['service_coverage'].get(service, {})
            service_coverage[city] = neighborhoods
            output_data['service_coverage'][service] = service_coverage

    for service, coverage in output_data['service_coverage'].items():
        for city in set(row['City/Town'] for row in bay_area_data):
            if city not in coverage:
                coverage[city] = []

    return output_data