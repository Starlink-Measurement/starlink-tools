import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd
import argparse

def main(args):
    options = webdriver.ChromeOptions()

    # Using the local chrome configuration, because chrome does not allow you to login in a "program controlled browser".
    # So to play under a premium account, you need to login in your google account in your local chrome
    options.add_argument("user-data-dir=c:/Users/19217/AppData/Local/Google/Chrome/User Data/")
    driver = webdriver.Chrome(executable_path="C:/Program Files/Google/Chrome/chromedriver_win32/chromedriver.exe", options = options)
    driver.get("https://www.youtube.com/watch?v=KcMlPl9jArM")

    # open the stats of nerd and switch to the appropriate resolution. 
    input("Press any key when you ready. Ensure you login a premium account to avoid Ads!!!")

    buffer_health = driver.find_element(By.XPATH, """//*[@id="movie_player"]/div[@class="html5-video-info-panel"]/div/div[11]/span/span[2]""")
    connection_speed = driver.find_element(By.XPATH, """//*[@id="movie_player"]/div[@class="html5-video-info-panel"]/div/div[9]/span/span[2]""")
    network_activity = driver.find_element(By.XPATH, """//*[@id="movie_player"]/div[@class="html5-video-info-panel"]/div/div[10]/span/span[2]""")

    time_list = []
    bh_list = []
    cs_list = []
    na_list = []

    curr_time = time.time()

    # record the end time
    end_timestamp = curr_time + int(args.time)

    while time.time() < end_timestamp:
        while time.time() > curr_time + 1:
            curr_time = time.time()
            time_list.append(str(time.time()))
            bh_list.append(str(buffer_health.get_attribute("innerHTML")))
            cs_list.append(str(connection_speed.get_attribute("innerHTML")))
            na_list.append(str(network_activity.get_attribute("innerHTML")))
            print(time_list[-1] + ", " + cs_list[-1] + ", " + na_list[-1] + ", " + bh_list[-1])

    driver.close()
    df = pd.DataFrame({'timestamp': time_list,
                    'connection speed': cs_list,
                    'network activity': na_list,
                    'buffer health': bh_list})

    df.to_csv(args.name, index = False)

    if args.shutdown == "1":
        os.system("shutdown -s")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Scrape YouTube stats of nerd data to csv file.")
    parser.add_argument('-n', '--name', default='Streaming_data.csv', help='the file name for the output csv file.')
    parser.add_argument('-t', '--time', default='60', help='record time period (in seconds).')
    parser.add_argument('-s', '--shutdown', default='0', help='shutdown after task finish (1/0)')
    args = parser.parse_args()
    main(args)
