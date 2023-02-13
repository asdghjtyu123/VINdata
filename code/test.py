import requests
import json
import os
import time
import os
import json
import requests
import numpy as np
def _levenshtein_distance(ref, hyp):
    m = len(ref)
    n = len(hyp)

    if ref == hyp:
        return 0
    if m == 0:
        return n
    if n == 0:
        return m

    if m < n:
        ref, hyp = hyp, ref
        m, n = n, m

    distance = np.zeros((2, n + 1), dtype=np.int32)

    for j in range(0,n + 1):
        distance[0][j] = j

    for i in range(1, m + 1):
        prev_row_idx = (i - 1) % 2
        cur_row_idx = i % 2
        distance[cur_row_idx][0] = i
        for j in range(1, n + 1):
            if ref[i - 1] == hyp[j - 1]:
                distance[cur_row_idx][j] = distance[prev_row_idx][j - 1]
            else:
                s_num = distance[prev_row_idx][j - 1] + 1
                i_num = distance[cur_row_idx][j - 1] + 1
                d_num = distance[prev_row_idx][j] + 1
                distance[cur_row_idx][j] = min(s_num, i_num, d_num)

    return distance[m % 2][n]


def word_errors(reference, hypothesis, ignore_case=False, delimiter=' '):
    if ignore_case == True:
        reference = reference.lower()
        hypothesis = hypothesis.lower()

    ref_words = reference.split(delimiter)
    hyp_words = hypothesis.split(delimiter)

    edit_distance = _levenshtein_distance(ref_words, hyp_words)
    return float(edit_distance), len(ref_words)


def char_errors(reference, hypothesis, ignore_case=False, remove_space=False):
    if ignore_case == True:
        reference = reference.lower()
        hypothesis = hypothesis.lower()

    join_char = ' '
    if remove_space == True:
        join_char = ''

    reference = join_char.join(filter(None, reference.split(' ')))
    hypothesis = join_char.join(filter(None, hypothesis.split(' ')))

    edit_distance = _levenshtein_distance(reference, hypothesis)
    return float(edit_distance), len(reference)


def wer(reference, hypothesis, ignore_case=False, delimiter=' '):
    edit_distance, ref_len = word_errors(reference, hypothesis, ignore_case,
                                         delimiter)

    if ref_len == 0:
        raise ValueError("Reference's word number should be greater than 0.")

    wer = float(edit_distance) / ref_len
    return wer


def cer(reference, hypothesis, ignore_case=False, remove_space=False):
    edit_distance, ref_len = char_errors(reference, hypothesis, ignore_case,
                                         remove_space)

    if ref_len == 0:
        raise ValueError("Length of reference should be greater than 0.")

    cer = float(edit_distance) / ref_len
    return cer
def requestviettel(filename):
    
    url = "https://viettelgroup.ai/voice/api/asr/v1/rest/decode_file"
    headers = {
        'token': 'anonymous'
    }
    files = {'file': open(filename,'rb')}
    response = requests.post(url,files=files, headers=headers,timeout=None)
    ref_=response.json()
    if (len(ref_)==1):
        transcript=ref_[0]['result']['hypotheses'][0]['transcript']
        # print(transcript)    
    elif (len(ref_)==2):
        transcript=ref_[0]['result']['hypotheses'][0]['transcript']+' '+ref_[1]['result']['hypotheses'][0]['transcript']
    else:
        transcript=ref_[0]['result']['hypotheses'][0]['transcript']+' '+ref_[1]['result']['hypotheses'][0]['transcript']+' '+ref_[2]['result']['hypotheses'][0]['transcript']
    print(transcript) 
    return transcript

def viettel(audio_dir):
    a=[]
    audio_dirout='tran'+'\\'
    for i in os.listdir(audio_dir):
        print(i.split('.')[0])
        b=i.split('.')[0]
        c=i.split('.')[1]
        if c != 'wav':
            continue
        if not os.path.exists("tran"):
            os.mkdir("tran")     
        if (os.path.isfile(audio_dirout+b+'.txt')):
            continue
        a.append(requestviettel('{}{}'.format(audio_dir,i)))
        with open('{}{}.txt'.format(audio_dirout,b),'a',encoding='utf-8') as h:
            h.write(requestviettel('{}{}'.format(audio_dir,i)))
        for j in os.listdir(r'D:\15m\tran'):
            if os.path.getsize('D:\\15m\\tran\\'+j) == 0:
                print ("delete",audio_dirout+b+'.txt')
                os.remove('D:\\15m\\tran\\'+j)
    return a


def requestFPT(filename):
    url = 'https://api.fpt.ai/hmi/asr/general'
    payload = open(filename, 'rb').read()
    headers = {'api-key': 'E7WVMDd26dtKm5Q7tRo1MORnwsUDOzik'}
     #examle: 'api-key': '3ISvE45DVemWTvrMTIgMtyfIjHnd8yAz'
    response = requests.post(url=url, data=payload, headers=headers,timeout=None)
    res_json = response.json()
    # print(res_json,"***")
    transcript = res_json['hypotheses'][0]['utterance']
    #print('request FPT success')

    print('FPT transcript:',transcript)
    return transcript



def FPT(audio_dir_path , transcript_out_dir):
    audio_dir = audio_dir_path 
    transcript_dir = transcript_out_dir + '\\'
    if not os.path.exists(transcript_dir):
        os.mkdir(transcript_dir) 
    for j in os.listdir(r'D:\15m\cuted_transcript'):
        if os.path.getsize('D:\\15m\\cuted_transcript\\'+j) == 0:
            print ("delete"+j)
            os.remove('D:\\15m\\cuted_transcript\\'+j)        
    for f in os.listdir(audio_dir):
        if (f.split('.')[1]!='wav'):
            continue
        name_label_file = transcript_dir + f.split('.')[0]+ '.txt'
        if (os.path.isfile(name_label_file)):
            continue
        audio_path = audio_dir + f
        label_file = open(name_label_file, 'w', encoding='utf-8')
        res = requestFPT(audio_path)
        label_file.write(res)
        print(name_label_file)

def bum():
    f = open('D:\\15m\\data\\15m.json','r',encoding='utf-8')
    a=[]
    data = json.load(f)
    for i in data:
        # if (i['wav'].split('wav')[0]+'txt' in os.listdir(r'D:\15m\tran')):      
            #  ********Dung viettel thi bo cai nay 
        a.append(i['text'])
        # print(i['text'])
    return a

def predfpt():
    f = open('D:\\15m\\data\\15m.json','r',encoding='utf-8')
    a=[]
    aa=[]
    data = json.load(f)
    audir=r'D:\15m\cuted_transcript'
    for i in data:
        with open(audir+'\\'+i['wav'].split('wav')[0]+'txt','r',encoding='utf-8') as f:
            a=f.readlines()
            aa.append(a[-1].upper())
    return aa
def predviettel():
    f = open('D:\\15m\\data\\15m.json','r',encoding='utf-8')
    a=[]
    aa=[]
    data = json.load(f)
    audir=r'D:\15m\tran'
    for i in data:
        print(os.path.isfile(audir+'\\'+i['wav'].split('wav')[0]+'txt'),audir+'\\'+i['wav'].split('wav')[0]+'txt')
        if (os.path.exists(audir+'\\'+i['wav'].split('wav')[0]+'txt')):
            print(os.path.isfile(audir+'\\'+i['wav'].split('wav')[0]+'txt'),audir+'\\'+i['wav'].split('wav')[0]+'txt')
            with open(audir+'\\'+i['wav'].split('wav')[0]+'txt','r',encoding='utf-8') as f:
                a=f.readlines()

                aa.append(a[0].upper())
            # pass
            
        else:
            # print(os.path.isfile(audir+'\\'+i['wav'].split('wav')[0]+'txt'),audir+'\\'+i['wav'].split('wav')[0]+'txt')
            pass
    print(aa)
    return aa
if __name__ == '__main__':
    test_cer, test_wer = [], []
    a=predfpt()
    b=bum()
    for j in range(len(a)):
                # print(decoded_preds[j])
        test_cer.append(cer(b[j], a[j]))
        test_wer.append(wer(b[j], a[j]))

    avg_cer = sum(test_cer)/len(test_cer)
    avg_wer = sum(test_wer)/len(test_wer)
    print('avg_cer:',avg_cer*100,'avg_wer:',avg_wer*100)
    # requestviettel(r'D:\15m\data\000002022072920-03.wav'
    foldeR_='D:\\15m\\data\\'
    
    # FPT(foldeR_, 'cuted_transcript')
    for i in viettel(foldeR_):
        print(i)