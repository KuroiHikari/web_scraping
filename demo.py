# ### Imports
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re


# Function to extract year, brand, and type from the name
def extract_info(name):
    match = re.match(r'(\d{4})\s(.+?)\s(.+)', name)

    if match:
        year = match.group(1)
        brand = match.group(2)
        car_type = match.group(3)
        return year, brand, car_type
    else:
        return 'n/a', 'n/a', 'n/a'



# Pagination
name = []
mileage = []
dealer = []
rating = []
reviews = []
price = []

for i in range(1,11):
    # Website in variable
    # website = 'https://www.cars.com/shopping/results/?makes[]=mercedes_benz&maximum_distance=all&models[]=&page=' + str(i) + '&stock_type=cpo&zip='
    website = 'https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&maximum_distance=20&mileage_max=&monthly_payment=&page=' + str(i) + '&page_size=20&sort=best_match_desc&stock_type=cpo&year_max=&year_min=&zip='
    # Request to website
    response = requests.get(website)

    # Soup Object
    soup = BeautifulSoup(response.content, 'html.parser')

    # Results
    results = soup.find_all('div', {'class': 'vehicle-card'})

    # For loop for cars in 1 page
    for result in results:
        # name
        try:
            name.append(result.find('h2').get_text())
        except:
            name.append('n/a')

        # mileage
        try:
            mileage.append(result.find('div', {'class': 'mileage'}).get_text())
        except:
            mileage.append('0')

        # dealer
        try:
            dealer.append(result.find('div', {'class': 'dealer-name'}).get_text().strip())
        except:
            dealer.append('n/a')

        # rating
        try:
            rating.append(result.find('span', {'class': 'sds-rating__count'}).get_text())
        except:
            rating.append('0')

        # reviews
        try:
            reviews.append(result.find('span', {'class': 'sds-rating__link'}).get_text())
        except:
            reviews.append('0')

        # price
        try:
            price.append(result.find('span', {'class': 'primary-price'}).get_text())
        except:
            price.append('n/a')

# Panda Dataframe
car_dealer = pd.DataFrame({'Name': name, 'Price': price, 'Mileage': mileage, 'Rating': rating, 'Reviews': reviews, 'Dealer': dealer})

car_dealer[['Year', 'Brand', 'Type']] = car_dealer['Name'].apply(extract_info).apply(pd.Series)

# Drop the original 'Name' column if needed
car_dealer = car_dealer.drop('Name', axis=1)

# Reorder columns for clarity if needed
car_dealer = car_dealer[['Year', 'Brand', 'Type', 'Price', 'Mileage', 'Rating', 'Reviews', 'Dealer']]
print(car_dealer)

# Data cleaning
car_dealer['Mileage'] = car_dealer['Mileage'].str.replace(',', '').str.replace(' mi.', '').astype(float)
car_dealer['Rating'] = car_dealer['Rating'].astype(float)
car_dealer['Reviews'] = car_dealer['Reviews'].str.replace(',', '').str.replace(' reviews)', '').str.replace(' review)', '').str.replace('(', '').astype(int)
car_dealer['Price'] = car_dealer['Price'].str.replace(',', '').str.replace('$', '').astype(int) * 100

# Output in Excel
car_dealer.to_excel('single_page_car.xlsx', index=False)