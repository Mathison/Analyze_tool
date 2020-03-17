import json
import math
import gzip
import os, sys
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import re
import collections

#####input keywords that need to be filtered
keywords = []

###########used to read a single json file, it will return a list of orginal tweet information
def read_json(file,platform):
    print('Read file ' + file)
    data = []
    try:
        with open(file,'r',encoding = 'utf-8') as f:
            for index,line in enumerate(f):
                
        
                try:
                    ori_data = json.loads(line)
                    if line.strip():
                        if platform == 'youtube_comment':
                        #####clean the original json file
                            comments = list(ori_data['comments'])
                            ori_data['comments'] = []
                            for com in comments:
                                if check(com['comment_text'],keywords): 
                                    ori_data['comment_result'] = com
                                    data.append(ori_data)
                          
                        if platform == 'youtube_description':
                        #####clean the original json file
                            if check(ori_data['description'],keywords): 
                                data.append(ori_data)

                        if platform == 'instagram_comment':
                        #####clean the original json file
                            comments = get_instagram_comments(ori_data)
                            ori_data['comments'] = []
                            ori_data['edge_media_preview_comment'] = []
                            ori_data['edge_media_to_parent_comment'] = []

                            for com in comments:
                                com_text = com['node']['text']
                                if check(com_text,keywords): 
                                    ori_data['comment_result'] = com['node']
                                    data.append(ori_data)

 
                        if platform == 'instagram_post':
                        #####clean the original json file
                            text = get_instagram_text(ori_data)
                            if check(text,keywords): 
                                data.append(ori_data)
                        
                        if platform == 'twitter':
                        #####clean the original json file
                            com_text = get_twitter_text(ori_data)
                            if check(com_text,keywords): 
                                data.append(ori_data)
                           
                        if platform == 'tumblr_comment':
                        #####clean the original json file
                            comments = ori_data['comments']
                            ori_data['comments'] = []
                            for com in comments:
                                if 'reply_text' in com:
                                    com_text = com['reply_text']
                                    if check(com_text,keywords): 
                                        ori_data['comment_result'] = com
                                        data.append(ori_data)

                        if platform == 'tumblr_post':
                        #####clean the original json file
                            if check(ori_data['text'],keywords): 
                                data.append(ori_data)

                        if platform == 'tumblr_description':
                        #####clean the original json file
                            if check(ori_data['description'],keywords): 
                                data.append(ori_data)

                        if platform == 'reddit_description':
                        #####clean the original json file
                            if 'post' not in ori_data:
                                continue
                            for p_key in ori_data['post']:
                                ori_data = ori_data['post'][p_key]
                            text = get_reddit_text(ori_data)
                            if check(text,keywords): 
                                data.append(ori_data)

                        if platform == 'reddit_comment':
                        #####clean the original json file
                            if 'comments' not in ori_data:
                                continue
                            comments_dict = dict(ori_data['comments'])
                            ori_data['comments'] = []
                            ori_data['comment_result'] = {}
                            for com_key in comments_dict:
                                ori_data['comment_result'] = comments_dict[com_key]
                                #print(comments_dict[com_key])
                                text = get_reddit_text(comments_dict[com_key])
                                if check(text,keywords):
                                    print(text) 
                                    data.append(ori_data)

                        if platform == 'reddit_title':
                        #####clean the original json file
                            for p_key in ori_data['post']:
                                ori_data = ori_data['post'][p_key]
                            text = ori_data['title']
                            print(text)
                            if check(text,keywords): 
                                data.append(ori_data)


                except Exception as e:
                    print(e)
                    #print(ori_data['post'])
                    #print(comments_dict[com_key])
                    print("can't open line "+str(index))
    except Exception as e:
        print(e)
        with open(file,'r',encoding = 'utf-16') as f:
            for index,line in enumerate(f):
                
                try:
                    ori_data = json.loads(line)
                    if line.strip():
                        if platform == 'youtube_comment':
                        #####clean the original json file
                            comments = list(ori_data['comments'])
                            ori_data['comments'] = []
                            for com in comments:
                                if check(com['comment_text'],keywords): 
                                    ori_data['comment_result'] = com
                                    data.append(ori_data)
                        
                        if platform == 'youtube_description':
                        #####clean the original json file
                            if check(ori_data['description'],keywords): 
                                data.append(ori_data)

                        if platform == 'instagram_comment':
                        #####clean the original json file
                            comments = get_instagram_comments(ori_data)
                            ori_data['comments'] = []
                            ori_data['edge_media_preview_comment'] = []
                            ori_data['edge_media_to_parent_comment'] = []
                            for com in comments:
                                com_text = com['node']['text']
                                if check(com_text,keywords): 
                                    ori_data['comment_result'] = com['node']
                                    data.append(ori_data)

                        if platform == 'instagram_post':
                        #####clean the original json file
                            text = get_instagram_text(ori_data)
                            if check(text,keywords): 
                                data.append(ori_data)


                        if platform == 'twitter':
                        #####clean the original json file
                            com_text = get_twitter_text(ori_data)
                            if check(com_text,keywords): 
                                data.append(ori_data)

                        if platform == 'tumblr_comment':
                        #####clean the original json file
                            comments = ori_data['comments']
                            ori_data['comments'] = []
                            for com in comments:
                                if 'reply_text' in com:
                                    com_text = com['reply_text']
                                    if check(com_text,keywords): 
                                        ori_data['comment_result'] = com
                                        data.append(ori_data)

                        if platform == 'tumblr_post':
                        #####clean the original json file
                            if check(ori_data['text'],keywords):
                                 data.append(ori_data)

                        if platform == 'tumblr_description':
                        #####clean the original json file
                            if check(ori_data['description'],keywords): 
                                 data.append(ori_data)

                        if platform == 'reddit_description':
                        #####clean the original json file
                            if 'post' not in ori_data:
                                continue
                            for p_key in ori_data['post']:
                                ori_data = ori_data['post'][p_key]
                            text = get_reddit_text(ori_data)
                            if check(text,keywords): 
                                data.append(ori_data)

                        if platform == 'reddit_comment':
                        #####clean the original json file
                            if 'comment' not in ori_data:
                                continue
                            comments_dict = dict(ori_data['comments'])
                            ori_data['comments'] = []
                            ori_data['comment_result'] = {}
                            for com_key in comments_dict:
                                ori_data['comment_result'] = comments_dict[com_key]
                                #print(comments_dict[com_key])
                                text = get_reddit_text(comments_dict[com_key])
                                if check(text,keywords): 
                                    data.append(ori_data)

                        if platform == 'reddit_title':
                        #####clean the original json file
                            for p_key in ori_data['post']:
                                ori_data = ori_data['post'][p_key]
                            text = ori_data['title']
                            print(text)
                            if check(text,keywords): 
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

def get_reddit_text(data):
    text = ''
    for content in data['media']['richtextContent']['document']:
        try:
            ###############fetch last layer
            con = dict(content)
            for c in con:
                if 'c' in con:
                    con = con['c'][0]
                else:
                    break
            ################

            if con['e'] == 'link':
                text = text + con['u'] + ' '
            else:
                text = text + con['t'] + ' '
        except Exception as e:
            #print(e)
            continue
    return text

def get_instagram_text(data):
    try:
        text = data['edge_media_to_caption']['edges'][0]['node']['text']
    except:
        text = ''
    return text

def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_twitter_text(data):
    flattern_data = flatten(data)
    try:
        text = data['full_text']
    except:
        text = data['text']
    for key in flattern_data:
        if key.split('.')[-1] == 'full_text':
            text = flattern_data[key]
    return text  

def get_instagram_comments(data):
    text_list = []
    try:
        comments_list = data['edge_media_to_comment']['edges']
    except:
        preview_num = 0
        parent_num = 0
        if 'edge_media_to_parent_comment' in data:
            #print('yes parent')
            parent_num = len(data['edge_media_to_parent_comment']['edges'])
        
        if 'edge_media_preview_comment' in data:
            #print('yes preview')
            preview_num = len(data['edge_media_preview_comment']['edges'])
        
        print(parent_num,preview_num)
        if parent_num >= preview_num:
            comments_list = data['edge_media_to_parent_comment']['edges']
        else:
            comments_list = data['edge_media_preview_comment']['edges']
    '''    
    for comment in comments_list:
        text_list.append(comment['node']['text'])
    '''
    return comments_list

def get_youtube_comments_text(data):
    data_list = []
    if len(data['comments']) != 0:
        for comment in data['comments']:
            data_list.append(comment['comment_text'])
    return data_list


def check(text,keywords):
    if check_key(text,keywords): #or check_link(text): # or check_phone(text):
        return True
    else:
        return False

################output the target tweets according to the topic result
def check_key(text,keywords):
    text = text.replace(':',' ')
    text = text.replace('/',' ')
    text = text.replace('#',' ')
    text = text.replace('@',' ')
    text = text.replace('$',' ')
    text = text.replace(',',' ')
    text = text.replace('.',' ')
    text = text.replace('&',' ')
    text = text.replace('(',' ')
    text = text.replace(')',' ')
    text = text.replace('"',' ')
    text = text.replace('-',' ')
    text_word = text.lower().split()
    if len(set(keywords) & set(text_word)) != 0:###the text contain keywords we need
        return True
    else:
        return False

def check_link(text):
    text = text.replace(':',' ')
    text = text.replace(',',' ')
    text = text.replace('.',' ')
    text = text.replace('&',' ')
    text = text.replace('(',' ')
    text = text.replace(')',' ')
    text = text.replace('"',' ')
    text = text.replace('-',' ')
    
    results = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',text)
    if len(results) != 0 or 'http' in text or 'www' in text:
        return True
    else:
        return False

def check_link_with_pharm(text):
    text = text.replace(':',' ')
    text = text.replace(',',' ')
    text = text.replace('.',' ')
    text = text.replace('&',' ')
    text = text.replace('(',' ')
    text = text.replace(')',' ')
    text = text.replace('"',' ')
    text = text.replace('-',' ')
    
    results = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',text)
    if len(results) != 0:
        for r in results:
            if 'pharm' in r or 'med' in r or 'health' in r or 'drug' in r or 'pill' in r:
                return True
    else:
        return False


def check_phone(text):
    text = text.replace(':',' ')
    text = text.replace(',',' ')
    text = text.replace('.',' ')
    text = text.replace('&',' ')
    text = text.replace('(',' ')
    text = text.replace(')',' ')
    text = text.replace('"',' ')
    text = text.replace('-',' ')

    results = re.findall('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',text)
    if len(results) != 0:
        return True
    else:
        return False

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

def write_file(topic_list,file):
    try:
        target_file = open(file, 'w')
        for t in topic_list:
            print(t)
            target_file.write(str(t))
            target_file.write('\n')
        target_file.close()
    except Exception as e:
        print(e)
        print("can't open file" + file)

def write_csv(data_list,path):
    with open(path, 'w', encoding='utf-16',newline='') as csv_file:
        writer = csv.writer(csv_file)
        for item in data_list:
            writer.writerow(str(item))

if __name__ == '__main__':
    json_path = sys.argv[1] ####the direcory of data .json folder
    target_path = sys.argv[2]  ####the direcory of the output .json 
    platform = sys.argv[3]
    
    #if not os.path.exists(target_path):
    #    os.mkdir(target_path)

    data_list = []
    
    for index,filename in enumerate(sorted(os.listdir(json_path))):
        if filename[-5:] == '.json':
            data_list += read_json(json_path+filename,platform)
        else:
            json_file = json_path + filename + '/'
            print(json_file)
            data_list += read_folder(json_file,platform)

    print(len(data_list))
    write_json(data_list,target_path)
