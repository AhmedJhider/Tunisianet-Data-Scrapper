import requests
from bs4 import BeautifulSoup
import pandas

class Datasheet():
    
    def __init__(self,url):
        self.url = url
        self.soup = self.get_soup(self.url)
        self.nbPages = self.get_nbPages()
        self.nbProducts = self.get_nbProducts()
        self.listProducts = []
        self.listBrands = []
        self.fill_listProducts()
        self.listBrandsAmounts = []
        self.fill_listBrandsAmounts()
    
    def exportCsv(self):
        data = pandas.DataFrame(self.listProducts)
        file_name=f"C:/{self.url[34:]}.csv"
        data.to_csv(file_name,index=False,header=False)

    def get_soup(self,url):
        response = requests.get(url)
        html = response.text
        return BeautifulSoup(html,"html.parser")

    def get_nbPages(self):
        allPages = self.soup.find_all("a",class_="js-search-link")
        return int(allPages[-2].string)

    def get_nbProducts(self):
        searchResults = self.soup.find("div",class_="col-md-6 col-sm-6 col-xs-6 text-xs-left")
        return int(searchResults.string[searchResults.string.find("de ")+3:searchResults.string.find("article")])

    def fill_listProducts(self):
        self.listProducts = [["Title","Brand","Dispo","Price"]]
        for i in range (1,self.nbPages+1):
            print(f"----{i}/{self.nbPages}----")
            soup = self.get_soup(self.url+f"?page={i}&order=product.price.asc")
            productTitles = soup.find_all("h2",class_="h3 product-title")
            productInfos = soup.find_all("div",class_="wb-action-block col-lg-2 col-xl-2 col-md-2 col-sm-2 col-xs-12")
            for productInfo,productTitle in zip(productInfos,productTitles):
                productTitle = productTitle.string
                productPrice = int(productInfo.find("span",class_="price").string.replace(" DT","").replace(f"{chr(160)}","").replace(",",""))//1000
                productDispo = productInfo.find("div",id="stock_availability").find("span").string
                productBrand = productInfo.find("img",class_="img img-thumbnail manufacturer-logo").get("alt")
                self.listProducts.append([productTitle,productBrand,productDispo,productPrice])
                
    def fill_listBrandsAmounts(self):
        BrandsAmounts = self.soup.find("div",{"data-url":"fabricants"})
        for BrandAmount in BrandsAmounts.find_all("li"):
            if len(BrandAmount.get('class'))==1:
                self.listBrands.append(BrandAmount.find("span",class_="name").string)
                self.listBrandsAmounts.append([BrandAmount.find("span",class_="name").string,int(BrandAmount.find("span",class_="count").string)])

    def get_listProducts(self):
        return self.listProducts

    def get_listBrands(self):
        return self.listBrands
    
    def get_listBrandsAmounts(self):
        return self.listBrandsAmounts
