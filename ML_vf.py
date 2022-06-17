import requests
from bs4 import BeautifulSoup
import pandas as pd

url_base = 'https://lista.mercadolivre.com.br/'

product_name = input('Tell us the product you want') #The exercise chose "Mi band 5"

response = requests.get(url_base + product_name)

site = BeautifulSoup(response.text, 'html.parser')

products = site.findAll('div', attrs={'class':'andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default'})

products_list = []

for product in products:
    title_product = product.find('h2', attrs={'class': 'ui-search-item__title'})
    link = product.find('a', attrs={'class':'ui-search-link'})

    real = product.find('span', attrs={'class':'price-tag-fraction'})
    cents = product.find('span', attrs={'class':'price-tag-cents'})

    if (cents):
        products_list.append([title_product.text, link['href'], real.text, cents.text])
    else:
        products_list.append([title_product.text, link['href'], real.text, '00']) #I included 00 in order to fill Nul values, this should be the cents

    #print('\n\n')


#generate Dataframe (Columns)
products = pd.DataFrame(products_list, columns=['title_product', 'Link', 'Real', 'Cents'])

#Creating a Column Price
products['Price'] = products['Real'] + ',' + products['Cents']

#Drop the previous columns related to price
products.drop("Real", axis=1, inplace=True)
products.drop("Cents", axis=1, inplace=True)


#generate csv
products.to_csv('mlivre_vf.csv', index=False)

#read csv
df_prod = pd.read_csv('mlivre_vf.csv')