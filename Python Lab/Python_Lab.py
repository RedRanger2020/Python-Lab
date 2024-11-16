import sys
import logging as log
from Modules.FolderMod import FolderMod as fm
from Modules.SetMod import SetMod as sm
from Modules.DataMod import DataMod as dm
from visual.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication

def show_app(fman):
    '''
    Вызов граф. интерфейса
    '''
    app = QApplication(sys.argv)
    w = MainWindow(fman)
    w.show()
    sys.exit(app.exec())

def init_logger():
    '''
    Инициализация логгера
    '''
    logger = log.getLogger("NT_analysis")
    logger.setLevel(log.DEBUG)
    ch = log.StreamHandler()
    ch.setLevel(log.DEBUG)
    logger.addHandler(ch)

def update_dataset(conf, fman):
    '''
    Обновление датасета
    '''
    need_count = conf.image_count
    queries = conf.queries

    data = dm(conf, fman)
    for query in queries:
        data.download_images(query, need_count)
        data.indexation(query)    
    data.save_new_dataset(queries)

def main():
    '''
    Функция точки входа в программу
    ''' 
    init_logger()
    log.basicConfig(level= log.DEBUG)
    conf = sm()
    fman = fm(conf)
    if(conf.need_upd):
        update_dataset(conf, fman)

    show_app(fman)

if __name__ == '__main__':
    main()