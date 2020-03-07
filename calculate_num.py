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
    text = ' '.join(re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+","hyperlink", text).split())

    ####change phonenumber to 'phonenumber'
    text = ' '.join(re.sub("(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?","phonenumber", text).split())

    ####change email address to 'emailaddress'
    text = ' '.join(re.sub("[\w\.-]+@[\w\.-]+\.\w+","emailaddress", text).split())    #text = re.sub('\s+', ' ',text).strip()
    
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

def read_json(file):
    data = []
    count = 1
    print('Read '+file)
    if file[-5:] != '.json':
        return ['']
    try:
        with open(file,'r') as f:
            for index,line in enumerate(f):
                try:
                    if line.strip():
                        text = get_reddit_comments_text(json.loads(line))
                        if type(text) == list:
                            for t in text:
                                data.append(t)
                        else:
                            data.append(text)
                except Exception as e:
                    print(e)
                    print("can't open line "+str(index))
    except Exception as e:
        print(e)
        with open(file,'r',encoding = 'utf-16') as f:
            for index,line in enumerate(f):
                try:
                    if line.strip():
                        text = get_reddit_comments_text(json.loads(line))
                        if type(text) == list:
                            for t in text:
                                data.append(t)
                        else:
                            data.append(text)
                except Exception as e:
                    print(e)
                    print("can't open line "+str(index))
    return len(data)

###########used to go through the folder, and collect the tweet data
###########it will return the list of tweets in all files in the folder
def read_folder(path):
    text_data = 0
    for index,filename in enumerate(sorted(os.listdir(path))):
        try:
            d = read_json(path+filename)
            text_data += d
        except Exception as e:
            print(e)
            print("Can't open file "+str(filename))
        print('Finish read '+filename)
    return text_data

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

def get_reddit_comments_text(data):
    comments = data['comments']
    comments_list = [key for key in comments]
    return comments_list

def get_twitter_text(data):
    flattern_data = flatten(data)
    text = data['text']
    for key in flattern_data:
        if key.split('.')[-1] == 'full_text':
            text = flattern_data[key]
    return text  

def get_instagram_text(data):
    try:
        text = data['edge_media_to_caption']['edges'][0]['node']['text']
    except:
        text = ''
    return text

def get_tumblr_comments_text(data):
    comment_list = []
    for comment in data['comments']:
        try:
            comment_list.append(comment['reply_text'])
        except:
            continue
    return comment_list

def get_instagram_comments_text(data):
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
        
    for comment in comments_list:
        text_list.append(comment['node']['text'])
    return text_list

def get_youtube_description_text(data):
    data_list = data['description']
    return data_list


def get_youtube_comments_text(data):
    data_list = []
    if len(data['comments']) != 0:
        for comment in data['comments']:
            data_list.append(comment['comment_text'])
    return data_list


def get_reddit_title_text(data):
    data_list = []
    data_list.append(data['title'])
    return data_list

def get_reddit_comments_text(data):
    data_list = []
    if 'children' not in data:
        return data_list
    for d in data['children']:
        data_list.append(d['text'])
        data_list += get_reddit_comment_text(d)
    return data_list

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

if __name__ == '__main__':
        #json_path = ['./scraper_data/twitter/opioids/xannax/','./scraper_data/twitter/opioids/xanax/']
        #json_path = ['./scraper_data/tumblr/opioids/xannax/','./scraper_data/tumblr/opioids/xanax/']
        json_path = ['/data2/opioids/reddit/opioids_test/opioids/']
        text_list = 0
        for j_path in json_path:
            for index,filename in enumerate(sorted(os.listdir(j_path))):  
                print(filename)
                if filename[-5:] == '.json':
                    text_list += read_json(j_path+filename)
                elif os.path.exists(j_path + filename + '/'):
                    print(index)
                    j_file = j_path + filename + '/'
                    text_list += read_folder(j_file)
                else:
                    continue
        print(text_list)