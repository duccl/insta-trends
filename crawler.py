from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

class Crawler:
    EXPLORE_URL = "https://www.instagram.com/explore/"
    def __init__(self,url,chromedriver):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        self.driver= webdriver.Chrome(chromedriver,options = options)
        self.driver.get(url)
        self.tag_counter = {}

    def log(self,message):
        print(f'[NOW] || {message}')

    def wait_for_element(self,by,selector):
        try:
            element = WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((by,selector)))
            return
        except Exception as e:
            self.driver.quit()
    def login(self,user,password):
        self.wait_for_element(By.CSS_SELECTOR,'input')
        username_field,password_field = self.driver.find_elements_by_tag_name('input')
        username_field.send_keys(user)
        password_field.send_keys(password)
        submit_button = self.driver.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()
        self.sleep()
        self.wait_for_element(By.CSS_SELECTOR,f'a[href="/{user}/"]')
        self.sleep()

    def sleep(self,time_in_seconds = 0.5):
        time.sleep(time_in_seconds)

    def go_to_explore(self):
        self.driver.get(self.EXPLORE_URL)

    def update_tag_count(self,tag_name):
        if tag_name in self.tag_counter:
            self.tag_counter[tag_name] += 1
        else:
            self.tag_counter[tag_name] = 1

    def access_first_post(self):
        self.wait_for_element(By.CSS_SELECTOR,'a[href*="p"]')
        self.wait_for_element(By.CSS_SELECTOR,'img[decoding]')
        self.sleep()
        post = self.driver.find_element_by_css_selector('a[href*="p"]')
        post.click()
        self.wait_for_element(By.CSS_SELECTOR,'article')
        
    def list_tags(self):
        self.wait_for_element(By.CSS_SELECTOR,"h2 + span")
        self.sleep()
        tags_elements = self.driver.find_elements_by_css_selector("h2 + span > a[href*='explore/tags/']")
        for tag in tags_elements:
            self.update_tag_count(tag.text)

    def paginate(self):
        self.wait_for_element(By.CSS_SELECTOR,'a[class*="coreSpriteRightPaginationArrow"]')
        right_paginator = self.driver.find_element_by_css_selector('a[class*="coreSpriteRightPaginationArrow"]')
        right_paginator.click()
        self.wait_for_element(By.CSS_SELECTOR,'article')

    def export_data(self):
        with open('data.json','w') as file:
            json.dump(self.tag_counter,file,ensure_ascii=False,indent = 3)
                
        
