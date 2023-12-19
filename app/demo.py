# ### Imports
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Pagination
name = []
mileage = []
dealer = []
rating = []
reviews = []
price = []

for i in range(1,11):
    # Website in variable
    website = 'https://www.cars.com/shopping/results/?makes[]=mercedes_benz&maximum_distance=all&models[]=&page=' + str(i) + '&stock_type=cpo&zip='

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
            mileage.append('n/a')

        # dealer
        try:
            dealer.append(result.find('div', {'class': 'dealer-name'}).get_text().strip())
        except:
            dealer.append('n/a')

        # rating
        try:
            rating.append(result.find('span', {'class': 'sds-rating__count'}).get_text())
        except:
            rating.append('n/a')

        # reviews
        try:
            reviews.append(result.find('span', {'class': 'sds-rating__link'}).get_text())
        except:
            reviews.append('n/a')

        # price
        try:
            price.append(result.find('span', {'class': 'primary-price'}).get_text())
        except:
            price.append('n/a')

# Panda Dataframe
car_dealer = pd.DataFrame({'Name': name, 'Price': price, 'Mileage': mileage, 'Rating': rating, 'Reviews': reviews, 'Dealer': dealer})
print(car_dealer)

# Data cleaning
car_dealer['Reviews'] = car_dealer['Reviews'].apply(lambda x: x.strip('reviews)').strip('('))
car_dealer['Mileage'] = car_dealer['Mileage'].apply(lambda x: x.strip('mi.'))

# Output in Excel
car_dealer.to_excel('single_page_car.xlsx', index=False)
