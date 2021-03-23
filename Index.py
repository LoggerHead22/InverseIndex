import gzip
import os
import sys
import re
import pickle
import VarByte
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
    arr = [next(post_list)]
    reduce(lambda x, y: arr.append(x + y) or x + y, post_list)
    return arr

def make_encoded_pl(post_list, vb):
    """Извлекает из индекса закодированный posting list для term"""

    return vb.encode(diff(post_list))

def build_inverse_index(path):
    """Строим обратный индекс. path - путь к папке с *.gz файлами"""
    files = [os.path.join(path, fpath) for fpath in os.listdir(path)]
    results = [process_file(file) for file in files]

    if not os.path.exists('index'):
        os.makedirs('index')

    index = {}
    for result in results:
        index.update(result)

    id2url = {i: url for i, url in enumerate(index)} #отображение id -> url

    with open('index/id2url.pkl', 'wb') as fp:
        pickle.dump(id2url, fp)

    counter = Counter()

    for key in index:
        counter.update(index[key])

    terms = [pair[0] for pair in counter.most_common() if pair[1] > 1]

    term2id = {key: i for i, key in enumerate(terms)}

    with open('index/term2id.pkl', 'wb') as fp: #отображение term -> id term'a
        pickle.dump(term2id, fp)

    vb = VarByte.VarByte()


    data_text = [" ".join(tokens) for tokens in index.values()]

    vectorizer = CountVectorizer(vocabulary = terms, token_pattern = r'\w+')

    data_vec = vectorizer.fit_transform(data_text)

    #хранит отображение id term'a -> posting list
    inv_index = {i : make_encoded_pl(pl, vb)
                 for i, pl in enumerate(data_vec.T.tolil().rows)}


    num_of_bytes = []
    with open('index/inverse_index', 'wb') as f:
        for term_id in inv_index:
            num_bytes_written = f.write(inv_index[term_id])
            num_of_bytes.append(num_bytes_written)

    with open('index/n_bytes.pkl', 'wb') as fp:
        pickle.dump(num_of_bytes, fp)

    return True



#%%
if __name__ == '__main__':
    #path = 'dataset/dataset'
    if len(sys.argv) > 2:
        print('Wrong Input Argaments. Need path to *.gz files')

    else:
        print('Building Index...')
        path = sys.argv[1]
        if(build_inverse_index(path)):
            print('Inverse Index Successfully built')
