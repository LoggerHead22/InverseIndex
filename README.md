Описание файлов: 
    QueryParser.py - класс для парсинга запросов
    QTree.py - содержит классы нод, реализующих дерево запросов с потоковым алгоритмом
    VarByte.py - класс реализующий алгоритм сжатия VarByte
    Index.py - функции для построения обратного индекса
    Search.py - функции для поиска по индексу

    
Работа программы: 
    Помимо стандартных библиотек, реализация требует scikit-learn.
    Поэтому при ее отсутствии, нужно запустить preinstall.sh
    
    Скрипт Index.sh запускает создание индекса. Первый аргумент путь к папке с файлами *.gz.
    Предполагается что в данной папке кроме архивов с данными ничего нет.
    
    Индекс и дополнительные файлы (словарь и другие) помещаются в папку 'index'(создается программой).
    
    Search.sh считывает запросы из stdin. При отсутствие запроса в течении 10 секунд чтение прекращается.  
    