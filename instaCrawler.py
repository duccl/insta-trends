from crawler import Crawler
import os

instaCrawler = Crawler('https://www.instagram.com/',".\\chromedriver.exe")
instaCrawler.login(os.getenv('USERNAME'),os.getenv('PASSWORD'))
instaCrawler.go_to_explore()
instaCrawler.access_first_post()
for i in range(5):
    instaCrawler.list_tags()
    instaCrawler.paginate()
instaCrawler.export_data()
