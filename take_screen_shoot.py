import requests
import json
import urllib
import io
import os
import re
import random
import time
import sys
import pymongo
from urllib.request import urlopen
import numpy as np


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def read_json(file,platform):
    data = []
    try:
        with open(file,'r',encoding = 'utf-8') as f:
            for index,line in enumerate(f):
                ori_data = json.loads(line)
                try:
                    if line.strip():
                        if platform == 'youtube':
                        #####clean the original json file
                            if 'link' in ori_data:
                                ori_data['id'] = ori_data['link'].split('=')[-1]
                                data.append(ori_data)
 
                        if platform == 'instagram':
                        #####clean the original json file
                            link = 'https://www.instagram.com/p/'+ori_data['shortcode']
                            ori_data['link'] = link
                            data.append(ori_data)
                        
                        if platform == 'twitter':
                        #####clean the original json file
                            try:
                                link = 'https://twitter.com/' + ori_data['screen_name'] + '/status/' + ori_data['pid']
                                ori_data['link'] = link
                                ori_data['id'] = ori_data['pid']
                                data.append(ori_data)
                            except:
                                link = 'https://twitter.com/' + ori_data['user']['screen_name'] + '/status/' + ori_data['id_str']
                                ori_data['link'] = link
                                ori_data['id'] = ori_data['id_str']
                                data.append(ori_data)
                            

                        if platform == 'tumblr':
                        #####clean the original json file 
                            link = 'https://' + ori_data['screen_name'] + '.tumblr.com/post/' + str(ori_data['pid'])
                            ori_data['link'] = link
                            ori_data['id'] = ori_data['pid']
                            data.append(ori_data)

                except Exception as e:
                    print(e)
                    print("can't open line "+str(index))
    except Exception as e:
        print(e)
        with open(file,'r',encoding = 'utf-16') as f:
            for index,line in enumerate(f):
                ori_data = json.loads(line)
                try:
                    if line.strip():
                        if platform == 'youtube':
                        #####clean the original json file
                            if 'link' in ori_data:
                                ori_data['id'] = ori_data['link'].split('=')[-1]
                                data.append(ori_data)
 
                        if platform == 'instagram':
                        #####clean the original json file
                            link = 'https://www.instagram.com/p/'+ori_data['shortcode']
                            ori_data['link'] = link
                            data.append(ori_data)
                        
                        if platform == 'twitter':
                        #####clean the original json file
                            try:
                                link = 'https://twitter.com/' + ori_data['screen_name'] + '/status/' + ori_data['pid']
                                ori_data['link'] = link
                                ori_data['id'] = ori_data['pid']
                                data.append(ori_data)
                            except:
                                link = 'https://twitter.com/' + ori_data['user']['screen_name'] + '/status/' + ori_data['id_str']
                                ori_data['link'] = link
                                ori_data['id'] = ori_data['id_str']
                                data.append(ori_data)
                            

                        if platform == 'tumblr':
                        #####clean the original json file 
                            link = 'https://' + ori_data['screen_name'] + '.tumblr.com/post/' + str(ori_data['pid'])
                            ori_data['link'] = link
                            ori_data['id'] = ori_data['pid']
                            data.append(ori_data)

                except Exception as e:
                    print(e)
                    print("can't open line "+str(index))
    return data

###########used to go through the folder, and collect the tweet data
###########it will return the list of tweets in all files in the folder
def read_folder(path,platform):
    data = []
    read = 0
    for filename in sorted(os.listdir(path)):
        print('Read '+path+filename)
        d = read_json(path+filename,platform)
        data.extend(d)
    return data

def init_drive(driver_path):
    opts = Options()
    #opts.binary_location = driver_path
    opts.add_argument("user_agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.20 Safari/537.36")
    opts.add_argument("--disable-notifications")
    opts.add_argument('--headless')
    #opts.add_argument("--window-size=720,1080")
    opts.add_argument("--lang=en")
    opts.add_argument('--no-sandbox')
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument('disable_infobars')
    drive = webdriver.Chrome(driver_path, options=opts)
    return drive


if __name__ == '__main__':
    #json_path = sys.argv[1] ####the direcory of data .json folder
    #target_path = sys.argv[1]  ####the direcory of the output .json 
    #platform = sys.argv[3]
    target_path = '/data1/screen_shot/'
    drug_type = '/opioids/'
    platforms = ['instagram','tumblr','youtube','twitter']

    if not os.path.exists(target_path):
        os.mkdir(target_path)
    
    data_list = []
    driver_path = '/usr/lib/chromium-browser/chromedriver'

    ######get screen shot
    driver = init_drive(driver_path)

    for platform in platforms:
        json_path = '/data1/data/' + platform + '/data' + drug_type
        for index,filename in enumerate(sorted(os.listdir(json_path))):
            #########record teh data with link
            if filename[-5:] == '.json':
                data_list += read_json(json_path+filename,platform)
            else:
                json_file = json_path + filename + '/'
                data_list += read_folder(json_file,platform)
            for d in data_list:
                if 'link' not in d:
                    continue
                link = d['link']
     
                if platform == 'instagram':
                    pid = d['shortcode']
                else:
                    pid = d['id']
               
                #######create first layer folder
                output_path = target_path + platform  
                if not os.path.exists(output_path):
                    print("Create path " + output_path)
                    os.mkdir(output_path)

                #######create second layer folder
                output_path = target_path + platform + drug_type 
                if not os.path.exists(output_path):
                    print("Create path " + output_path)
                    os.mkdir(output_path)

                #######test whetehr the screen shot exist
                output_path = output_path + str(pid) +'.png'
                if os.path.exists(output_path):
                    continue

                print("Save screen shot "+ output_path)
                driver.get(link)
                time.sleep(1)
                driver.save_screenshot(output_path)
