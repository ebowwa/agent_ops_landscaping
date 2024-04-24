# create_output_csv.py
import pandas as pd

def load_data():
    # Load Bay Area data
    bay_area_data = pd.read_csv('input/Bay_Area.csv')
    bay_area_data['Neighborhoods'] = bay_area_data['Neighborhoods'].str.split('\n')

    # Load services data
    services_data = pd.read_csv('input/gallery.csv')

    company_name = "Goldson Landscaping"
    company_services = services_data['Item'].tolist()

    output_data = {
        "company_name": company_name,
        "services": company_services,
        "service_coverage": {}
    }

    for service in company_services:
        service_coverage = {}
        for city in bay_area_data['City/Town'].unique():
            neighborhoods = bay_area_data.loc[bay_area_data['City/Town'] == city, 'Neighborhoods'].tolist()[0]
            service_coverage[city] = neighborhoods
        output_data['service_coverage'][service] = service_coverage

    return output_data

def create_output_csv():
    output_data = load_data()

    # Create a list of tuples with (service, city) pairs
    service_city_pairs = [(service, city) for service in output_data['services'] for city in output_data['service_coverage'][service]]

    # Create a DataFrame from the list of tuples
    output_df = pd.DataFrame(service_city_pairs, columns=['Service', 'City'])

    # Add a new column with the city and neighborhoods
    output_df['City & Neighborhoods'] = output_df.apply(lambda row: f"{row['City']}: {', '.join(output_data['service_coverage'][row['Service']][row['City']])}", axis=1)

    # Save the DataFrame to a CSV file
    output_df.to_csv('output/output.csv', index=False)

if __name__ == "__main__":
    create_output_csv()