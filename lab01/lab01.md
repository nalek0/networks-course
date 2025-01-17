# Практика 1. Wireshark: HTTP
Эта работа исследует несколько аспектов протокола HTTP: базовое взаимодействие GET/ответ,
форматы сообщений HTTP, получение больших файлов HTML, получение файлов HTML со
встроенными объектами, а также проверку подлинности и безопасность HTTP.

Во всех заданиях (а также во всех следующих лабах) предполагается, что вы к своему ответу 
приложите **подтверждающий скрин** программы Wireshark (достаточно одного скрина на задание).

## Задание 1. Базовое взаимодействие HTTP GET/response (2 балла)

#### Подготовка
1. Запустите веб-браузер.
2. Запустите анализатор пакетов Wireshark, но пока не начинайте захват пакетов. Введите
   «http» в окне фильтра, чтобы позже в окне списка пакетов отображались только захваченные сообщения HTTP.
3. Подождите несколько секунд, а затем начните захват пакетов Wireshark.
4. Введите в браузере адрес: http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file1.html.  
   Ваш браузер должен отобразить очень простой однострочный HTML-файл.
5. Остановите захват пакетов Wireshark.

#### Вопросы
1. Использует ли ваш браузер HTTP версии 1.0 или 1.1? Какая версия HTTP работает на
   сервере?
   - Запрос моего браузера - `GET /wireshark-labs/HTTP-wireshark-file1.html HTTP/1.1 `, тут видно, что он использует http 1.1 
   - Сервер вернул - `HTTP/1.1 200 OK  (text/html)`, тут тоже видно, что сервер использует http 1.1
2. Какие языки (если есть) ваш браузер может принимать? В захваченном сеансе какую еще
   информацию (если есть) браузер предоставляет серверу относительно пользователя/браузера?
   - `Accept-Language: en-US,en;q=0.9,ru;q=0.8\r\n` говорит, что брайзер принимает английский и русский языки (en-US,en;ru)
   - `User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\r\n` говоит, какой у меня браузер (версия, ОС)
   - `Accept-Encoding: gzip, deflate\r\n` говорит какие методы сжатия данных поддерживает браузер
   - `Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n` говорит, какой контент принимает (html, xml, images, etc...)
3. Какой IP-адрес вашего компьютера? Какой адрес сервера gaia.cs.umass.edu?
   - IP-адрес моего компьютера - `192.168.0.108`, его я получил из столбца **Source** запроса
   - IP-адрес сервера gaia.cs.umass.edu - `128.119.245.12`, его я получил из столбца **Destination** запроса
4. Какой код состояния возвращается с сервера на ваш браузер?
   - `200 OK`
5. Когда HTML-файл, который вы извлекаете, последний раз модифицировался на сервере?
   - В header-ах ответа есть параметр: `Last-Modified: Wed, 21 Feb 2024 06:59:02 GMT\r\n`, то есть последний раз менялся файл 21го февраля
6. Сколько байтов контента возвращается вашему браузеру?
   - `Content-Length: 128\r\n` --- значит возвращается 128 байтов контента

#### Скриншот:

![Task 1](./task1.png "Task#1")

## Задание 2. HTTP CONDITIONAL GET/response (2 балла)
Большинство веб-браузеров выполняют кэширование объектов и, таким образом, выполняют
условный GET при извлечении объекта HTTP. Прежде чем выполнять описанные ниже шаги, 
убедитесь, что кеш вашего браузера пуст.

#### Подготовка
1. Запустите веб-браузер и убедитесь, что кэш браузера очищен.
2. Запустите анализатор пакетов Wireshark.
3. Введите следующий URL-адрес в адресную строку браузера:
   http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html.  
   Ваш браузер должен отобразить очень простой пятистрочный HTML-файл.
4. Введите тот же URL-адрес в браузер еще раз (или просто нажмите кнопку обновления в
   браузере).
5. Остановите захват пакетов Wireshark и введите «http» в окне фильтра, чтобы в окне списка
   пакетов отображались только захваченные HTTP-сообщения.

#### Вопросы
1. Проверьте содержимое первого HTTP-запроса GET. Видите ли вы строку «IF-MODIFIED-SINCE» в HTTP GET?
   - В первом запросе такого хедера нет
2. Проверьте содержимое ответа сервера. Вернул ли сервер содержимое файла явно? Как вы
   это можете увидеть?
   - Файл вернулся явно
   - Результат запроса 200 OK и у ответа есть `Line-based text data: text/html (10 lines)`
3. Теперь проверьте содержимое второго HTTP-запроса GET (из вашего браузера на сторону
   сервера). Видите ли вы строку «IF-MODIFIED-SINCE» в HTTP GET? Если да, то какая
   информация следует за заголовком «IF-MODIFIED-SINCE»?
   - У второго запроса есть данный хедер с параметром: `If-Modified-Since: Wed, 21 Feb 2024 06:59:02 GMT\r\n`
4. Какой код состояния HTTP и фраза возвращаются сервером в ответ на этот второй запрос
   HTTP GET? Вернул ли сервер явно содержимое файла?
   - Ответ с кодом 304 Not Modified
   - Контента файла в ответе нет, как это было в первом запросе

#### Скриншот:

![Task 2](./task2.png "Task#2")

## Задание 3. Получение длинных документов (2 балла)

#### Подготовка
1. Запустите веб-браузер и убедитесь, что кэш браузера очищен.
2. Запустите анализатор пакетов Wireshark.
3. Введите следующий URL-адрес в адресную строку браузера:
   http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html  
   В браузере должен отобразиться довольно длинный текст.
4. Остановите захват пакетов Wireshark и введите «http» в окне фильтра.

#### Вопросы
1. Сколько сообщений HTTP GET отправил ваш браузер? Какой номер пакета в трассировке
   содержит сообщение GET?
   - Отплавляется только один http запрос, если не учитывать запрос favicon 
   - Номер пакета - 74
2. Какой номер пакета в трассировке содержит код состояния и фразу, связанные с ответом
   на HTTP-запрос GET?
   - Номер пакета - 87
3. Сколько сегментов TCP, содержащих данные, потребовалось для передачи одного HTTP ответа?
   - 4 сегмента, три по 1460 байт и один 481 байта
4. Есть ли в передаваемых данных какая-либо информация заголовка HTTP, связанная с
   сегментацией TCP?
   - Есть допалнительный хедер `Accept-Ranges: bytes\r\n`

#### Скриншоты:

![Task 3](./task3.png "Task#3")
![Task 3 Picture 2](./task3.2.png "Task#3 Picture#2")

## Задание 4. HTML-документы со встроенными объектами (2 балла)
Исследуйте, что происходит, когда ваш браузер загружает файл со встроенными объектами, т. е. файл, 
включающий в себя другие объекты (в данном примере это файлы и картинки),
которые хранятся на другом сервере (серверах).

#### Подготовка
1. Запустите веб-браузер и убедитесь, что кэш браузера очищен.
2. Запустите анализатор пакетов Wireshark.
3. Введите следующий URL-адрес в адресную строку браузера:
   http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html.  
   Ваш браузер должен отобразить HTML-файл с двумя изображениями. На эти два изображения есть ссылки в
   базовом файле HTML. То есть сами изображения не содержатся в HTML, вместо этого URL-
   адреса изображений содержатся в загруженном файле HTML. Ваш браузер должен
   получить эти изображения с указанных веб-сайтов.
4. Остановите захват пакетов Wireshark и введите «http» в окне фильтра.

#### Вопросы
1. Сколько HTTP GET запросов было отправлено вашим браузером? На какие интернет-адреса были отправлены эти GET-запросы?
   - Выло отправлено три запроса
   - Первый: `13  1.633998264 192.168.0.108  128.119.245.12 HTTP  568   GET /wireshark-labs/HTTP-wireshark-file4.html HTTP/1.1`
   - Второй: `22  1.779369842 192.168.0.108  128.119.245.12 HTTP  514   GET /pearson.png HTTP/1.1`
   - Третий: `26  1.819171369 192.168.0.108  178.79.137.164 HTTP  493   GET /8E_cover_small.jpg HTTP/1.1`
   - Адреса: Первый и второй: `Host: gaia.cs.umass.edu\r\n`, третий: `Host: kurose.cslash.net\r\n`
2. Можете ли вы сказать, загрузил ли ваш браузер два изображения последовательно или
   они были загружены с веб-сайтов параллельно? Объясните.
   - Можно заметить, что картинки возвращаются уже после того момента, как оба запроса были посланы, поэтому можно утверждать, что запросы посылаются параллельно

#### Скриншот:

![Task 4](./task4.png "Task#4")

## Задание 5. HTTP-аутентификация (2 балла)
Запустите веб-сайт, защищенный паролем, и исследуйте последовательность HTTP-сообщений, которыми обмениваются такие сайты.

#### Подготовка
1. Убедитесь, что кеш вашего браузера очищен.
2. Запустите анализатор пакетов Wireshark.
3. Введите следующий URL-адрес в адресную строку браузера:
   http://gaia.cs.umass.edu/wireshark-labs/protected_pages/HTTP-wireshark-file5.html
4. Введите требуемые имя пользователя и пароль во всплывающем окне  
   (Имя пользователя — «wireshark-students», пароль — «network»).
5. Остановите захват пакетов Wireshark и введите «http» в окне фильтра

#### Вопросы
1. Каков ответ сервера (код состояния и фраза) в ответ на начальное HTTP-сообщение GET от вашего браузера?
   - Первый запрос - `401 Unauthorized` 
2. Когда ваш браузер отправляет сообщение HTTP GET во второй раз, какое новое поле включается в сообщение HTTP GET?
   - Добавляется поле `Authorization: Basic d2lyZXNoYXJrLXN0dWRlbnRzOm5ldHdvcms=\r\n`


#### Скриншот:



![Task 5](./task5.png "Task#5")