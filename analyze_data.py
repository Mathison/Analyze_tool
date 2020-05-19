#############2018/8/15
#############Jiawei Li
####This file is used to analyze the .json file and capture the words in it

import json
import math
import gzip
import os, sys
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import re
import collections

def clean(text):
    #text = re.sub(r'[^\x00-\x7F]+','', text)
    text = str.replace(text,',',' ')
    text = str.replace(text,"'",' ')
    text = str.replace(text,'"',' ')
    text = str.replace(text,'!',' ')
    text = str.replace(text,'^',' ')
    text = str.replace(text,'(',' ')
    text = str.replace(text,')',' ')
    text = str.replace(text,'%',' ')
    text = str.replace(text,'-',' ')
    text = str.replace(text,'_',' ')
    text = str.replace(text,'|',' ')
    text = str.replace(text,'.',' ')
    text = str.replace(text,':',' ')
    #text = str.replace(text,'@',' ')
    #text = str.replace(text,'#','')
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())

    ####change hyper link to 'hyperlink'
    #text = ' '.join(re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+","hyperlink", text).split())

    ####change phonenumber to 'phonenumber'
    #text = ' '.join(re.sub("(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?","phonenumber", text).split())

    ####change email address to 'emailaddress'
    #text = ' '.join(re.sub("[\w\.-]+@[\w\.-]+\.\w+","emailaddress", text).split())    #text = re.sub('\s+', ' ',text).strip()
    
    text = text.split(' ')
    new_text = []
    for each in text:
        '''
        if(str.find(each,'http') != -1):
            continue
        '''
        if not each.isalnum():
            continue
        new_text.append(str.lower(each));
    text = ' '.join(new_text)

    return text

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def get_data_text(f):
    data = []
    for index,line in enumerate(f):
        ori_data = json.loads(line)
        
        try:
            if line.strip():
                if platform == 'youtube_comment':
                #####clean the original json file
                    comments = list(ori_data['comments'])
                    ori_data['comments'] = []
                    for com in comments:
                        data.append(com['comment_text'])
                                
                if platform == 'youtube_description':
                #####clean the original json file
                    data.append(ori_data['description'])

                if platform == 'instagram_comment':
                #####clean the original json file
                    comments = get_instagram_comments(ori_data)
                    ori_data['comments'] = []
                    for com in comments:
                        com_text = com['node']['text']
                        data.append(com_text)

 
                if platform == 'instagram_post':
                #####clean the original json file
                    text = get_instagram_text(ori_data)
                    data.append(text)
                       
                        
                if platform == 'twitter':
                #####clean the original json file
                    text = get_twitter_text(ori_data)
                    data.append(text) 
                           
                if platform == 'tumblr_comment':
                #####clean the original json file
                    comments = ori_data['comments']
                    for com in comments:
                        if 'reply_text' in com:
                            com_text = com['reply_text']
                            data.append(com_text)

                if platform == 'tumblr_post':
                #####clean the original json file
                    data.append(ori_data['text'])

                if platform == 'tumblr_description':
                #####clean the original json file
                    data.append(ori_data['description']) 

                if platform == 'reddit_description':
                #####clean the original json file
                    for p_key in ori_data['post']:
                        ori_data = ori_data['post'][p_key]
                    text = get_reddit_text(ori_data)
                    data.append(text)

                if platform == 'reddit_comment':
                #####clean the original json file
                    comments_dict = dict(ori_data['comments'])
                    ori_data['comments'] = []
                    ori_data['comment_result'] = {}
                    for com_key in comments_dict:
                        ori_data['comment_result'] = comments_dict[com_key]
                        #print(comments_dict[com_key])
                        text = get_reddit_text(comments_dict[com_key])
                        data.append(text)

                if platform == 'reddit_title':
                #####clean the original json file
                    for p_key in ori_data['post']:
                        ori_data = ori_data['post'][p_key]
                    text = ori_data['title']
                    print(text)
                    data.append(text)

        except Exception as e:
            print(e)
            print(ori_data)
            print("can't open line "+str(index))
    return data

def read_json(file,platform):
    text_data = []
    try:
        with open(file,'r',encoding = 'utf-8') as f:
            text_data = get_data_text(f)
    except Exception as e:
        print(e)
        with open(file,'r',encoding = 'utf-16') as f:
            text_data = get_data_text(f)
    return text_data

###########used to go through the folder, and collect the tweet data
###########it will return the list of tweets in all files in the folder
def read_folder(path,platform):
    total_data = []
    read = 0
    for filename in sorted(os.listdir(path)):
        print('Read ' + path + filename)
        d = read_json(path+filename,platform)
        total_data.extend(d)
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
            continue
    return text

def get_instagram_text(data):
    try:
        text = data['edge_media_to_caption']['edges'][0]['node']['text']
    except:
        text = ''
    return text

def get_instagram_comments(data):
    text_list = []
    try:
        comments_list = data['edge_media_to_comment']['edges']
    except:
        preview_num = 0
        parent_num = 0
        if 'edge_media_to_parent_comment' in data:
            parent_num = len(data['edge_media_to_parent_comment']['edges'])
        
        if 'edge_media_preview_comment' in data:
            preview_num = len(data['edge_media_preview_comment']['edges'])
        
        print(parent_num,preview_num)
        if parent_num >= preview_num:
            comments_list = data['edge_media_to_parent_comment']['edges']
        else:
            comments_list = data['edge_media_preview_comment']['edges']
    return comments_list


def get_twitter_text(data):
    if 'retweeted_status'in data:
        try:
            text = data['retweeted_status']['extended_tweet']['full_text']
        except:
            text = data['retweeted_status']['text']
    else:
        try:
            text = data['extended_tweet']['full_text']
        except:
            if 'full_text' in data:
                text = data['full_text']
            else:
                text = data['text']
    return text 

###########get text from the list file
###########it will collect the text in it
###########remember the text here is the original one without cleaning
###########and also create a dictionary with tweet_id : text
def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items) 

###########get words from one single clean text, return a list of words
def get_word(text):
    special_word = ['rt','co','amp'] #here is the word we don't want it to show up in the sentence
    words = []
    for w in clean(text).split():
        if isEnglish(w):
            if w not in set(stopwords.words('english')) and w not in special_word:
                words.append(w)
    return words
    

############clean the text data and collect the words, the input should be a list of texts
############it will return a vocabulary of words and a dictionary of frequency
def collect_words(list_text,vocab):
    #words_vocab = []
    for t in list_text:
        vocab += get_word(t)
        vocab = list(set(vocab))
    return vocab

##########write vocab to a txt file
def write_vocab(vocab,vocab_path):
    try:
        file = open(vocab_path, 'w')
        for idx,item in enumerate(vocab):
            #file.write(str(idx)+'\t')
            file.write("%s\n" % item)
        file.close()
    except:
        print("can't open file" + vocab_path)
        
def read_vocab(vocab_path):
    try:
        with open(vocab_path) as f:
            vocab = f.readlines()
            vocab = [x.replace('\n','') for x in vocab] 
            return vocab
    except:
        print("can't open file" + vocab_path)

###########write the index code to the btm index file
def get_index(text_list,vocab):
    index_list = []
    for t in text_list:
        words = get_word(t)
        index = []
        for w in words:
            try:
                index.append(vocab.index(w))
            except Exception as e:
                print(e)
                continue
        index_list.append(index)
    return index_list

def write_index(index_list,output_path):
    #vocab = read_vocab(vocab_path)
    btm_input = open(output_path,'w')
    for i in index_list:
        #words = get_word(t)
        for w in i:
            btm_input.write(str(w)+' ')
        btm_input.write('\n')      
    btm_input.close()
      
    #except:
        #print("can't open file" + vocab_path + " or " +input_path)

######write frequency( dict ) to the json file
def write_freq(freq,freq_path):
    try:
        with open(freq_path, 'w') as fp:
            json.dump(freq, fp)
    except:
        print("can't open file" + freq_path)
    
def run_btm_learning(inputfile, no_topics, vocab_file, alpha, beta, total_number_of_iterations, save_step, output_path):
    # Example:
    # ../../BTM/src/btm est 150 3577 0.3 0.01 1000 10 data_processing_files/btm_input.txt output/BTM_OUTPUT/
    #btm_directory = '../BTM/batch/btm '
    execute_string = btm_directory + 'est ' + str(no_topics) + ' ' +             str(len(open(vocab_file,'r').readlines())) + ' ' +             str(alpha) + ' ' +             str(beta) + ' ' +             str(total_number_of_iterations) + ' ' +             str(save_step) + ' ' +             inputfile + ' ' +             output_path

    print(execute_string)
    os.system(execute_string)

def run_btm_inference(no_topics,inputfile,output_path):
    # Example
    # ../../BTM/src/btm inf sum_b 150 ../data_processing_files/btm_input.txt ../output/BTM_OUTPUT/models/first_run/
    #btm_directory = '../BTM/batch/btm '
    execute_string = btm_directory + 'inf sum_b ' + str(no_topics) + ' ' +             inputfile + ' ' +             output_path

    print(execute_string)
    os.system(execute_string)

#############this is the directory where we store the raw jason file
btm_directory = '/home/jimmy/analyze_tool/BTM-master/src/btm '

#########parameter
#num_topics = 20
beta = 0.01
total_number_of_iterations = 1000
save_step = 10
read = 0 

if __name__ == '__main__':
    ######analyze the data
    command = sys.argv[1:]
    option = command[0]  ##has option "--help", "vocab", "BTM"
                         ##"vocab" will write the vocabulary list of these data
                         ##"BTM" will run the btm algorithm to generate the result
    
    if len(command) == 1 and option == "--help":
        print("#########################################"+\
              "\nCommand 'analyze_data.py vocab vocab_path index_path j_path platform' \
              \nWill write the vocabulary of the json data based on 'j_path' to 'vocab_path' \
              \nThen write index of the text to 'output_path' \
              \nCommand 'analyze_data.py BTM vocab_path index_path btm_path num_topics' \
              \nWill apply BTM to index data in 'input_path' and write result to 'btm_path'"+\
              "\n#########################################")
        exit(1)
    
    if len(command) >= 3:
        vocab_path = command[1] 
        index_path = command[2]
        j_path = command[3]  ##path of the folder of json data when option = 'vocab'
                             ##when option == 'BTM' this is the path to the index file
        platform = command[4]

        if option == "vocab":
            word_vocab = []
            all_text = []
            index_list = []
            
            for index,filename in enumerate(sorted(os.listdir(j_path))):  
                print(filename)
                if filename[-5:] == '.json':
                    text_list = read_json(j_path+filename,platform)
                elif os.path.exists(j_path + filename + '/'):
                    print(index)
                    j_file = j_path + filename + '/'
                    text_list = read_folder(j_file,platform)
                else:
                    continue
                print("Number of text is " + str(len(text_list)))
                if len(text_list) == 0:
                    continue
                word_vocab += collect_words(text_list,word_vocab)
                print("Number of words is " + str(len(word_vocab)))
            write_vocab(word_vocab,vocab_path)
            
            word_vocab = read_vocab(vocab_path)
            for index,filename in enumerate(sorted(os.listdir(j_path))):
                #print(j_path + filename + '/')
                if filename[-5:] == '.json':
                    text_list = read_json(j_path+filename,platform)
                elif os.path.exists(j_path + filename + '/'):
                        
                    j_file = j_path + filename + '/'
                    text_list = read_folder(j_file,platform)
                else:
                    continue

                index_list += get_index(text_list,word_vocab)
                print('Finish index generation on ' + str(filename))
            print('The total number of text is ' + str(len(index_list)))            
            write_index(index_list,index_path)
            

    
        ######excute the btm
        if option == "BTM":
            BTM_path = command[3]
            num_topics = command[4]
            alpha = 50/int(num_topics)
            if not os.path.exists(BTM_path):
                os.mkdir(BTM_path)
            run_btm_learning(index_path, num_topics, vocab_path, alpha, beta, total_number_of_iterations, save_step, BTM_path)
            run_btm_inference(num_topics,index_path,BTM_path)

