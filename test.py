from Data_scraper import Website,Scraper,make_dir
from time import time 

def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args,**kwargs)
        t2 = time()
        print(f"time taken = {t2-t1} ms")
        return result
    return wrapper   



URL= ("https://www.myprotein.com/")
make_dir()
timer(Website(URL))