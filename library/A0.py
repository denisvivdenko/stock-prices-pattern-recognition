#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Віконна аплікація для редагування даних самої БД
Поле -> Вміст
instrument_title -> EURUSD
instrument_title_long -> Euro vs US Dollar
instrument_broker -> Gerchik # Звідкіля ми беремо дані
digits -> 5 # Кількість цифр після коми або роздільна здатність
comment -> '' # Будь-який коментар до активу

instrument_title -> GDX.us
instrument_title_long -> VanEck Vectors Gold Miners ETF
'''
from PyQt5 import QtCore as qc
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
import os, sys, sqlite3, time, calendar
from mylib import *

btn_style_normal = 'font: 22pt "Consolas";'
btn_style_transfer_data = 'font: 22pt "Consolas"; color: red;'
table_style_normal = 'font: 24pt "Consolas";'



class MainClass(qw.QWidget):
  def __init__(self, parent=None):
    qw.QWidget.__init__(self, parent)
    self.main_layout = self.vbox()
    self.refreshData = self.getBtn('Refresh')
    self.main_layout.addWidget(self.refreshData)
    self.setLayout(self.main_layout)

  def getBtn(self, text):
    '''Повертає мінімалістичну кнопку'''
    btn = qw.QPushButton()
    btn.setText(text)
    btn.setStyleSheet(btn_style_normal)
    return btn
  
  def hbox(self):
    '''Компактний горизонтальний'''
    h_box = qw.QHBoxLayout()
    h_box.setContentsMargins(0,0,0,0)
    h_box.setSpacing(0)
    h_box.setStretch(0,0)
    return h_box

  def vbox(self):
    '''Компактний вертикальний'''
    v_box = qw.QVBoxLayout()
    v_box.setContentsMargins(0,0,0,0)
    v_box.setSpacing(0)
    v_box.setStretch(0,0)
    return v_box

if __name__ == '__main__':
  app = qw.QApplication(sys.argv)
  w = MainClass()
  w.setWindowTitle('Встановлюємо дані для таблиці A0')
  w.setStyleSheet('font: 10pt "Verdana";')
  w.show()
  # w.showMaximized()
  sys.exit(app.exec_())




'''
SPDR S&P 500 ETF Trust — по праву считается самым популярным ETF, который 
состоит из акций крупнейших компаний индекса S&P 500.

iShares 20+ Year Treasury Bond ETF — фактически, данный ETF является индексом, 
который состоит из долгосрочных, 20-летних казначейских облигаций США. 

iShares Emerging Markets ETF — состоит из акции компаний крупной и средней 
капитализации в развивающихся странах (emerging markets) — в Китае, Бразилии, 
Турции и других. 

Vanguard Total World Stock ETF — фонд покрывает множество секторов экономики 
разных стран и состоит из акций американских, китайских, европейских компаний. 
ETF хорошо сбалансирован, в него входит более 7800 компаний. 

SPDR Gold Shares — акции данного фонда на 100% обеспечены собственными запасами 
золота. В хранилище фонда лежит более 700 тонн золота в слитках, что делает его 
самым крупным частным золотохранилищем. 

ETFMG Alternative Harvest ETF — фонд инвестирует в наиболее перспективные 
компании по выращиванию медицинской марихуаны в США. Одно из наиболее 
перспективных направлений в бизнесе сегодня. 

First Trust NASDAQ Clean Edge — позволяет инвестировать в компании развивающихся 
направлений чистой энергетики, включая производителей фотоэлектрических панелей, 
биотоплива или продвинутых аккумуляторных батарей. 

VanEck Vectors Oil Services ETF — фонд отражает динамику 25 нефтяных компаний, 
чьи акции торгуются на фондовом рынке в США. 

iShares US Healthcare ETF — отслеживает индекс Dow Jones U.S. Select Healthcare 
Providers Index, который состоит из акций американских компаний сектора 
медицинских услуг. 

VanEck Vectors Gaming ETF — фонд отслеживает глобальный индекс MVIS, индустрии 
видеоигр и киберспорта. 


'''
