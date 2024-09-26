import os

'''
���� ������ �������� � �������
'''
class FolderMod:
    
    def __createFolders(path):
        '''
        ������� ����� �� ������
        @path - ���� � �����
        '''
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def __createDataFolder(name):
        '''
        ������� ����� ��� ��������
        @name - ��� ��������
        '''
        path = f'datasets\\{name}'
        return FolderMod.__createFolders(path)

    def __getSystemsPath(name):
        '''
        �������� ���� � ��������� ������
        @name - ��� ��������
        '''
        path = FolderMod.__createDataFolder(name)
        return FolderMod.__createFolders(path + f'\\__systems')

    def getUsedUrlPath(name):
        '''
        �������� ���� � ������������� �����
        @name - ��� ��������
        '''
        return FolderMod.__getSystemsPath(name) + f'\\url.txt'

    def getPagePath(name):
        '''
        �������� ��������� ����������� ��������
        @name - ��� ��������
        '''
        return FolderMod.__getSystemsPath(name) + f'\\page.txt'

    def getSourcesPath(name):
        '''
        �������� ���� � ����� � ��������� �������������
        @name - ��� ��������
        '''
        path = FolderMod.__createDataFolder(name)
        return FolderMod.__createFolders(path + f'\\sources')
    
    def getSmallPath(name):
        '''
        �������� ���� � ����� �� ������� �������������
        @name - ��� ��������
        '''
        path = FolderMod.__createDataFolder(name)
        return FolderMod.__createFolders(path + f'\\small_sources')

    def getLastPage(name):
        '''
        �������� ��������� ��������� �������� ��� �������
        @name - ��� ��������
        '''
        path = FolderMod.getPagePath(name)
        pageCount = 0
        if os.path.exists(path):
            with open(path, 'r') as file:
                pageCount = int(file.read()) + 1
        return pageCount

    def getUsedUrl(name):
        '''
        �������� ������ ������������ ������ �� �����������
        @name - ��� ��������
        '''
        path = FolderMod.getUsedUrlPath(name)
        usedURL = []
        if os.path.exists(path):
            with open(path, 'r') as file:
                usedURL = file.read().split('\n')
        return usedURL

    def saveLastPage(name, page):
        '''
        ��������� ��������� ��������� ��������
        @name - ��� ��������
        '''
        path = FolderMod.getPagePath(name)
        with open(path, 'w') as file:
            file.write(str(page))

    
