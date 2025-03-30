import matplotlib.pyplot as plt 
import numpy as np 
import os 
import PIL 
import tensorflow as tf 
  
from tensorflow import keras 
from keras import layers 
from keras.models import Sequential 

import pathlib


'''def split_img():

        data_dir = pathlib.Path('D:/ТвГТУ/1 семестр Маг/Питон/Лабораторные/Python Lab/Python Lab/data/datasets') 
        image_count = len(list(data_dir.glob('*/*.jpg')))

        # Тренировка 
        train_ds = tf.keras.utils.image_dataset_from_directory( 
            data_dir, 
            validation_split=0.2, 
            subset="training", 
            seed=123, 
            image_size=(512, 512), 
            batch_size=32) 

        # Тестирование / Валидация 
        val_ds = tf.keras.utils.image_dataset_from_directory( 
            data_dir, 
            validation_split=0.2, 
            subset="validation", 
            seed=123, 
            image_size=(512,512), 
            batch_size=32) 

        class_names = train_ds.class_names 
        num_classes = len(class_names) 

        model = Sequential([ 
        layers.Rescaling(1./255, input_shape=(512,512, 3)), 
        layers.Conv2D(16, 3, padding='same', activation='relu'), 
        layers.MaxPooling2D(), 
        layers.Conv2D(32, 3, padding='same', activation='relu'), 
        layers.MaxPooling2D(), 
        layers.Conv2D(64, 3, padding='same', activation='relu'), 
        layers.MaxPooling2D(), 
        layers.Flatten(), 
        layers.Dense(128, activation='relu'), 
        layers.Dense(num_classes) 
        ]) 

        model.compile(optimizer='adam', 
              loss=tf.keras.losses.SparseCategoricalCrossentropy( 
                  from_logits=True), 
              metrics=['accuracy']) 
        return model.summary() 

def make_model():
        

        epochs=10
        history = model.fit( 
          self.train_ds, 
          validation_data=self.val_ds, 
          epochs=epochs 
        )

        #Accuracy 
        acc = history.history['accuracy'] 
        val_acc = history.history['val_accuracy'] 
  
        #loss 
        loss = history.history['loss'] 
        val_loss = history.history['val_loss'] 
  
        #epochs  
        epochs_range = range(epochs) 
  
        #Plotting graphs 
        plt.figure(figsize=(8, 8)) 
        plt.subplot(1, 2, 1) 
        plt.plot(epochs_range, acc, label='Training Accuracy') 
        plt.plot(epochs_range, val_acc, label='Validation Accuracy') 
        plt.legend(loc='lower right') 
        plt.title('Training and Validation Accuracy') 
  
        plt.subplot(1, 2, 2) 
        plt.plot(epochs_range, loss, label='Training Loss') 
        plt.plot(epochs_range, val_loss, label='Validation Loss') 
        plt.legend(loc='upper right') 
        plt.title('Training and Validation Loss') 
        plt.show() '''

class ModelMod(object):
    '''
    Класс отвечает за получение и загрузку данных
    '''

    def __init__(self):
        '''
        Конструктор класса
        '''
        self.data_dir = pathlib.Path('D:/ТвГТУ/1 семестр Маг/Питон/Лабораторные/Python Lab/Python Lab/data/datasets') 
        self.image_count = len(list(self.data_dir.glob('*/*.jpg')))

    def split_img(self):
        '''
        Разделяет изображения
        '''
        # Тренировка 
        self.train_ds = tf.keras.utils.image_dataset_from_directory( 
            self.data_dir, 
            validation_split=0.2, 
            subset="training", 
            seed=123, 
            image_size=(512, 512), 
            batch_size=32) 

        # Тестирование / Валидация 
        self.val_ds = tf.keras.utils.image_dataset_from_directory( 
            self.data_dir, 
            validation_split=0.2, 
            subset="validation", 
            seed=123, 
            image_size=(512,512), 
            batch_size=32) 

        self.class_names = self.train_ds.class_names 
        self.num_classes = len(self.class_names) 

    def make_model(self):
        '''
        Создаёт модель
        '''
        model = Sequential([ 
        layers.Rescaling(1./255, input_shape=(512,512, 3)), 
        layers.Conv2D(16, 3, padding='same', activation='relu'), 
        layers.MaxPooling2D(), 
        layers.Conv2D(32, 3, padding='same', activation='relu'), 
        layers.MaxPooling2D(), 
        layers.Conv2D(64, 3, padding='same', activation='relu'), 
        layers.MaxPooling2D(), 
        layers.Flatten(), 
        layers.Dense(128, activation='relu'), 
        layers.Dense(self.num_classes) 
        ]) 

        model.compile(optimizer='adam', 
              loss=tf.keras.losses.SparseCategoricalCrossentropy( 
                  from_logits=True), 
              metrics=['accuracy']) 
        print(model.summary()) 

        epochs=10
        history = model.fit( 
          self.train_ds, 
          validation_data=self.val_ds, 
          epochs=epochs 
        )

        #Accuracy 
        acc = history.history['accuracy'] 
        val_acc = history.history['val_accuracy'] 
  
        #loss 
        loss = history.history['loss'] 
        val_loss = history.history['val_loss'] 
  
        #epochs  
        epochs_range = range(epochs) 
  
        #Plotting graphs 
        plt.figure(figsize=(8, 8)) 
        plt.subplot(1, 2, 1) 
        plt.plot(epochs_range, acc, label='Training Accuracy') 
        plt.plot(epochs_range, val_acc, label='Validation Accuracy') 
        plt.legend(loc='lower right') 
        plt.title('Training and Validation Accuracy') 
  
        plt.subplot(1, 2, 2) 
        plt.plot(epochs_range, loss, label='Training Loss') 
        plt.plot(epochs_range, val_loss, label='Validation Loss') 
        plt.legend(loc='upper right') 
        plt.title('Training and Validation Loss') 
        plt.show()