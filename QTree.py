import QueryParser

"""
В данном модуле реализованны классы для нод дерева запросов, 
реализующих потоковый алгоритм.
"""

class QTreeNode:

    """
    Базовый класс для ноды дерева запросов
    """

    StartCode = -101
    EndCode = float('inf')

    def __init__(self, value):
        self.value = value
        self.current_value = QTreeNode.StartCode
        self.left = None
        self.right = None

    def fill_childs(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        if self.left and self.right:
            print('Value: ', self.value, 'Left:', self.left.value,
                  'Right:', self.right.value)
            print(self.left)
            print(self.right)
        else:
            print('Value: ', self.value, 'Left:',
                  self.left, 'Right:', self.right)
        return "_______"

    def evaluate():
        pass

    def goto():
        pass


class QTreeNodeTerm(QTreeNode):
    """
    Класс для листовой ноды дерева запросов.
    """

    def __init__(self, term):
        super().__init__(term.lower())
        self.post_list = []

    def evaluate(self):
        return self.current_value

    def get_post_list(self):
        return self.post_list

    def goto(self, doc_id):

        while self.current_value < doc_id:
            try:
                temp = next(self.generate_values())
            except:
                print('ERRRROR')
                temp = None

            if temp is not None:
                if self.current_value != QTreeNode.StartCode:
                    self.current_value += temp
                else:
                    self.current_value = temp
            else:
                self.current_value = QTreeNode.EndCode
                break
        #print(self.value, doc_id, self.current_value)

    def generate_values(self):
        if len(self.post_list) == 0:
            yield None
        else:
            for value in self.post_list[0]:
                yield value

            yield None

class QTreeNodeOr(QTreeNode):
    """
    Класс для |-ноды дерева запросов.
    """

    def __init__(self, operator):
        super().__init__(operator)

    def evaluate(self):
        self.left_value = self.left.evaluate()
        self.right_value = self.right.evaluate()

        #print('Or', self.left_value, self.right_value)
        result = min(self.left_value, self.right_value)

        return result

    def goto(self, doc_id):
        self.left.goto(doc_id)
        self.right.goto(doc_id)


class QTreeNodeAnd(QTreeNode):
    """
    Класс для &-ноды дерева запросов.
    """

    def __init__(self, operator):
        super().__init__(operator)

    def evaluate(self):
        self.left_value = self.left.evaluate()
        self.right_value = self.right.evaluate()

        #print('And', self.left_value, self.right_value)

        while self.left_value != self.right_value:
            max_value = max(self.left_value, self.right_value)
            self.left.goto(max_value)
            self.right.goto(max_value)
            self.left_value = self.left.evaluate()
            self.right_value = self.right.evaluate()
            #print('And', self.left_value, self.right_value)

        return self.left_value

    def goto(self, doc_id):
        self.left.goto(doc_id)
        self.right.goto(doc_id)


class QTreeNodeNot(QTreeNode):
    """
    Класс для !-ноды дерева запросов.
    """

    def __init__(self, operator, len_):
        super().__init__(operator)
        self.current_not_value = -1
        self.len = len_

    def evaluate(self):
        return self.current_not_value

    def goto(self, doc_id):
        if doc_id > self.current_not_value:
            self.current_not_value = doc_id
        self.left.goto(doc_id)
        self.current_value = self.left.evaluate()

        #print('NOT', self.left.value, self.current_not_value, self.current_value)

        while self.current_not_value == self.current_value:
            if self.current_not_value < self.len:
                self.goto(doc_id + 1)
            else:
                break


class QTree():

    def __init__(self, len_):
        self.dict = {}
        self.len = len_
        self.parser = QueryParser.QueryParser(self.make_node)
        self.head = None

    def __repr__(self):
        print(self.head)
        return '-------'

    def build_tree(self, query):
        self.head = self.parser.parse(query)

    def make_node(self, token):
        if token == '&':
            return QTreeNodeAnd(token)
        elif token == '|':
            return QTreeNodeOr(token)
        elif token == '!':
            return QTreeNodeNot(token, self.len)
        else:
            term_node = QTreeNodeTerm(token.lower())
            self.dict[token.lower()] = term_node.get_post_list()
            return term_node

    def execute(self):
        result = []
        self.current_value = 0

        while self.current_value <= self.len:
            self.head.goto(self.current_value)
            self.current_value = self.head.evaluate()
            #print(self.current_value)
            if self.current_value != QTreeNode.EndCode:
                result.append(self.current_value)

            self.current_value += 1

        return result


