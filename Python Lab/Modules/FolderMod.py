import os

class FolderMod:
    '''
    Этот модуль работает с файлами
    '''
    
    def __create_Folders(path):
        '''
        создает папки по адресу
        @path - путь к папке
        '''
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def __create_Data_Folder(name):
        '''
        создает папку для датасета
        @name - имя датасета
        '''
        path = f'datasets\\{name}'
        return FolderMod.__create_Folders(path)

    def __get_Systems_Path(name):
        '''
        получает путь к системным данным
        @name - имя датасета
        '''
        path = FolderMod.__create_Data_Folder(name)
        return FolderMod.__create_Folders(path + f'\\__systems')

    def get_Used_Url_Path(name):
        '''
        получает путь к обработанному файлу
        @name - имя датасета
        '''
        return FolderMod.__get_Systems_Path(name) + f'\\url.txt'

    def get_Page_Path(name):
        '''
        получает последнюю загруженную страницу
        @name - имя датасета
        '''
        return FolderMod.__get_Systems_Path(name) + f'\\page.txt'

    def get_Sources_Path(name):
        '''
        получает путь к папке с исходными изображениями
        @name - имя датасета
        '''
        path = FolderMod.__create_Data_Folder(name)
        return FolderMod.__create_Folders(path + f'\\sources')
    
    def get_Small_Path(name):
        '''
        получает путь к папке со сжатыми изображениями
        @name - имя датасета
        '''
        path = FolderMod.__create_Data_Folder(name)
        return FolderMod.__create_Folders(path + f'\\small_sources')

    def get_Last_Page(name):
        '''
        получает последнюю скачанную страницу для запроса
        @name - имя датасета
        '''
        path = FolderMod.get_Page_Path(name)
        pageCount = 0
        if os.path.exists(path):
            with open(path, 'r') as file:
                pageCount = int(file.read()) + 1
        return pageCount

    def get_Used_Url(name):
        '''
        получает список обработанных ссылок на изображения
        @name - имя датасета
        '''
        path = FolderMod.get_Used_Url_Path(name)
        usedURL = []
        if os.path.exists(path):
            with open(path, 'r') as file:
                usedURL = file.read().split('\n')
        return usedURL

    def save_Last_Page(name, page):
        '''
        сохраняет последнюю скачанную страницу
        @name - имя датасета
        '''
        path = FolderMod.get_Page_Path(name)
        with open(path, 'w') as file:
            file.write(str(page))

    
