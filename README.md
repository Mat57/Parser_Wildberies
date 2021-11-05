# Parser_Wildberies
Данные скрипты позволяют получить перечень акутальных категорий (с сылками на них) с сервиса WB, а также получать выгрузку по товарам с определенной категории.  
search_categories.py  
Предназначен для получения/обновления категорий. Предусмотрен black_list, исключающий определенные пункты меню.  
Для запуска скрипта необходимо иметь установленный Google Chrome, а также положить в каталог со скриптом веб драйвер.  
В результате работы скрипта сформируются два файла ('list_categories/itog.csv', 'list_categories/itog.txt').  
Данные файлы содержат ссылки на странницы содержащие определенные товары по категориям.

search_data.py  
Данный скрипт отвечает за выгрузку основых параметров по товару: цена, цена со скидкой, фирма производителя, тип товара.  
После запуска, необходимо ввести ссылку на категорию товара, по которой необходимо получить выгрузку.  
