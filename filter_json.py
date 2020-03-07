import json
import time
import os,sys
import csv
import collections

###########used to read a single json file, it will return a list of orginal tweet information
def read_json(file,platform):
    data = []
    if file[-5:] != '.json':
        return ['']

    try:
        with open(file,'r',encoding = 'utf-8') as f:
            for index,line in enumerate(f):
                ori_data = json.loads(line)
                try:
                    if line.strip():
                        if platform == 'youtube_comment':
                            #####clean the original json file
                            comments = list(ori_data['comments'])
                            
                            for com in comments:
                                ori_data['comment_result'] = com 
                                data.append(ori_data)
                            

                        if platform == 'youtube_description':
                        #####clean the original json file
                            data.append(ori_data)

                        if platform == 'instagram_comment':
                        #####clean the original json file
                            comments = get_instagram_comments(ori_data)
                            
                            for com in comments:
                                ori_data['comments'] = []
                                com_text = com['node']['text']
                                print(com_text)
                                ori_data['comments'].append(com)
                                data.append(ori_data)
                                                       
 
                        if platform == 'instagram_post':
                        #####clean the original json file
                            data.append(ori_data)
                        
                        if platform == 'twitter':
                        #####clean the original json file
                            data.append(ori_data)
                           
                        if platform == 'tumblr_comment':
                        #####clean the original json file
                            comments = ori_data['comments']
                            
                            for com in comments:
                                ori_data['comments'] = []
                                if 'reply_text' in com:
                                    com_text = com['reply_text']
                                    ori_data['comments'].append(com)
                                    data.append(ori_data)
                                                           

                        if platform == 'tumblr_post':
                        #####clean the original json file
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
                        if platform == 'youtube_comment':
                            #####clean the original json file
                            comments = list(ori_data['comments'])
                            
                            for com in comments:
                                ori_data['comment_result'] = com 
                                data.append(ori_data)

                        if platform == 'youtube_description':
                        #####clean the original json file
                            data.append(ori_data)

                        if platform == 'instagram_comment':
                        #####clean the original json file
                            comments = get_instagram_comments(ori_data)
                            
                            for com in comments:
                                ori_data['comments'] = []
                                com_text = com['node']['text']
                                print(com_text)
                                ori_data['comments'].append(com)
                                data.append(ori_data)
                                                       
 
                        if platform == 'instagram_post':
                        #####clean the original json file
                            data.append(ori_data)
                        
                        if platform == 'twitter':
                        #####clean the original json file
                            data.append(ori_data)
                           
                        if platform == 'tumblr_comment':
                        #####clean the original json file
                            comments = ori_data['comments']
                            
                            for com in comments:
                                ori_data['comments'] = []
                                if 'reply_text' in com:
                                    com_text = com['reply_text']
                                    ori_data['comments'].append(com)
                                    data.append(ori_data)
                                                           

                        if platform == 'tumblr_post':
                        #####clean the original json file
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
        text = data['text']
    except:
        text = data['full_text']
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


################output the target tweets according to the topic result
def find_target(data_list,doc_path,num):
    result = []
    topic_list = []
    with open(doc_path+'k'+str(num)+'.pz_d') as f:
        re=f.readlines()
        for ind,r in enumerate(re):

            topic = [float(t) for t in r.split()]
            if topic.index(max(topic)) in [3,23]:   
                result.append(data_list[ind])
                topic_list.append(topic.index(max(topic)))
    #result = [float(p) for p in open(path).readline().split()]
    return result,topic_list

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

def write_csv(topic_list,path):
    with open(path, 'w', encoding='utf-16',newline='') as csv_file:
        writer = csv.writer(csv_file)
        for item in topic_list:
            writer.writerow(str(item))

if __name__ == '__main__':
    json_path = sys.argv[1] ####the direcory of data .json folder
    doc_topic = sys.argv[2] ####the direcory of k#.pz_d
    num_topic = sys.argv[3]
    target_path = sys.argv[4]  ####the direcory of the output .json 
    platform = sys.argv[5]

    if not os.path.exists(target_path):
        os.mkdir(target_path)

    read = 0
    data_list = []
    
    for index,filename in enumerate(sorted(os.listdir(json_path))):
        if filename[-5:] == '.json':
            data_list += read_json(json_path+filename,platform)
        else:
            json_file = json_path + filename + '/'
            data_list += read_folder(json_file,platform)

    print(len(data_list))
    target_data,topic_list = find_target(data_list,doc_topic,num_topic)
    print(len(target_data))
    print(len(topic_list))
    write_json(target_data,target_path)
