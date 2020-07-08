from crawler import Crawler
import os
instaCrawler = Crawler('https://www.instagram.com/',".\\chromedriver.exe")
instaCrawler.login(os.envoiron['USERNAME'],os.envoiron['PASSWORD'])
instaCrawler.go_to_explore()
instaCrawler.access_first_post()
instaCrawler.list_tags()
instaCrawler.paginate()
instaCrawler.export_data()
