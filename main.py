from bs4 import BeautifulSoup

import requests
import wget

from urllib.request import urlopen
from urllib.error import HTTPError

import time
import csv
import datetime
import sys

time_start = datetime.datetime.now()


# file_name = 'platan_list.txt'
# csv_file_name = 'platan_list.csv'


def parsing_platan(file_name, csv_file_name):
    file_txt = open(file_name, encoding="utf-8")  # Открываем файл в необходимом формате

    with open(csv_file_name, 'w') as csvfile:
        spamwriter = csv.writer(csvfile,
                                delimiter=';',
                                quotechar='"',
                                escapechar='\\',
                                quoting=csv.QUOTE_ALL)

        for line in file_txt:  # Проходим по списку ID

            url = 'https://www.platan.ru/cgi-bin/qwery.pl/id='
            id_product = line[:-1]  # ID product
            doc_path_arr = []  # Массив путей документов
            pic_path_arr = []  # Массив путей изображений
            url_product = url + id_product  # Соеденяем URL с ID
            try:
                request = requests.get(url_product)  # Создание запроса к необходимой ссылке с продуктом
                bs = BeautifulSoup(request.text, 'html.parser')  # Получение страницы HTML
                all_docs = bs.find('div', id='docs').find_all('p')

                count_doc = 1  # Создание счетчика документов

                for block in all_docs:  # Проходим по массиву элементов
                    if block.find('i', class_='fa fa-file-pdf red-font'):  # Проверяем на наличие знача PDF
                        doc_url = block.find('a')['href']  # Получение значения ссылки
                        if 'google' in doc_url:
                            pass
                        else:
                            try:
                                try:
                                    wget.download(doc_url, out=f'doc/doc_{id_product}_{count_doc}.pdf')  # Скачивание файла
                                    doc_path_arr.append(f'doc/doc_{id_product}_{count_doc}.pdf')
                                    count_doc += 1  # Инкреминация счетчика

                                    time.sleep(0.2)
                                except HTTPError as error:
                                    assert error.code == 404
                                    doc_path_arr.append('no_file')

                            except ValueError:
                                try:
                                    wget.download('https://www.platan.ru' + doc_url, out=f'doc/doc_{id_product}_{count_doc}.pdf')  # Скачивание файла
                                    doc_path_arr.append(f'doc/doc_{id_product}_{count_doc}.pdf')
                                    count_doc += 1  # Инкреминация счетчика

                                    time.sleep(0.2)
                                except HTTPError as error:
                                    assert error.code == 404
                                    doc_path_arr.append('no_file')

                img_list = bs.find('div', class_='card-image bottom-space').find_all('img')
                img_url_arr = []

                for img in img_list:
                    if "preview" in img['src']:
                        pass
                    else:
                        img_url = "https://www.platan.ru" + img['src']
                        if img_url in img_url_arr:
                            pass
                        else:
                            img_url_arr.append(img_url)

                count_img = 1
                for img_url_item in img_url_arr:
                    wget.download(img_url_item, out=f'pic/pic_{id_product}_{count_img}.jpg')
                    pic_path_arr.append(f'pic/pic_{id_product}_{count_img}.jpg')
                    count_img += 1
                    time.sleep(0.2)

                pic_path_str = ''
                doc_path_str = ''

                for pic_path in pic_path_arr:
                    pic_path_str += pic_path + ', '

                for doc_path in doc_path_arr:
                    doc_path_str += doc_path + ', '

                doc_path_str = doc_path_str[:-2]
                pic_path_str = pic_path_str[:-2]

                spamwriter.writerow(
                     [
                         str(id_product),
                         str(pic_path_str),
                         str(doc_path_str)
                     ]
                )
                time.sleep(0.2)
            except HTTPError as error:
                assert error.code == 403

                spamwriter.writerow(
                    [
                        str(id_product),
                        str('bad_link'),
                        str('bad_link')
                    ]
                )

    time_end = datetime.datetime.now()

    print(time_end - time_start)


file_name = sys.argv[1]
csv_file_name = sys.argv[2]

parsing_platan(file_name, csv_file_name)