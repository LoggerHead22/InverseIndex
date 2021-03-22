import gzip
import codecs
import os
import re
import VarByte
import time
import pickle
import numpy as np
from collections import Counter
from functools import reduce
from sklearn.feature_extraction.text import CountVectorizer


def parse_file(path):
    """ Обрабатывает *.gzip файл. Возвращает словарь url : text """

    with gzip.open(path, mode='rb') as f:

        result = {}
        line = " "
        flag = None

        line = f.readline()

        while line:
            url = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', str(line))

            if url:
                flag = True
            else:
                line = f.readline()
                continue


            text = b''
            while flag and line:
                line = f.readline()
                try:
                    text_line = line.decode('utf-8')
                    text += line
                except:
                    result[url[0]] = text.decode('utf-8')
                    flag = False
                    text = b''
                    break

    return result

def lower(text):
    """ Приводит массив токену к нижнему регистру"""
    return [word.lower() for word in text]

def tokenizer(text):
    """ Токенизирует текст"""
    return re.findall(r'\w+', text)

def process_file(file):
    """ Обрабатывает *.gzip файл.
    Возвращает индекс по файлу (по подмножеству документов)."""
    result = parse_file(file)
    for url in result:
        result[url] = tokenizer(result[url])
        result[url] = set(lower(result[url]))
    return result

def diff(post_list):
    """ Переход от id документов к сдвигам"""
    arr = [post_list[0]]
    reduce(lambda x, y: arr.append(y-x) or y, post_list)
    return arr

def inverse_diff(post_list):
    """ Переход от id документов к сдвигам"""
    arr = [post_list[0]]
    reduce(lambda x, y: arr.append(x + y) or x + y, post_list)
    return arr

def make_encoded_pl(index, term, vb):
    """Извлекает из индекса закодированный posting list для term"""

    return vb.encode(diff([i for i, url in enumerate(index) if term in index[url]]))

def build_inverse_index(path):

    files = [os.path.join(path, fpath) for fpath in os.listdir(path)]
    results = [process_file(file) for file in files]


    index = {}
    for result in results:
        index.update(result)

    id2url = {i: url for i, url in enumerate(index)} #отображение id -> url

    with open('id2url.pkl', 'wb') as fp:
        pickle.dump(id2url, fp)

    counter = Counter()

    for key in index:
        counter.update(index[key])

    terms = [pair[0] for pair in counter.most_common() if pair[1] > 1]

    term2id = {key: i for i, key in enumerate(terms)}

    with open('term2id.pkl', 'wb') as fp: #отображение term -> id term'a
        pickle.dump(term2id, fp)

    vb = VarByte.VarByte()

    time_ = time.clock()
    #хранит отображение id term'a -> posting list
    inv_index = {term2id[term] : make_encoded_pl(index, term, vb) for term in terms}

    time_ = time.clock() - time_

    print(time_)

    num_of_bytes = []
    with open('inverse_index', 'wb') as f:
        for term_id in inv_index:
            num_bytes_written = f.write(inv_index[term_id])
            num_of_bytes.append(num_bytes_written)

    with open('n_bytes.pkl', 'wb') as fp:
        pickle.dump(num_of_bytes, fp)

    return inv_index



#%%
if __name__ == '__main__':
    path = 'dataset/dataset'
    index = build_inverse_index(path)
    print(index[15324])
#%%
    vb = VarByte.VarByte()

    #[111, 565, 797]
    #s1 = set(inverse_diff(vb.decode(index[66])))
    #s2 = set(inverse_diff(vb.decode(index[4638])))
    #s3 = set(inverse_diff(vb.decode(index[12968])))

    s1 = set(inverse_diff(vb.decode(index[111])))
    s2 = set(inverse_diff(vb.decode(index[565])))
    s3 = set(inverse_diff(vb.decode(index[797])))


    print(s1 & s2)
    print(s2 & s3)
    print(s1 & s3)

    print(s1 & s2 & s3, len(s1 & s2 & s3))


    #print(vb.decode(index[0]))