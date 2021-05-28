import sys
import time
import os
import random
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def banner():
    print("-[~]-  INSTABOT v1 by Serpent  -[~]-")
    print("    https://github.com/serpent33")
    print("#" * 36)
    print("")


class bot():

    def __init__(self,usr,pw):
        
        # USERNAME n PASSWORD
        self.user = usr
        self.pswd = pw

        # OPTIONS
        self.opt = webdriver.FirefoxOptions()

        self.opt.add_argument("--window-size=1440, 900")
        self.opt.add_argument("--headless") #Headless
        
        # DRIVER
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options= self.opt)

    # WAIT FOR OBJECT
    def WaitForObject(self, type, string):
        return WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((type, string)))

    def WaitForObjects(self, type, string):
        return WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((type, string)))

    # LOGIN
    def login(self):

        self.driver.get("https://instagram.com/")
        print("[~] Page loaded [~]")

        self.WaitForObject(By.XPATH, "/html/body/div[2]/div/div/button[1]").click()  # Accept Cookies
        print("[~] Cookies Accepted [~]")

        time.sleep(1)

        objects = self.WaitForObjects(By.CSS_SELECTOR, "input._2hvTZ.pexuQ.zyHYP")  # Put Username and Password in Input
        objects[0].send_keys(self.user)
        objects[1].send_keys(self.pswd)
        objects[1].send_keys(Keys.ENTER)

        time.sleep(random.randint(4, 6))
        
        self.WaitForObject(By.CSS_SELECTOR, "button.sqdOP.yWX7d.y3zKF").click()  # Disable Safe Login Data
        
        time.sleep(random.randint(2, 3))

        try:
            self.WaitForObject(By.CSS_SELECTOR, "button.aOOlW.HoLwm").click()  # Disable Notifications
        except Exception as e:
            print("Error: Cant login")
            self.driver.quit()
            sys.exit()

        print("[~] Bot logged in [~]")


    def pictureaction(self,hashtag):

        self.driver.get(f"https://instagram.com/explore/tags/{hashtag}/")
        print(f"[~] Opened Hashtag : {hashtag} [~]")

        self.driver.execute_script("window.scrollTo(0, 4000)") # Load more Pics
        
        pictures = self.WaitForObjects(By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")
        print(f"[~] Collected {str(len(pictures))} Pictures [~]")
        self.logcountpics = 0

        for pic in pictures:

            self.schalter = False
            pic.click()
            try:
                self.WaitForObject(By.CSS_SELECTOR, "[aria-label='Like']").click() # Like
                self.schalter = True

            except Exception as e:
                self.WaitForObject(By.CSS_SELECTOR, "[aria-label='Close']").click() # Close

            if self.schalter == True:
                self.WaitForObject(By.CSS_SELECTOR, "[aria-label='Close']").click() # Close

            self.logcountpics += 1
            print(f"Liked [{str(self.logcountpics)}/{str(len(pictures))}]")







if __name__ == "__main__":
    banner()
    os.environ['WDM_LOG_LEVEL'] = '0'
    

    # GET USERNAME AND PASSWORD
    try:
        username = str(sys.argv[1])
        password = str(sys.argv[2])
        hashtag  = str(sys.argv[3])
    
    except Exception as e:
        if str(e) == "list index out of range":
            print("Error: Missing Arguments [python3 bot.py username password hashtag]")
        else:
            print("Error: " + str(e))

        sys.exit()

    bot = bot(username,password)

    # LOGIN 
    bot.login()

    # START 
    bot.pictureaction(hashtag=hashtag)

