import json
import math
import gzip
import os, sys
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import re

def read_json(file,platform):
    data = []
    id_list = []
    try:
        with open(file,'r',encoding = 'utf-8') as f:
            for index,line in enumerate(f):
                try:
                    if line.strip():
                        if platform == 'youtube_comment':
                            ori_data = json.loads(line)
                            
                            if ori_data['link'] not in set(id_list):
                                id_list.append(ori_data['link'])
                                data.append(ori_data)

                        if platform == 'instagram_comment':
                            ori_data = json.loads(line)
                            
                            if ori_data['shortcode'] not in set(id_list):
                                id_list.append(ori_data['shortcode'])
                                data.append(ori_data)
                                
                except Exception as e:
                    print(e)
                    print("can't open line "+str(index))
    except Exception as e:
        print(e)
        with open(file,'r',encoding = 'utf-16') as f:
            for index,line in enumerate(f):
                try:
                    if line.strip():
                        if platform == 'youtube_comment':
                            ori_data = json.loads(line)
                            
                            if ori_data['link'] not in set(id_list):
                                id_list.append(ori_data['link'])
                                data.append(ori_data)

                        if platform == 'instagram_comment':
                            ori_data = json.loads(line)
                            
                            if ori_data['shortcode'] not in set(id_list):
                                id_list.append(ori_data['shortcode'])
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

############write result to json file
def write_json(instagram_list,json_file):
    try:
        target_file = open(json_file + '.json', 'w', encoding = 'utf-16')
        for ins in instagram_list:
            json.dump(ins, target_file)
            target_file.write('\n')
        target_file.close()
    except Exception as e:
        print(e)
        print("can't open file " + json_file)

if __name__ == '__main__':
    json_path = sys.argv[1] ####the direcory of data .json folder
    target_path = sys.argv[2]  ####the direcory of the output .json 
    platform = sys.argv[3]
    
    read = 0
    data_list = []
    
    for index,filename in enumerate(sorted(os.listdir(json_path))):
        if filename[-5:] == '.json':
            data_list += read_json(json_path+filename,platform)
        else:
            json_file = json_path + filename + '/'
            data_list += read_folder(json_file,platform)

    print(len(data_list))
    write_json(data_list,target_path)