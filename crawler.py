from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import os
class Crawler:
    EXPLORE_URL = "https://www.instagram.com/explore/"
    def __init__(self,url,chromedriver):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--enable-logging')
        options.add_argument('--log-level=0')
        options.add_argument('--v=99')
        options.add_argument('--single-process')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument(
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.30 Safari/537.36')
        options.binary_location = os.getcwd() + "/bin/headless-chromium" 
        self.driver= webdriver.Chrome(executable_path=chromedriver,chrome_options = options)
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
            print(e)
            return
    def login(self,user,password):
        self.wait_for_element(By.CSS_SELECTOR,'input')
        self.log("login")
        username_field,password_field = self.driver.find_elements_by_tag_name('input')
        username_field.send_keys(user)
        password_field.send_keys(password)
        self.log("login done")
        submit_button = self.driver.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()
        self.log("submit done")
        self.sleep()
        self.log("waiting load")
        self.wait_for_element(By.CSS_SELECTOR,f'a[href="/{user}/"]')
        self.log("waiting load done")
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
        self.log("waiting post")
        self.wait_for_element(By.CSS_SELECTOR,'a[href*="p"]')
        self.log("waiting post done")
        self.log("waiting img")
        self.wait_for_element(By.CSS_SELECTOR,'img[decoding]')
        self.log("waiting img done")
        self.sleep()
        post = self.driver.find_element_by_css_selector('a[href*="p"]')
        self.log(post)
        post.click()
        self.log("post click done")
        self.log("post wait load")
        self.wait_for_element(By.CSS_SELECTOR,'article')
        self.log("post wait load done")
        
    def list_tags(self):
        self.log("list tags wait")
        self.wait_for_element(By.CSS_SELECTOR,"h2 + span")
        self.log("list tags wait done")
        self.sleep()
        tags_elements = self.driver.find_elements_by_css_selector("h2 + span > a[href*='explore/tags/']")
        self.log("list tags begin")
        for tag in tags_elements:
            self.update_tag_count(tag.text)
            self.log("list tag "+tag.text)

    def paginate(self):
        self.log("wait paginator")
        self.wait_for_element(By.CSS_SELECTOR,'a[class*="coreSpriteRightPaginationArrow"]')
        self.log("wait paginator done")
        right_paginator = self.driver.find_element_by_css_selector('a[class*="coreSpriteRightPaginationArrow"]')
        right_paginator.click()
        self.log("go paginator")
        self.log("wait article")
        self.wait_for_element(By.CSS_SELECTOR,'article')
        self.log("wait article done")

    def export_data(self):
        with open('data.json','w',encoding='utf-8') as file:
            json.dump(self.tag_counter,file,ensure_ascii=False,indent = 3)
                
        
