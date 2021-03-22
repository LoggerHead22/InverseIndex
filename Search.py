import QTree
import VarByte
import pickle


def process_query(query):

    with open('id2url.pkl', 'rb') as fp:
        id2url = pickle.load(fp)

    with open('term2id.pkl', 'rb') as fp:
        term2id = pickle.load(fp)

    with open('n_bytes.pkl', 'rb') as fp:
        num_of_bytes = pickle.load(fp)

    #dict_ = {}
    qtree = QTree.QTree(len(id2url))

    qtree.build_tree(query)

    #print(qtree.dict)

    line2term = {}
    lines = []
    for term in qtree.dict:
        if term in term2id:
            line2term[term2id[term]] = term
            lines.append(term2id[term])

    lines = sorted(lines)

    #print(lines)
    vb = VarByte.VarByte()

    with open('inverse_index', 'rb') as f:
        #cчитываем только нужные постинг листы
        for i, line in enumerate(lines):
            f.seek(sum(num_of_bytes[:line]), 0)
            string_of_byte = f.read(num_of_bytes[line])
            qtree.dict[line2term[line]].append(vb.decode(string_of_byte))

    #print(qtree.dict)
    result = qtree.execute()

    print(query)
    print(len(result))
    for id_ in result:
        pass
        print(id2url[id_])

    return len(result)


def search():
    pass

if __name__ == '__main__':

    with open('id2url.pkl', 'rb') as fp:
        id2url = pickle.load(fp)

    with open('term2id.pkl', 'rb') as fp:
        term2id = pickle.load(fp)

    print(len(term2id))


    querys = ['энергоносители', 'власти & США & конфликт',
              'Представитель & милиции', 'Совет & Федерации & президент',
              'США & конгресс & Сирия', 'Range & Rover',
              'Россия & экономика & инфляция', 'Шенгенское & соглашение']
    #for query in querys:
    #    process_query(query)

    #print(process_query('путин'))
    #print(process_query("навальный & враг & народа"))