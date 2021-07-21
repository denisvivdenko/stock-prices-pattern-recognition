'''
Бібліотека для праці з БД
'''
import os, sqlite3
import time, calendar, datetime
from datetime import datetime

source_main_folder_sqlite_db_file = 'D:{sep}db{sep}'.format(sep=os.sep)
'''Неповна адреса папки з файлами БД '''

source_folder_txt_file = '..{sep}..{sep}..{sep}MQL4{sep}Files{sep}SQLite{sep}'.format(sep=os.sep)
'''Неповна адреса папки із текстовими файлами від МТ4'''


arr_tf_minute = [15, 20, 30, 45, 60, 120, 180, 240, 360, 480, 720, 1440]
'''Масив часових проміжків'''


arr_fi = [
  'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'USDCHF', 'USDJPY', 'USDCAD',
  'EURGBP', 'GBPCAD', 'GBPAUD', 'GBPNZD', 'GBPCHF', 'GBPJPY',
  'AUDNZD', 'AUDCAD', 'EURAUD', 'AUDCHF', 'AUDJPY',
  'NZDCAD', 'EURNZD', 'NZDCHF', 'NZDJPY',
  'CADJPY', 'CHFJPY', 'EURCHF', 'EURJPY', 'EURCAD', 'CADCHF',
  'USDMXN', 'USDZAR', 'AUDSGD', 'CHFSGD', 'EURNOK', 'EURSEK',
  'EURSGD', 'SGDJPY', 'USDNOK', 'USDSEK',

  'AUDNOK', 'AUDSEK', 'CHFNOK', 'CHFPLN', 'EURHUF',
  'EURMXN', 'EURPLN', 'EURTRY', 'GBPDKK', 'GBPNOK',
  'GBPPLN', 'GBPSEK', 'GBPSGD', 'GBPZAR', 'NOKJPY',
  'NOKSEK', 'NZDSGD', 'SEKJPY', 'TRYJPY', 'USDCNH',
  'USDCZK', 'USDDKK', 'USDHUF', 'USDPLN', 'USDRUB',
  'USDSGD', 'USDTRY', 'ZARJPY', 'EEM.us', 'FXI.us',
  'GDX.us', 'GLD.us', 'IEF.us', 'IWM.us', 'IYR.us',
  'IYZ.us', 'MCHI.us', 'QQQ.us', 'RSX.us', 'SPY.us',
  'TLT.us', 'XLB.us', 'XLE.us', 'XLF.us', 'XLI.us',
  'XLK.us', 'XLP.us', 'XLU.us', 'XLV.us', 'XLY.us',
  'XAUEUR', 'XAUUSD', 'XAGEUR', 'XAGUSD',

  'CHFHUF..', 'EURCNH..', 'EURCZK..', 'EURRON..', 'EURZAR..',
  'GBPMXN..', 'USDBRL..', 'USDCLP..', 'USDRON..', 'ALUMINIUM..',
  'COPPER..', 'NICKEL..', 'ZINC..', 'PALLADIUM..', 'PLATINUM..',
  'NATGAS..', 'OIL.WTI..', 'OILs..', 'COCOA..', 'COFFEE..',
  'CORN..', 'SOYBEAN..', 'SUGARs..', 'WHEAT..', 'COTTONs..',
  'AUS200..', 'AUT20..', 'DE.30..', 'EU.50..', 'FRA.40..',
  'NED25..', 'RUS50..', 'SPA.35..', 'SUI20..', 'W.20..',
  'ITA.40..', 'JAP225..', 'KOSP200..', 'BUND10Y..', 'CZKCASH..',
  'EMISS..', 'SCHATZ2Y..', 'TNOTE..', 'UK.100..', 'US.100..',
  'US.30..', 'US.500..', 'BRAComp..', 'CHNComp..', 'HKComp..',
  'MEXComp..', 'US2000..', 'USDIDX..', 'VOLX..']

arr_ind = ['_GBPx', '_USDx', '_AUDx', '_NZDx', '_JPYx', '_EURx', '_CHFx', '_CADx']

table_format_create_m1 = '__time integer unique, __open real not null, __high real not null, __low real not null, __close real not null'
table_format_create_m1_vc = 'vc__time integer unique, vc__open real not null, vc__high real not null, vc__low real not null, vc__close real not null'


def getSQLCreateTableM1_VC(num_period, num_period_ind=14):
  '''Повертає команду для створення простої таблиці VC_M00001

  :param int num_period: Таймфрем
  :param int num_period_ind: Період індикатора, для якого розраховуємо
  :rtype: bool'''
  return 'create table if not exists {}({});'.format(getNameTableVC(num_period, num_period_ind), table_format_create_m1_vc)

def getSQLCreateTableM1(num_period):
  '''Повертає команду для створення простої таблиці MT4_M00001'''
  return 'create table if not exists {}({});'.format(getNameTable(num_period), table_format_create_m1)

def getNameTableVC(num_period, num_period_ind=14):
  '''Повертає назву таблиці у вигляді VC_M00001'''
  return 'VC__M{:05d}_{}'.format(num_period, num_period_ind)

def getNameTable(num_period):
  '''Повертає назву таблиці у вигляді MT4_M00001'''
  return 'MT4__M{:05d}'.format(num_period)

def sql_query_create_db_minutes_vc(num):
  '''Повертає команду створення таблиці для індикаторних данних VC'''
  name_table = '{}'.format(getNameTableVC(num))
  format_table = '__time integer unique, __open real not null, __high real not null, __low real not null, __close real not null'
  __sql_send = 'create table if not exists {} ({});'.format(name_table, format_table)
  return __sql_send

def sql_query_create_db_minutes(num):
  '''Повертає потрібний набір команд для створення таблиці з даними для
  певного часового проміжку'''
  name_table = '{}'.format(getNameTable(num))
  format_table = '__time integer unique, __open real not null, __high real not null, __low real not null, __close real not null'
  __sql_send = 'create table if not exists {} ({});'.format(name_table, format_table)
  return __sql_send

def getDayWeekNum(unix_time):
  '''Повертає номер дня тижня вибраної дати
  Monday - 1
  Thuesday - 2...'''
  return datetime.utcfromtimestamp(unix_time).isoweekday()

def getDayWeekText(unix_time):
  '''Повертає текстове значення дня тижня вибраної дати'''
  return '{}'.format(calendar.day_name[datetime.utcfromtimestamp(unix_time).weekday()])

def getUNIX_YMD(unix_date):
  '''Подаємо час вигляду '2021.01.26 15:38:12', а повернути має '2021.01.26'
  тільки у вигляді UNIX формату
  '''
  str1 = time.strftime('%Y.%m.%d', time.gmtime(unix_date))
  int1 = calendar.timegm(time.strptime(str1, '%Y.%m.%d'))
  return int1

def convert_Human2UNIX(str_time):
  '''
  Конвертація формату дати для людини у unix-формат
  '2000.01.21 12:34'
  '''
  return calendar.timegm(time.strptime(str_time, '%Y.%m.%d %H:%M'))

def convert_UNIX2Human(unix_time):
  '''
  Конвертація unix-часу у людський час
  %d %b %Y %H:%M
  '''
  return time.strftime('%d %b %Y %H:%M', time.gmtime(unix_time))

def getListFiles(adres_folder, name_extend):
  '''
  Повертає перелік файлів, які треба прочитати
  '''
  ret = []
  for file in os.listdir(adres_folder):
    if file.endswith(name_extend):
      ret.append('{}'.format(os.path.join('', file)))
  return ret


def sql3_executeQuery(work_file_db, query):
  '''Відправляємо запит на виконання SQLite3 без повернення значень
  work_file_db - повна адреса БД разом із файлом
  query - SQL запит у БД
  '''
  if os.path.exists(work_file_db):
    try:
      connection = sqlite3.connect(work_file_db)
      cursor = connection.cursor()
      cursor.execute(query)
      connection.commit()
      cursor.close()
    except sqlite3.Error as error:
      print("Трапилась помилка під час виконання запиту:\n|{}|\nУ файл:\n{}".format(query, work_file_db), error)
    finally:
      if (connection):
        connection.close()
  else:
    print('Файл {} не знайдений.'.format(work_file_db))

def sql3_sendData(work_file_db, query, data_tuple):
  '''Відправляємо tuple у БД
  Уважно перевіряй відповідність елементів масиву із запитом
  work_file_db - повна адреса БД разом із файлом
  query - SQL запит у БД
  data_tuple - дані у вигляді tuple 
  '''
  if os.path.exists(work_file_db):
    try:
      connection = sqlite3.connect(work_file_db)
      cursor = connection.cursor()
      cursor.executemany(query, data_tuple)
      #print('Записано рядків => {}'.format(cursor.rowcount))
      connection.commit()
      cursor.close()
    except sqlite3.Error as error:
      print("Трапилась помилка під час виконання запиту:\n|{}|\nУ файл:\n{}".format(query, work_file_db), error)
    finally:
      if (connection):
        connection.close()
  else:
    print('Файл {} не знайдений.'.format(work_file_db))

def sql3_getDataMoreRow(work_file_db, query):
  '''Забираємо багато рядків із файла БД
  work_file_db - повна адреса БД разом із файлом
  query - SQL запит у БД
  '''
  ret = -1
  if os.path.exists(work_file_db):
    try:
      connection = sqlite3.connect(work_file_db)
      cursor = connection.cursor()
      cursor.execute(query)
      ret = cursor.fetchall()
      connection.commit()
      cursor.close()
    except sqlite3.Error as error:
      print("Трапилась помилка під час виконання запиту:\n|{}|\nУ файл:\n{}".format(query, work_file_db), error)
    finally:
      if (connection):
        connection.close()
  else:
    print('Файл {} не знайдений.'.format(work_file_db))
  return ret

def sql3_getDataOneRow(work_file_db, query):
  '''Забираємо один рядок із файла БД
  work_file_db - повна адреса БД разом із файлом
  query - SQL запит у БД
  '''
  ret = -1
  if os.path.exists(work_file_db):
    try:
      connection = sqlite3.connect(work_file_db)
      cursor = connection.cursor()
      cursor.execute(query)
      ret = cursor.fetchone()
      connection.commit()
      cursor.close()
    except sqlite3.Error as error:
      print("Трапилась помилка під час виконання запиту:\n|{}|\nУ файл:\n{}".format(query, work_file_db), error)
    finally:
      if (connection):
        connection.close()
  else:
    print('Файл {} не знайдений.'.format(work_file_db))
  return ret

def full_update_vc_table(adr):
  '''Повний перерахунок змісту VC таблиць.
  Усе розраховано на таблиці з періодом 14 та 56

  1) Знищуємо вміст VC таблиці
  2) Створюємо тимчасову таблицю для зберігання даних.
  3) Копіюємо дані з оригінальної таблиці у тимчасову таблицю.
  4) Видаляємо зміст основної таблиці.
  5) Копіюємо дані із тимчасової таблиці у основну. Паралельно працює trigger.
  6) Видаляємо тимчасову таблицю.'''
  arr_period = []
  arr_period.append(14)
  arr_period.append(14*4)
  if os.path.exists(adr):
    try:
      connection = sqlite3.connect(adr)
      cursor = connection.cursor()
      for y in arr_period:
        for i in arr_tf_minute:
          query_1 = 'delete from "main"."{}"; '.format(getNameTableVC(i, y))
          cursor.execute(query_1)
          query_2 = 'create table if not exists tmp ( __time integer unique, __open real not null, __high real not null, __low real not null, __close real not null);'
          cursor.execute(query_2)
          query_3 = 'insert or ignore into tmp select * from {} order by __time asc;'.format(getNameTable(i))
          cursor.execute(query_3)
          query_4 = 'delete from "main"."{}";'.format(getNameTable(i))
          cursor.execute(query_4)
          query_5 = 'insert or ignore into {} select * from tmp order by __time asc;'.format(getNameTable(i))
          cursor.execute(query_5)
          query_6 = 'drop table if exists "main"."tmp";'
          cursor.execute(query_6)
          connection.commit()
      cursor.close()
    except sqlite3.Error as error:
      print("Трапилась помилка під час виконання запиту:\n|{}|\nУ файл:\n{}".format(query, adr), error)
    finally:
      if (connection):
        connection.close()
  else:
    print('Файл {} не знайдений.'.format(adr))

def trigger_insert_after(adr):
  '''Встановити оновлену версію тригера, що слідкує
  за наповненням основної таблиці.
  Коли заходить новий рядок у MT4_M00015 то спрацьовує цей тригер. Він рахує
  4 значення для нових даних.'''
  arr_period = []
  arr_period.append(14)
  arr_period.append(14*4)
  if os.path.exists(adr):
    try:
      connection = sqlite3.connect(adr)
      cursor = connection.cursor()
      for y in arr_period:
        for i in arr_tf_minute:
          query_trigger_drop = 'drop trigger if exists "main"."trigger_after_insert_{i_tf}m_{y_per}p_for_one_row";'.format(i_tf = i, y_per = y)
          query_trigger_create = """
            create trigger if not exists trigger_after_insert_{i_tf}m_{y_per}p_for_one_row after insert
            on {table_source} for each row
            begin
              insert into {table_vc} select * from(
                select
                  __time as vc__time,
                  round((__open - __bvalue)/__avalue, 12) as vc__open,
                  round((__high - __bvalue)/__avalue, 12) as vc__high,
                  round((__low - __bvalue)/__avalue, 12) as vc__low,
                  round((__close - __bvalue)/__avalue, 12) as vc__close
                from
                  (
                    with
                      result
                    as
                    (
                      select
                        __time as __time,
                        __open as __open,
                        __high as __high,
                        __low as __low,
                        __close as __close,
                        __summ as __summ,
                        __diff as __diff,
                        round(sum(__summ), 12) as __tmp_var_bvalue,
                        round(sum(__diff), 12) as __tmp_var_avalue
                      from (
                        select 
                          __time as __time,
                          __open as __open,
                          __high as __high,
                          __low as __low,
                          __close as __close,
                          (__high + __low)/2.0 as __summ,
                          (__high - __low) as __diff
                        from {table_source} order by __time desc limit 14
                      )
                    )
                    select
                      __time,
                      __open,
                      __high,
                      __low,
                      __close,
                      __summ,
                      __diff,
                      __tmp_var_bvalue,
                      __tmp_var_avalue,
                      round(__tmp_var_avalue/14.0*0.2, 12) as __avalue,
                      round(__tmp_var_bvalue/14.0, 12) as __bvalue
                    from
                      result
                  )
              );
            end;
          """.format(table_source=getNameTable(i), table_vc=getNameTableVC(i, y), i_tf = i, y_per = y)
          cursor.execute(query_trigger_drop)
          cursor.execute(query_trigger_create)
          print('Тригер додано для TF={} IND={}.'.format(i, y))
      connection.commit()
      cursor.close()
    except sqlite3.Error as error:
      print("Трапилась помилка під час виконання запиту:\n|{}|\nУ файл:\n{}".format(query, adr), error)
    finally:
      if (connection):
        connection.close()
  else:
    print('Файл {} не знайдений.'.format(adr))


