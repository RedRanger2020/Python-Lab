import os

class FolderMod:
    '''
    Этот модуль работает с файлами
    '''
    
    def __create_folders(path):
        '''
        создает папки по адресу
        @path - путь к папке
        '''
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def __create_data_folder(name):
        '''
        создает папку для датасета
        @name - имя датасета
        '''
        path = f'datasets\\{name}'
        return FolderMod.__create_folders(path)

    def __get_Systems_Path(name):
        '''
        получает путь к системным данным
        @name - имя датасета
        '''
        path = FolderMod.__create_data_folder(name)
        return FolderMod.__create_folders(path + f'\\__systems')

    def get_used_url_path(name):
        '''
        получает путь к обработанному файлу
        @name - имя датасета
        '''
        return FolderMod.__get_Systems_Path(name) + f'\\url.txt'

    def get_page_path(name):
        '''
        получает последнюю загруженную страницу
        @name - имя датасета
        '''
        return FolderMod.__get_Systems_Path(name) + f'\\page.txt'

    def get_sources_path(name):
        '''
        получает путь к папке с исходными изображениями
        @name - имя датасета
        '''
        path = FolderMod.__create_data_folder(name)
        return FolderMod.__create_folders(path + f'\\sources')
    
    def get_small_path(name):
        '''
        получает путь к папке со сжатыми изображениями
        @name - имя датасета
        '''
        path = FolderMod.__create_data_folder(name)
        return FolderMod.__create_folders(path + f'\\small_sources')

    def get_last_page(name):
        '''
        получает последнюю скачанную страницу для запроса
        @name - имя датасета
        '''
        path = FolderMod.get_page_path(name)
        pageCount = 0
        if os.path.exists(path):
            with open(path, 'r') as file:
                pageCount = int(file.read()) + 1
        return pageCount

    def get_used_url(name):
        '''
        получает список обработанных ссылок на изображения
        @name - имя датасета
        '''
        path = FolderMod.get_used_url_path(name)
        usedURL = []
        if os.path.exists(path):
            with open(path, 'r') as file:
                usedURL = file.read().split('\n')
        return usedURL

    def save_last_page(name, page):
        '''
        сохраняет последнюю скачанную страницу
        @name - имя датасета
        '''
        path = FolderMod.get_page_path(name)
        with open(path, 'w') as file:
            file.write(str(page))

    
