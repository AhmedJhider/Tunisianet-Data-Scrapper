from datasheet import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def countbrands(listBrandsAmounts):
    listBrandsAmounts.sort(key=lambda x:x[1],reverse=True)
    listBrands = [brand[0] for brand in listBrandsAmounts]
    listAmounts = [brand[1] for brand in listBrandsAmounts]

    x1 = plt.subplot(221)
    x1.bar(listBrands, listAmounts)
    plt.xticks(rotation=45,ha="right")
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

    x1.set_title('Number of products by brand') 
    plt.tight_layout()
    # plt.show()

def pricebrands(listBrands,listProducts):
    allPrices=[]
    for brand in listBrands:
        brandPrices=[]
        for product in listProducts:
            if brand == product[1]:
                brandPrices.append(int(product[3]))
        allPrices.append(brandPrices)
    x2 = plt.subplot(222)
    x2.boxplot(allPrices)
    plt.xticks(ticks=list(range(1,len(listBrands)+1)), labels=listBrands)
    
    plt.gca().ticklabel_format(style='plain', axis='y')
    x2.set_title("Price distribution")
    plt.xticks(rotation=45,ha="right")
    plt.tight_layout()
    # plt.show()

def manprices(listBrands,listProducts,x):
    allPrices=[]
    x3 = plt.subplot(220+2+x)
    for brand in listBrands:
        brandPrices=[]
        for product in listProducts:
            if brand == product[1]:
                brandPrices.append(int(product[3]))
        if x == 1:
            allPrices.append(max(brandPrices))
            x3.set_title('Most expensive product by brand') 
        elif x == 2:
            allPrices.append(min(brandPrices))
            x3.set_title('Cheapest product by brand') 
        else:
            allPrices.append(sum(brandPrices)/len(brandPrices))
            x3.set_title('Average price of product by brand') 
    x3.bar(listBrands, allPrices)
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    plt.xticks(rotation=45,ha="right")
    plt.tight_layout()
    # plt.show()
    if x== 2:
        plt.show()

plt.rcParams['toolbar'] = 'None'
plt.figure(figsize=(12, 7),num='Analysis')
plt.suptitle("Product Analysis")
url = input("Give url: ")
data = Datasheet(url)
countbrands(data.get_listBrandsAmounts())
pricebrands(data.get_listBrands(),data.get_listProducts())
manprices(data.get_listBrands(),data.get_listProducts(),1)
manprices(data.get_listBrands(),data.get_listProducts(),2)
# manprices(data.get_listBrands(),data.get_listProducts(),3)