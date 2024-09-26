import os

'''
Этот модуль работает с файлами
'''
class FolderMod:
    
    def __createFolders(path):
        '''
        создает папки по адресу
        @path - путь к папке
        '''
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def __createDataFolder(name):
        '''
        создает папку для датасета
        @name - имя датасета
        '''
        path = f'datasets\\{name}'
        return FolderMod.__createFolders(path)

    def __getSystemsPath(name):
        '''
        получает путь к системным данным
        @name - имя датасета
        '''
        path = FolderMod.__createDataFolder(name)
        return FolderMod.__createFolders(path + f'\\__systems')

    def getUsedUrlPath(name):
        '''
        получает путь к обработанному файлу
        @name - имя датасета
        '''
        return FolderMod.__getSystemsPath(name) + f'\\url.txt'

    def getPagePath(name):
        '''
        получает последнюю загруженную страницу
        @name - имя датасета
        '''
        return FolderMod.__getSystemsPath(name) + f'\\page.txt'

    def getSourcesPath(name):
        '''
        получает путь к папке с исходными изображениями
        @name - имя датасета
        '''
        path = FolderMod.__createDataFolder(name)
        return FolderMod.__createFolders(path + f'\\sources')
    
    def getSmallPath(name):
        '''
        получает путь к папке со сжатыми изображениями
        @name - имя датасета
        '''
        path = FolderMod.__createDataFolder(name)
        return FolderMod.__createFolders(path + f'\\small_sources')

    def getLastPage(name):
        '''
        получает последнюю скачанную страницу для запроса
        @name - имя датасета
        '''
        path = FolderMod.getPagePath(name)
        pageCount = 0
        if os.path.exists(path):
            with open(path, 'r') as file:
                pageCount = int(file.read()) + 1
        return pageCount

    def getUsedUrl(name):
        '''
        получает список обработанных ссылок на изображения
        @name - имя датасета
        '''
        path = FolderMod.getUsedUrlPath(name)
        usedURL = []
        if os.path.exists(path):
            with open(path, 'r') as file:
                usedURL = file.read().split('\n')
        return usedURL

    def saveLastPage(name, page):
        '''
        сохраняет последнюю скачанную страницу
        @name - имя датасета
        '''
        path = FolderMod.getPagePath(name)
        with open(path, 'w') as file:
            file.write(str(page))

    
