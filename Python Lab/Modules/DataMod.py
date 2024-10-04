import os
import requests
import time
import json
import shutil
import cv2
from Modules.FolderMod import FolderMod as fm
from random import randint
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fp.fp import FreeProxy

class DataMod(object):
    '''
    Класс отвечает за получение и загрузку данных
    '''
    
    frp = FreeProxy(rand=True)
    lastProxies = {}
    blackProxy =[]
    
    def __parsePage(page,query):
        '''
        Разбор кода html страницы
        @page - номер страницы
        @query - запрос
        '''
        content = DataMod.__getHtml(page, query, False)
        #получаем содержимое страницы
        rootDiv = None
        while rootDiv is None:
            root = BeautifulSoup(content, 'html.parser')
            rootDiv = root.find('div', class_="Root", id=lambda x: x and x.startswith('ImagesApp-'))
            #проверка на капчу
            if(rootDiv is None):
                DataMod.lastProxies = {}
                print(f'Capcha on {page} page.') 
                content = DataMod.__getHtml(page, query, True)

        dataState = rootDiv.get('data-state');
        jdata = json.loads(dataState)
        jent = jdata['initialState']['serpList']['items']['entities']
        
        links = []
        #получаем url оригинальных изображений
        for item in jent:
            url = jent[item]['origUrl'];
            print(url)
            links.append(url)

        return links


    def __getHeaders():
         '''
         Получение случайного заголовка страницы
         '''
         ua = UserAgent(os='windows',min_percentage=40)
         headers = {'User-Agent': ua.random,
                   'Accept-Encoding': 'gzip, deflate, br, zstd',
                   'Accept-Language': 'ru,en;q=0.9',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
                   }
         return headers


    def __download(name, url, nameFile, newLoad):
        '''
        Скачивание изображения по ссылке
        @name - запрос
        @url - ссылка на изображение
        @nameFile - название файла
        @newLoad - индикатор первый ли вызов функции
        '''
        HEADERS = DataMod.__getHeaders()
        path = fm.get_Sources_Path(name);
        try:
            with requests.get(url, headers=HEADERS, stream=True, timeout=(5,15)) as r:
                with open(path +'\\'+nameFile, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    print(f'Downloaded file[{nameFile}]: {url}')
                    return True
        except requests.exceptions.SSLError as e:
            # Узнаем имя возникшего исключения
            print(e.__class__.__name__ + f': {url}')
            return False
        except Exception as e:
            # Узнаем имя возникшего исключения
            print(e.__class__.__name__ + f': {url}')
            DataMod.__await(randint(1,5))
            if newLoad:
               return DataMod.__download(name, url, nameFile, False)
        return False


    def __await(sec):
        '''
        Ожидание с выводом в консоль
        @sec - количество секунд
        '''
        for i in range(sec, 0, -1):
            print(f'Sleep: {i:03} s', end = '\r')
            time.sleep(1)

    def imgSearch(name, needCount):
        '''
        Поиск изображения по запросу
        @name - запрос
        @needCount - необходимое количество изображений
        '''

        urls = []
        page = fm.get_Last_Page(name)
        usedURLs = fm.get_Used_Url(name)
        len_file = len(usedURLs)
        query = str.replace(name,' ','%20')
        
        path = fm.get_Sources_Path(name)
        jpg_files = os.listdir(path)
        imagesCount = len(jpg_files)

        while imagesCount < needCount: 
            urls = DataMod.__parsePage(page, query)
            actualUrl = list(set(urls) - set(usedURLs))
            print(f'Found {len(actualUrl)} urls')
            
            with open(fm.get_Used_Url_Path(name), 'a') as file:
                for url in actualUrl:
                    nameFile = 'download_' + str(len_file) + '.jpg'
                    isLoaded = DataMod.__download(name, url, nameFile, True)
                    usedURLs.append(url)
                    file.write(url+"\n")
                    if isLoaded == True:
                        len_file+=1
                        imagesCount+=1
            print(f'{imagesCount} images out of {needCount}')
            page+=1
            fm.save_Last_Page(name,page)

    def __printInfoConnect(url, proxy, headers):
        '''
        Вывод информации о текущем подключении
        @url - ссылка для подключения
        @proxy - ip proxy
        @headers - заголовки строки подключения
        '''
        if not proxy:
            proxy = 'no'

        print()
        print(f'URL: {url}')
        print(f'Proxy: {proxy}')
        print(f'Headers UA: {headers}')


    def __getHtml(page, query, needProxy):
        '''
        Получение кода html страницы
        @page - номер страницы
        @query - запрос
        @needProxy - необходимость прокси для подключения
        '''
        URL = f'https://yandex.ru/images/touch/search?from=tabbar&p={page}&text={query}&itype=jpg'
        HEADERS = DataMod.__getHeaders()
        proxies = DataMod.lastProxies
        proxy = ''
        if(needProxy):
            while not proxies:
                try:
                    proxy = DataMod.frp.get()
                    if(proxy in DataMod.blackProxy):
                        print(f'Proxy {proxy} in black list')
                        continue
                    proxies = { 'http': proxy, 'https': proxy }
                    DataMod.lastProxies = proxies
                except Exception as e:
                    # Узнаем имя возникшего исключения
                    print(e.__class__.__name__ + ' in find proxy')  
                    DataMod.__await(5);
                    DataMod.lastProxies = ''
    
        
        DataMod.__printInfoConnect(URL, proxies, HEADERS)

        try:
            response = requests.get(URL, headers=HEADERS, timeout=2, proxies=proxies, verify=False)
        except Exception as e:
            print(e.__class__.__name__ + f': {URL}') 
            DataMod.lastProxies = ''
            DataMod.blackProxy.append(proxy)
            return DataMod.__getHtml(page, query, True)

        print('Connected')
        
        return response.content

    def reinitIndexs(name):
        '''
        Изменение номеров файлов по порядку 0000, 0001 ...
        @name - запрос
        '''
        path = fm.get_Sources_Path(name)
        jpg_files = os.listdir(path)
        digit_len = len(str(len(jpg_files)))
        
        # Создаём список файлов в папке
        initial_number = 0;
        # Перебираем каждый файл и увеличиваем порядковый номер
        for file_name in jpg_files:
            os.rename(path+'\\'+file_name, path + '\\' + f'tre_{initial_number}.jpg')
            initial_number += 1

        file_names = os.listdir(path)
        initial_number = 0;
        for file_name in file_names:
            indexName = str(initial_number).zfill(digit_len) + '.jpg'
            os.rename(path + '\\' + file_name, path + '\\' + indexName)
            initial_number+=1


    def removeUnunique(name):
        '''
        Удаление неуникальных файлов
        @name - запрос
        '''
        path = fm.get_Small_Path(name)
        if not os.path.isdir(path):
            return 0
        count = 0
        file_names = os.listdir(path)

        for nameA in file_names:
            image_1 = cv2.imread(f'{path}\\{nameA}')

            for nameB in file_names:
                if(nameA == nameB):
                    continue
                image_2 = cv2.imread(f'{path}\\{nameB}')
                if((image_1 == image_2).all()):
                    os.remove(f'{path}\\{nameB}')
                    count+=1
        print(f'Deleted {count} ununique files')
        return len(file_names);

    def removeUnvalide(name):
        '''
        Удаление недоступных файлов
        @name - запрос
        '''
        path = fm.get_Sources_Path(name)
        if not os.path.isdir(path):
            return
        count = 0
        file_names = os.listdir(path)
        for name in file_names:
            image = cv2.imread(f'{path}\\{name}')
            if(image is None):
                os.remove(f'{path}\\{name}')
                count+=1
        print(f'Deleted {count} unvalide files')
     
    
    def resizeImages(name):
        '''
        Масштабирование изображения
        @name - запрос
        '''
        height = 128
        width = 128
        size = (width, height)
        path = fm.get_Sources_Path(name)
        smallP = fm.get_Small_Path(name)

        files_small = os.listdir(smallP)
        for sname in files_small:
            os.remove(f'{smallP}\\{sname}')

        file_names = os.listdir(path)
        for fname in file_names:
            img = cv2.imread(path+f'\\{fname}')
            dst = cv2.resize( img, size )
            cv2.imwrite(smallP + f'\\{fname}', dst)


    def clearData(name):
        '''
        Очистка данных
        @name - запрос
        '''
        print(f'Start cleaning data {name}...')
        print('Removing unvalide files...')
        DataMod.removeUnvalide(name)
        print('Removing non-unique files...')
        count = DataMod.removeUnunique(name)
        print('Updating indexs')
        DataMod.reinitIndexs(name)
        DataMod.resizeImages(name)
        return count

