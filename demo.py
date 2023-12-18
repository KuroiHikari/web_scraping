# ### Imports
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

## HTTP Request
## store website in variable
# website = 'https://www.cars.com/shopping/results/?stock_type=cpo&makes%5B%5D=mercedes_benz&models%5B%5D=&list_price_max=&maximum_distance=20&zip='
# print("Website:", website)
#
# # Get Request
# response = requests.get(website)
#
# # Status Code
# print("Status code:", response.status_code)
#
# # Soup Object
# soup = BeautifulSoup(response.content, 'html.parser')
#
# # Results
# results = soup.find_all('div', {'class': 'vehicle-card'})
#
# # Length
# print("Length:", len(results))

# Target necessary data
# Name
# Mileage
# Dealer Name
# Rating
# Rating Count
# Price


# # Name
# name = results[0].find('h2')
# if name:
#     print("Name:", name.get_text())
# else:
#     print("Name: not available")
#
# # Mileage
# mileage = results[0].find('div', {'class': 'mileage'})
# if mileage:
#     print("Mileage:", mileage.get_text())
# else:
#     print("Mileage: not available")
#
# # Rating
# rating = results[0].find('span', {'class': 'sds-rating__count'})
# if rating:
#     print("Rating:", rating.get_text())
# else:
#     print("Rating: not available")
#
# # Review count
# review = results[0].find('span', {'class': 'sds-rating__link'})
# if review:
#     print("Reviews:", review.get_text())
# else:
#     print("Reviews: not available")
#
# # Price
# price = results[0].find('span', {'class': 'primary-price'})
# if price:
#     print("Price:", price.get_text())
# else:
#     print("Price: not available")
#
# # Dealer
# dealer = results[0].find('div', {'class': 'dealer-name'})
# if dealer:
#     print("Dealer:", dealer.get_text().strip())
# else:
#     print("Dealer: not available")



# # For Loop for all cars in 1 page
# name = []
# mileage = []
# dealer = []
# rating = []
# reviews = []
# price = []
#
# for result in results[1:]:
#     #name
#     try:
#         name.append(result.find('h2').get_text())
#     except:
#         name.append('n/a')
#
#     #mileage
#     try:
#         mileage.append(result.find('div', {'class': 'mileage'}).get_text())
#     except:
#         mileage.append('n/a')
#
#     #dealer
#     try:
#         dealer.append(result.find('div', {'class': 'dealer-name'}).get_text().strip())
#     except:
#         dealer.append('n/a')
#
#     #rating
#     try:
#         rating.append(result.find('span', {'class': 'sds-rating__count'}).get_text())
#     except:
#         rating.append('n/a')
#
#     #reviews
#     try:
#         reviews.append(result.find('span', {'class': 'sds-rating__link'}).get_text())
#     except:
#         reviews.append('n/a')
#
#     #price
#     try:
#         price.append(result.find('span', {'class': 'primary-price'}).get_text())
#     except:
#         price.append('n/a')

# Print out results
# print(name)
# print(price)
# print(mileage)
# print(rating)
# print(reviews)
# print(dealer)

# # Panda Dataframe
# car_dealer = pd.DataFrame({'Name': name, 'Price': price, 'Mileage': mileage, 'Rating': rating, 'Reviews': reviews, 'Dealer': dealer})
# print(car_dealer)
#
# # Data cleaning
# car_dealer['Reviews'] = car_dealer['Reviews'].apply(lambda x: x.strip('reviews)').strip('('))
# car_dealer['Mileage'] = car_dealer['Mileage'].apply(lambda x: x.strip('mi.'))
#
# # Output in Excel
# car_dealer.to_excel('single_page_car.xlsx', index=False)

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