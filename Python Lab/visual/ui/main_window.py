from collections import defaultdict

from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QWidget, QComboBox, QFileDialog, QMessageBox

from util.Scripts import copy_dataset_to_tag as copy_ds_tags, create_folder
from util.Scripts import copy_dataset_to_rand as copy_ds_rand
from util.Scripts import get_iters_from_annotations as get_iters
from util.Scripts import get_keys_from_dict as get_keys
from Schemes import schemes as s
from Modules.ModelMod import ModelMod as mm

class MessageDialog(QMessageBox):
    '''
    Класс, отвечающий за сообщения
    '''

    def __init__(self, info):
        super().__init__()
        self.setWindowTitle("Сообщение")
        self.setText("Статистика DataFrame:")
        self.setInformativeText(info)
        self.setStandardButtons(QMessageBox.Ok)

class MainWindow(QMainWindow):
    '''
    Класс, ответственный за интерфейс
    '''
    def __init__(self, fm):
        '''
        Конструктор класса
        '''
        super(MainWindow, self).__init__()
        self.fm = fm
        self.title = "Анализатор"
        self.resize(300, 250)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('app/sources/logo.jpg'))
        self.iters = defaultdict(list)
        window = QWidget()
        vbox = QVBoxLayout()
        self.image_view = QLabel()
        img = QPixmap('app/sources/logo.jpg')
        self.image_view.setPixmap(img)

        self.annots = self.fm.get_annotations()

        box_select = QHBoxLayout()
        self.cb_annot = QComboBox()
        ann = ['no'] + self.annots
        self.cb_annot.addItems(ann)
        box_select.addWidget(self.cb_annot)
        btn_open = QPushButton("Загрузить")
        btn_open.clicked.connect(self.btn_open_click)
        box_select.addWidget(btn_open)

        box_create = QHBoxLayout()
        btn_create_rand = QPushButton("Создать датасет(случайная нумерация)")
        btn_create_rand.clicked.connect(self.btn_create_rand)
        btn_create_tag = QPushButton("Создать датасет(по тэгам)")
        btn_create_tag.clicked.connect(self.btn_create_tag)
        box_create.addWidget(btn_create_rand)
        box_create.addWidget(btn_create_tag)

        box_anal = QHBoxLayout()
        btn_stat = QPushButton("Статистика")
        btn_stat.clicked.connect(self.btn_stat_click)
        btn_count = QPushButton("Количество пикселей")
        btn_count.clicked.connect(self.btn_count_click)
        btn_gist = QPushButton("Гистограмма по каналам")
        btn_gist.clicked.connect(self.btn_gist_click)
        btn_gist_img = QPushButton("Гистограмма для изображения")
        btn_gist_img.clicked.connect(self.btn_gist_img_click)
        box_anal.addWidget(btn_stat)
        box_anal.addWidget(btn_count)
        box_anal.addWidget(btn_gist)
        box_anal.addWidget(btn_gist_img)

        box_nav = QHBoxLayout()
        prev_btn = QPushButton("Предыдущее изображение")
        prev_btn.clicked.connect(self.btn_prev_click)
        box_nav.addWidget(prev_btn)
        self.cb_tag = QComboBox()
        self.cb_tag.currentTextChanged.connect(self.on_combobox_changed)
        box_nav.addWidget(self.cb_tag)
        next_btn = QPushButton("Следующее изображение")
        next_btn.clicked.connect(self.btn_next_click)
        box_nav.addWidget(next_btn)

        box_stat = QHBoxLayout()
        mod_btn = QPushButton("Создать модель")
        mod_btn.clicked.connect(self.btn_mod_clicked)
        box_stat.addWidget(mod_btn)

        vbox.addLayout(box_select)
        vbox.addLayout(box_create)
        vbox.addLayout(box_anal)
        vbox.addWidget(self.image_view)
        vbox.addLayout(box_nav)
        vbox.addLayout(box_stat)

        window.setLayout(vbox)
        self.setCentralWidget(window)


    def btn_create_tag(self):
        '''
        Кнопка копирования датасета с тэгами
        '''
        path_ann, _ = QFileDialog.getOpenFileName(None, 'Выберите файл исходной аннотации')
        path_to = create_folder(f'{self.fm.path_copy}\\tag')
        ann = copy_ds_tags(path_to, path_ann, self.fm.path_ann)
        self.cb_annot.addItem(ann)        

    def btn_create_rand(self):
        '''
        Кнопка копирования датасета со случ. номерами
        '''
        path_ann, _ = QFileDialog.getOpenFileName(None, 'Выберите файл исходной аннотации')
        path_to = create_folder(f'{self.fm.path_copy}\\rand')
        ann = copy_ds_rand(path_to, path_ann, self.fm.path_ann)
        self.cb_annot.addItem(ann)


    def btn_open_click(self):
        '''
        Кнопка "загрузить"
        '''
        annot = self.cb_annot.currentText()
        if annot == 'no':
            return

        path_annot = f'{self.fm.create_annotation_folder()}\\{annot}'
        self.iters = get_iters(path_annot)
        tags = ['no'] + list(self.iters.keys()) 
        self.cb_tag.clear()
        self.cb_tag.addItems(tags)

    def btn_next_click(self):
        '''
        Кнопка "следующее изображение"
        '''
        tag = self.cb_tag.currentText()
        if tag == 'no' or tag == '':
            return
        it = self.iters[tag]
        path = it.next()
        if not path:
            print('Достигли конца')
            img = QPixmap('visual/sources/logo.jpg')
            self.image_view.setPixmap(img)
            return

        img = QPixmap(path)
        self.image_view.setPixmap(img)

    def btn_prev_click(self):
        '''
        Кнопка "предыдущее изображение"
        '''
        tag = self.cb_tag.currentText()
        if tag == 'no' or tag == '':
            return

        it = self.iters[tag]
        path = it.prev()
        if not path:
            print('Достигли конца')
            img = QPixmap('visual/sources/logo.jpg')
            self.image_view.setPixmap(img)
            return

        img = QPixmap(path)
        self.image_view.setPixmap(img)

    def on_combobox_changed(self, value):
        '''
        Обработка выбора из combobox
        '''
        if value == 'no'  or value == '':
            img = QPixmap('visual/sources/logo.jpg')
            self.image_view.setPixmap(img)
            return
        it = self.iters[value]
        path = it.get()
        if not path:
            img = QPixmap('visual/sources/logo.jpg')
            self.image_view.setPixmap(img)
            return

        img = QPixmap(path)
        self.image_view.setPixmap(img)

    def btn_stat_click(self):
        '''
        Кнопка получения статистики о датасете
        '''
        annot = self.cb_annot.currentText()
        if annot == 'no':
            return

        path = f'{self.fm.create_annotation_folder()}\\{annot}'
        df = s.annotation_to_frame(path,['cat', 'dog'])
        print(df)
        df = s.statistic(df)
        dialog = MessageDialog(df)
        dialog.exec_()

    def btn_count_click(self):
        '''
        Кнопка получения информации о количестве пикселей в датасете
        '''
        annot = self.cb_annot.currentText()
        if annot == 'no':
            return

        path = f'{self.fm.create_annotation_folder()}\\{annot}'
        df = s.annotation_to_frame(path, get_keys(self.iters))
        df = s.count_pixels_for_group(df)
        dialog = MessageDialog(df)
        dialog.exec_()

    def btn_gist_click(self):
        '''
        Кнопка построения гистаграммы
        '''
        annot = self.cb_annot.currentText()
        if annot == 'no':
            return

        path = f'{self.fm.create_annotation_folder()}\\{annot}'
        df = s.annotation_to_frame(path, get_keys(self.iters))
        b,g,r  = s.compute_histogram(df, 0)
        s.plot_histograms(b,g,r)

    def btn_gist_img_click(self):
        '''
        Нажали на кнопку построения гистаграмм
        '''
        annot = self.cb_annot.currentText()
        if annot == 'no':
            return
        
        tag = self.cb_tag.currentText()
        if tag == 'no' or tag == '':
            return

        it = self.iters[tag]
        path = it.get()
        b,g,r  = s.compute_histogram2(path)
        s.plot_histograms(b,g,r)

    def btn_mod_clicked(self):
        '''
        Нажали на кнопку построения модели
        '''
        model = mm()
        model.split_img()
        model.make_model()

