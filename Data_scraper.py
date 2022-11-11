from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep,time
from webdriver_manager.chrome import ChromeDriverManager

import csv
import json
import os
import pandas as pd
import requests
import uuid

class Scraper():
    """ 
    This class is used to scrape data from a website.
    
    Attributes:
    driver: webdriver 
    URL(str) : The source of the scraped data
    webpage_link_list(list): List of product page URLs
    data_list (list): list of dictionaries which contain all the scraped information for each product page
    page_titles (list): list of product pages
    page_idx(int) : This is used to iterate when creating the folders for the image sub-folders.
    
    """
    def __init__(self,URL):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options= self.__generate_options())
        self.URL = ("https://www.myprotein.com/")
        self.homepage_links =[]
        self.data_list = []
        self.page_titles =[] 
        self.page_idx=0
        
    def __generate_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('no-sandbox') 
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("disable-dev-shm-usage")
        return chrome_options
    
    def navigate(self,xpath =  '//a[@class="responsiveFlyoutMenu_levelOneLink responsiveFlyoutMenu_levelOneLink-hasChildren"]'):
        """This function navigates through the homepage to each individual section. It also collects the titles of each section"""
        click_drop_down = self.driver.find_elements(By.XPATH, xpath)
        for links in click_drop_down[0:5]:
            title = links.get_attribute("data-context")
            drop_down_link = links.get_attribute("href")
            self.homepage_links.append(drop_down_link)
            self.page_titles.append(title)
        self.image_folder()
        
    def scroll(self):
        """This function locates the product pages and then collects the URL of each page."""
        try:
            try:
                view_all_redirect = self.driver.find_element(By.XPATH, '//*[@class="sectionPeek_allCta"]').get_attribute("href")
                self.driver.get(view_all_redirect)
            except Exception:
                view_all_redirect2 = self.driver.find_element(By.XPATH,'//*[@class="sectionPeek_allCta sectionPeek_allCta-show"]').get_attribute("href")
                self.driver.get(view_all_redirect2)
        except Exception as e: 
            print(e)
        sleep(1)
        
    def product_page_scraper(self):
        """This navigates the website 5 times for each section, collecting their product page URL and then creating an image folder."""
        self.driver.find_element( By.CLASS_NAME, 'emailReengagement_close_button').click()
        self.navigate()
        for link in range (len(self.homepage_links)):
            self.driver.get(self.homepage_links[link])
            self.scroll()
            self.image_downloader()
            page_dict = self.scrape()
            self.data_list.append(page_dict)
            self.page_idx +=1
        print(self.page_titles)
    
    def product_image(self):
        """This collects all the src tags for all the images on the product page.All of this information is then added to a list"""
        image_src = []
        image = self.driver.find_elements(By.XPATH, '//*[@data-track="product-image"]')    
        for element in image:
            image_src.append(element.get_attribute("src"))
        return image_src
        


    def product_info(self):
        """This collects all the relevent information for every product on the produuct page. This includes the ProductID, Name and price. 
        All of this information is then added to a dictionary. Each item in the dictionary has a UUID as the key"""
        product_id = self.driver.find_elements(By.XPATH, '//*[@class="js-enhanced-ecommerce-data athenaProductBlock_hiddenElement"]')
        data_dict = {}
        for element in product_id:
            data_dict.setdefault(str(uuid.uuid4()),[element.get_attribute("data-product-id"),
                                                    element.get_attribute("data-product-title"),
                                                    element.get_attribute("data-product-price")])
        return data_dict
    
    
    def scrape(self):
        """This function appends the dictionary created in the product_info method with the 
        list of src tags created in the product_image method"""
        idx=0
        fill_image_src=self.product_image()
        attribute_dict = self.product_info()
        for key,value in attribute_dict.items():
            value.append(fill_image_src[idx])
            attribute_dict[key] = value
            idx +=1
        return attribute_dict
    
    def json_file_save(self):
        """This method creates a json file for the data that collected across the 5 product pages. It is located in the folder raw_data"""
        with open("data.json", "w") as f:
            json.dump(self.data_list,f)
        json_file = "data.json"
        destination = "/raw_data/data.json"
        
        try:
            os.replace(json_file,destination)
        except FileNotFoundError:
            print(json_file+"was not found")
        
     
    def image_downloader(self):
        """
        This function extracts the src links from the dictionary and downloads the images.
        After the images are downloaded the images are then moved to the appropriate folder
        which corresponds to their category.
        """
        info = self.scrape()
        for key,value in info.items():
            product_id = value[0]
            product_name = value[1]
            image = value[3]
        #     bucket_names = str("nadirsmyprotien" + str(self.page_titles[self.page_idx].lower().replace(",","-").replace("&", "and").replace(" ","-")))
        #     try:
        #         try:
        #             bucket = self.s3.create_bucket(Bucket=bucket_names,CreateBucketConfiguration={
        # 'LocationConstraint': 'eu-west-2',})
        #         except:
        #             bucket = bucket_names
        #     except Exception as e:
        #         print(e)
    
            with open(product_name.replace(" ", "_").replace(":","-")[:12] +"-" + product_id + ".jpg", "wb") as f:
                # Here the file name is created according to the product name and ID. 
                im = requests.get(image)
                f.write(im.content)
            image_file = str("{0}-{1}.jpg".format(product_name.replace(" ", "_").replace(":","-")[:12], product_id))
            destination = str("/images/{0}/{1}".format(self.page_titles[self.page_idx],image_file))
            try:
                os.replace(image_file,destination)
                #self.s3.upload_file(destination, str(bucket), image_file)

            except FileNotFoundError:
                print(image_file+" was not found")
            

    def image_folder(self):
        """ 
        This function creates the image folders for each product page. 
        The list of page titles that was appended in the navigate function are used to do this.
        All of these pages are located within the parent folder images
        """
        for page in range (len(self.page_titles)):
            directory = self.page_titles[page]
            parent_direct = '/images'
            path = os.path.join(parent_direct,directory)
            try:
                os.mkdir(path)
            except OSError as error:
                print(error)
                
    def format_data(self):
        file= open ("/raw_data/data.json")
        raw_data = json.load(file)
        df = pd.DataFrame.from_dict(raw_data[0], orient ="index" ,columns = ["Product ID" , "Product Name", "Price", "Image Link"]) 
        df.to_csv( "/raw_data/formatted_data.csv", mode= "w" , header = True, index=True )
        
        for i in range (1, len(raw_data)):
            df = pd.DataFrame.from_dict(raw_data[i], orient= "index", columns = ["Product ID" , "Product Name", "Price", "Image Link"]) 
            df.to_csv( "/raw_data/formatted_data.csv", mode= "a" , header = False, index=True )
            print(df)
            i +=1
            
        file2 = pd.read_csv( "/raw_data/formatted_data.csv")
        duplicates = file2[file2.duplicated(subset=["Product ID"])]
        print(duplicates)
        file2.drop_duplicates(subset = ["Product ID"], keep = "first")
        file2.to_csv( "/raw_data/formatted_data.csv", index=True)

def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args,**kwargs)
        t2 = time()
        print(f"time taken = {t2-t1} ms")
        return result
    return wrapper   
@timer             
def website(URL):
    """ 
    This is the overall functionality of the program.
    - Firstly the Website URL is obtained
    - Next the homepage is navigated until the url of all the product pages is collected.
    - After that all the images from that page are downloaded and stored in their appropriate folders
    - Then all the relevant information is scraped from that product page and stored in a dictionary.
    - And then this is added to a data list after which the process is repeated for the other 4 product 
      pages.   
    - Finally the data dictionary is printed and the saved as a json file.
    """
    MyProtein = Scraper(URL)
    MyProtein.driver.get(MyProtein.URL)
    sleep(2)
    MyProtein.product_page_scraper()
    print(MyProtein.data_list)
    MyProtein.json_file_save()
    MyProtein.format_data()
    MyProtein.driver.quit()
    
def make_dir():
    """ 
    This function creates 2 folders. 1 for the raw data and the other for the images.    
    """
    folders = ["raw_data","images"]
    for dir in range (len(folders)):
        directory = folders[dir]
        parent_direct = '/'
        path = os.path.join(parent_direct,directory)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

                            
if __name__ == "__main__":
    URL= ("https://www.myprotein.com/")
    make_dir()
    website(URL)