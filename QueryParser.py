import re
import QTree

class QueryParser:
    operators = {'&', '|'}

    def __init__(self, create_func):
        self.create_func = create_func

    def parse(self, query):
        return self.parse_recurent(re.findall(r'\w+|[\(\)&\|!]', query))

    @classmethod
    def del_brackets(cls, token_query):
        if len(token_query) < 3:
            return token_query

        counter = 0
        flag = True
        for token in token_query[:-1]:
            if token == '(':
                counter+=1
            elif token == ')':
                counter-=1

            if counter == 0:
                flag = False
                break

        if flag:
            return token_query[1:-1]
        else:
            return token_query

    @classmethod
    def find_operator_index(cls, token_query):
        counter = 0
        result_or = None
        result_and = None

        for i, token in enumerate(token_query):
            if token == '(':
                counter+=1
            elif token == ')':
                counter-=1

            if token == '|' and counter == 0:
                result_or = i

            if token == '&' and counter == 0:
                result_and = i

        if result_or:
            return result_or

        if result_and:
            return result_and


        return None

    def parse_recurent(self, token_query):
        QNode = None
        token_query = QueryParser.del_brackets(token_query) #удаляем обвязку из скобок если нужно

        index = QueryParser.find_operator_index(token_query)

        if index is None:
            if token_query[0] == '!':
                QNode = self.create_func(token_query[0])
                left_node = self.parse_recurent(token_query[1:])
                right_node = None
                QNode.fill_childs(left_node, right_node)
            else:
                QNode = self.create_func(token_query[0])

        else:
            QNode = self.create_func(token_query[index])
            left_node = self.parse_recurent(token_query[:index])
            right_node = self.parse_recurent(token_query[index + 1:])

            QNode.fill_childs(left_node, right_node)

        return QNode


if __name__ == '__main__':
    test_str = "(!(docker & запуск) & (ubuntu | убунту) | привет)"
